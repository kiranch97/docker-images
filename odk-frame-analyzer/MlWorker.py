import os
import logging
import time
import simplejson as json
import asyncio
from odkframelib.DiskWriter import DiskWriter
from aio_pika import connect, Message, IncomingMessage, ExchangeType
from model.garbage_detection import GarbageImageClassifier


disk_writer = DiskWriter()

GarbageImageClassifier = GarbageImageClassifier(cuda=False)

SETTINGS = {
    'RMQ_USER': os.environ.get('RMQ_USER') or 'odk',
    'RMQ_PASSWORD': os.environ.get('RMQ_PASSWORD') or 'rmqodk',
    'RMQ_URL': os.environ.get('RMQ_URL') or '116.203.210.203',
    'RMQ_QUEUE_FRAMES_FOR_ML': 'image_frames_for_ml',
    'RMQ_EXCHANGE_FRAMES_FOR_ML': 'exhange_ml_frames',
    'RMQ_QUEUE_ANALYSED_FRAMES': 'analysed_frames',
    'RMQ_EXCHANGE_FRAMES_ANALYSED': 'exchange_analysed_frames'
}


class MlWorker:

    def __init__(self):
        self.rmq_conn = None
        self.channel = None
        self.setup_logger()
        self.ml_queue_name = None
        self.exchange_ml = None
        self.analysed_queue_name = None
        self.exchange_analysed = None
        self.is_ready = False

    def setup_logger(self):
        self.logger = logging.getLogger(__name__)

        if not self.logger.handlers:
            logging.basicConfig(
                level=logging.INFO,
                format='%(asctime)s %(name)s %(levelname)-4s %(message)s')

    async def setup_consumer(self, ml_queue_name: str):
        self.rmq_conn = await connect(
            "amqp://{0}:{1}@{2}".format(
                SETTINGS['RMQ_USER'],
                SETTINGS['RMQ_PASSWORD'],
                SETTINGS['RMQ_URL']),
            loop=asyncio.get_running_loop()
        )

        print("Connecting to RMQ at URL: {0}".format(SETTINGS['RMQ_URL']))

        self.channel = await self.rmq_conn.channel()

        self.ml_queue_name = ml_queue_name
        self.exchange_ml = await self.channel.declare_exchange(
            SETTINGS['RMQ_EXCHANGE_FRAMES_FOR_ML'], ExchangeType.DIRECT)
        queue_ml = await self.channel.declare_queue(self.ml_queue_name)
        await queue_ml.bind(self.exchange_ml)
        await queue_ml.consume(self.handle_new_frame_on_ml_queue, no_ack=True)

    # ----

    async def setup_queue(self, analysed_queue_name: str):
        self.rmq_conn = await connect(
            "amqp://{0}:{1}@{2}".format(
                SETTINGS['RMQ_USER'],
                SETTINGS['RMQ_PASSWORD'],
                SETTINGS['RMQ_URL']
            ),
            loop=asyncio.get_running_loop()
        )

        self.analysed_queue_name = analysed_queue_name
        self.channel = await self.rmq_conn.channel()
        self.exchange_analysed = await self.channel.declare_exchange(
            SETTINGS['RMQ_EXCHANGE_FRAMES_ANALYSED'], ExchangeType.DIRECT)

        self.is_ready = True

    # ----

    async def queue_analysed_frame(self, analysed_frame_data: dict):
        if not analysed_frame_data:
            return

        if not self.is_ready:
            await self.setup_queue(SETTINGS["RMQ_QUEUE_ANALYSED_FRAMES"])

        analysed_frame_data_Json = json.dumps(analysed_frame_data).encode()

        await self.exchange_analysed.publish(
            Message(analysed_frame_data_Json),
            routing_key=self.analysed_queue_name,
        )

    async def handle_new_frame_on_ml_queue(self, message: IncomingMessage):
        if not self.is_ready:
            await self.setup_queue(SETTINGS["RMQ_QUEUE_ANALYSED_FRAMES"])
        
        frame_data_dict = json.loads(message.body.decode("utf-8"))
        frame_data = json.dumps(frame_data_dict)
        
        analysed_frame_data = \
            GarbageImageClassifier.detect_image(frame_data)

        if analysed_frame_data:
            print("Something detected")
            analysed_frame_data = analysed_frame_data[0]
            analysed_frame_data["app_id"] = frame_data_dict["app_id"]
            analysed_frame_data["take_frame"] = frame_data_dict

            if analysed_frame_data.get("app_id")[:4] == "demo":
                analysed_frame_data["frame_name"] = None

            else:
                analysed_frame_data["frame_name"] = "{0} {1}, {2}.jpeg".format(
                    frame_data_dict.get("timestamp"),
                    frame_data_dict.get("lat"), 
                    frame_data_dict.get("lng")
                )

                await disk_writer.save_file(analysed_frame_data)

            send_analysed_task = asyncio.create_task(
                self.queue_analysed_frame(analysed_frame_data))
            await send_analysed_task

        else:
            print("Nothing detected")
            await disk_writer.save_file(frame_data_dict)


if __name__ == "__main__":
    loop = asyncio.get_event_loop()

    mlworker = MlWorker()

    loop.create_task(
        mlworker.setup_consumer(SETTINGS["RMQ_QUEUE_FRAMES_FOR_ML"]))

    print(' [*] Waiting for frames. To exit press CTRL+C')

    loop.run_forever()
