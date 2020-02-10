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

    '''

    Example of frame data dictionary as it is retrieved from the queue:

    frame_data_dict = {
        '_debug_rmq_time_on_queue': 1581347922959,
        'app_id': 'cgar53mb78',
        'img': 'data:image/jpeg:base64,/9j/rtPcyeyAs1KrYPzSksm...', # raw frame
        'lat': 52.3736064,
        'lng': 4.9145957,
        'state': True,
        'timestamp': '2020-02-10 16:18:41.0089',
        'user_type': 'demo'
    }

    Will be transformed into 'analysed_frame':

    analaysed_frame_data = {
        'counts': {'cardboard': 0, 'garbage_bag': 1, ..., 'total': 1},
        'detected_objects': [{'bbox': {...}, 'confidence': 99, 'detected_object_type': 'garbage_bag'}],
        'frame_meta': {'height': 608, 'width': 1080},
        'ml_done_at': '2020-02-10 16:26:49.240261',
        'ml_time_taken': '0:00:01.515924',
        'take_frame': {
            'img': 'data:image/jpeg:base64,/9j/rtPcyeyAs1KrYPzSksm...', # blurred frame
            'timestamp': '2020-02-10 16:18:41.0089'
        },
        'frame_name': '', #TODO: change mapping of lat lng to seperate value
        'user_type': 'demo',
        'created_by_app': 'cgar53mb78'
    }
    
    '''

    async def handle_new_frame_on_ml_queue(self, message: IncomingMessage):
        if not self.is_ready:
            await self.setup_queue(SETTINGS["RMQ_QUEUE_ANALYSED_FRAMES"])

        frame_data_dict = json.loads(message.body.decode("utf-8"))
        frame_data = json.dumps(frame_data_dict)
        
        analysed_frame_data= GarbageImageClassifier.detect_image(frame_data)

        if analysed_frame_data:
            analysed_frame_data = analysed_frame_data[0]

            print("Something detected", analysed_frame_data['counts'])

            analysed_frame_data["user_type"] = frame_data_dict["user_type"]
            analysed_frame_data['take_frame']['timestamp'] = frame_data_dict["timestamp"]
            analysed_frame_data['take_frame']['app_id'] = frame_data_dict["app_id"]
            analysed_frame_data['location'] = {}
            analysed_frame_data['location']['lat'] = frame_data_dict['lat']
            analysed_frame_data['location']['lng'] = frame_data_dict['lng']

            # TODO: turn check if demo on when going live

            # if analysed_frame_data.get('user_type') != 'demo'
            #    file_location = disk_writer.save_file(analysed_frame_data, something_detected=true)

            file_location = disk_writer.save_file(analysed_frame_data, something_detected=True)

            analysed_frame_data['frame_name'] = file_location

            # TODO: turn check if demo on when going live

            # if analysed_frame_data.get('user_type') == 'demo':
            #     analysed_frame_data["frame_name"] = None

            send_analysed_task = asyncio.create_task(
                self.queue_analysed_frame(analysed_frame_data))
            await send_analysed_task

        else:
            print("Nothing detected")
            
            if frame_data_dict.get("user_type") != "demo":
                disk_writer.save_file(frame_data_dict, something_detected=False)


if __name__ == "__main__":
    loop = asyncio.get_event_loop()

    mlworker = MlWorker()

    loop.create_task(
        mlworker.setup_consumer(SETTINGS["RMQ_QUEUE_FRAMES_FOR_ML"]))

    print(' [*] Waiting for frames. To exit press CTRL+C')

    loop.run_forever()
