import os
import logging

import time

from typing import List
from starlette.websockets import WebSocket

import simplejson as json

import asyncio
from aio_pika import connect, Message, IncomingMessage, ExchangeType

from odklib.DiskWriter import DiskWriter
from odklib.DatabaseManager import DatabaseManager

diskwriter = DiskWriter()
dbm = DatabaseManager("postgresql://odk:pgodk@116.203.210.203:5432/odk")

SETTINGS = {
    'RMQ_USER': os.environ.get('RMQ_USER') or 'odk',
    'RMQ_PASSWORD': os.environ.get('RMQ_PASSWORD') or 'rmqodk',
    'RMQ_URL': os.environ.get('RMQ_URL') or '116.203.210.203',

    'RMQ_QUEUE_FRAMES_FOR_DASH': 'image_frames_for_dash',
    'RMQ_EXCHANGE_FRAMES_FOR_DASH': 'exhange_broadcast_frames',

    'RMQ_QUEUE_ANALYSED_FRAMES_FOR_DASH':
        'analysed_frames_for_dash',
    'RMQ_EXCHANGE_ANALYSED_FRAMES_FOR_DASH':
        'exhange_broadcast_analysed_frames',

    'RMQ_EXCHANGE_FRAMES_FOR_ML': 'exhange_ml_frames',
    'RMQ_QUEUE_FRAMES_FOR_ML': 'image_frames_for_ml',

    'RMQ_QUEUE_ANALYSED_FRAMES': 'analysed_frames',
    'RMQ_EXCHANGE_FRAMES_ANALYSED': 'exchange_analysed_frames'
}


"""

    FrameBroker distributes image frames and analysed frames with the help of
    a RabbitMQ instance

    IMPORTANT: we need a central place to save frames, because of the multiple
    worker we use to deploy FastAPI on Gunicorn

    transactions:
        * Dashboard side:
            - [ image_frames_for_dash - ImageFrame ] -
                producer {{ broadcast }}
            - [ image_frames_for_dash - ImageFrame ] -
                consumer {{ broadcast }} and sender to websockets
            - [ analyses_frames_for_dash - AnalysedFrame ] -
                producer {{ broadcast }} TODO
            - [ analyses_frames_for_dash - AnalysedFrame ] -
                 consumer {{ broadcast }} TODO
        * Machine learner side
            - [ image_frames_for_ml - ImageFrame ] -
                producer {{ direct }}


"""


class FrameBroker:

    def __init__(self):

        self.connections: List[WebSocket] = []
        self.is_ready = False
        self.setup_logger()
        self.rmq_conn = None
        self.channel = None

        self.dash_queue_name = None
        self.exchange_dash = None

        self.dash_analysed_queue_name = None
        self.exchange_dash_analysed = None

        self.ml_queue_name = None
        self.exchange_ml = None

        self.analysed_queue_name = None
        self.exchange_analysed = None
        # self.queues = {}
        # self.exchanges = {}

    # ----

    def setup_logger(self):

        self.logger = logging.getLogger(__name__)

        if not self.logger.handlers:
            logging.basicConfig(level=logging.INFO, format='%(asctime)s' +
                                                           '%(name)s' +
                                                           '%(levelname)-4s' +
                                                           '%(message)s')

    # ----

    async def setup_all_queues(self,
                               dash_queue_name: str,
                               dash_analysed_queue_name: str,
                               ml_queue_name: str,
                               analysed_queue_name: str):

        # QUEUES : [
        #       { name: "analused_frame_for_dash", "FANOUT" },
        #       { name: "images_for_ml", "DIRECT" },
        #        { name: "analysed_frames", "FANOUT" }
        # ]
        # @ queue_list: [ { "name", "exchange_type" : FANOUT|DIRECT } ]

        # TODO: catch error on wrong RMQ credentials !
        self.rmq_conn = await connect(
            "amqp://{0}:{1}@{2}".format(SETTINGS['RMQ_USER'],
                                        SETTINGS['RMQ_PASSWORD'],
                                        SETTINGS['RMQ_URL']),
            loop=asyncio.get_running_loop()
        )

        # setup channels
        self.channel = await self.rmq_conn.channel()

        # dash channel
        self.dash_queue_name = dash_queue_name
        self.exchange_dash = await self.channel.declare_exchange(
            SETTINGS['RMQ_EXCHANGE_FRAMES_FOR_DASH'], ExchangeType.FANOUT)
        queue_dash = await self.channel.declare_queue(self.dash_queue_name)
        await queue_dash.bind(self.exchange_dash)
        await queue_dash.consume(
            self.handle_new_frame_on_dash_queue,
            no_ack=True)

        # dash analysed channel
        self.dash_analysed_queue_name = dash_analysed_queue_name
        self.exchange_dash_analysed = await self.channel.declare_exchange(
            SETTINGS['RMQ_EXCHANGE_ANALYSED_FRAMES_FOR_DASH'],
            ExchangeType.FANOUT)
        queue_analysed_dash = await self.channel.declare_queue(
            self.dash_analysed_queue_name)
        await queue_analysed_dash.bind(self.exchange_dash_analysed)
        await queue_analysed_dash.consume(
            self.handle_new_analysed_frame_on_dash_queue,
            no_ack=True)

        # to ml channel (to be analysed)
        self.ml_queue_name = ml_queue_name
        self.exchange_ml = await self.channel.declare_exchange(
            SETTINGS['RMQ_EXCHANGE_FRAMES_FOR_ML'], ExchangeType.DIRECT)

        # from ml channel (analysed)
        self.analysed_queue_name = analysed_queue_name
        self.exchange_analysed = await self.channel.declare_exchange(
            SETTINGS['RMQ_EXCHANGE_FRAMES_ANALYSED'], ExchangeType.DIRECT)
        queue_analysed = await self.channel.declare_queue(
            self.analysed_queue_name)
        await queue_analysed.bind(self.exchange_analysed)
        await queue_analysed.consume(self.handle_analysed_frame, no_ack=True)

        self.is_ready = True

    # ----

    async def connect_to_websocket(self, websocket: WebSocket):
        await websocket.accept()
        self.logger.info("Added websocket connection to connections")
        self.logger.info(websocket)
        self.connections.append(websocket)

    # ----

    async def send_message_on_queues(self,
                                     frame_data: dict,
                                     stats: dict,
                                     running_clients: dict):

        # add time on queue
        frame_data['_debug_rmq_time_on_queue'] = int(round(time.time() * 1000))

        if not self.is_ready:
            await self.setup_all_queues(
                SETTINGS["RMQ_QUEUE_FRAMES_FOR_DASH"],
                SETTINGS["RMQ_QUEUE_ANALYSED_FRAMES_FOR_DASH"],
                SETTINGS["RMQ_QUEUE_FRAMES_FOR_ML"],
                SETTINGS["RMQ_QUEUE_ANALYSED_FRAMES"])

        frameJson = json.dumps(frame_data).encode()
        # statsJson = json.dumps(stats).encode()
        # running_clientsJson = json.dumps(running_clients).encode()

        # send messages to Dashboard
        await self.exchange_dash.publish(
            Message(frameJson),
            routing_key=self.dash_queue_name,
        )

        # await self.exchange_dash.publish(
        #     Message(statsJson),
        #     routing_key=self.dash_queue_name,
        # )

        # await self.exchange_dash.publish(
        #     Message(running_clientsJson),
        #     routing_key=self.dash_queue_name,
        # )

        await self.exchange_ml.publish(
            Message(frameJson),
            routing_key=self.ml_queue_name,
        )

        self.logger.debug("=> Broker: queue new frame - app_id : '{0}'".format(
            frame_data['app_id']))

    # ----

    def remove_websocket(self, websocket: WebSocket):
        self.connections.remove(websocket)

    # ----

    async def handle_new_frame_on_dash_queue(self, message: IncomingMessage):

        # when a new frame is detected on the queue: this will send it through
        # connected websockets

        # add time passed as debug to image frame
        frame_data_dict = json.loads(message.body.decode("utf-8"))
        frame_data_dict["_debug_rmq_off_time"] = int(round(time.time() * 1000))
        frame_data = json.dumps(frame_data_dict)

        living_connections = []

        while len(self.connections) > 0:
            websocket = self.connections.pop()
            # self.logger.info("=> Got message from queue")
            # self.logger.info(message)
            # print("=> Got message from queue")
            await websocket.send_text(frame_data)
            living_connections.append(websocket)

        self.connections = living_connections

    # ----

    async def handle_analysed_frame(self, message: IncomingMessage):

        # Get new analysed frame from MlWorker
        analysed_frame_data = json.loads(message.body.decode("utf-8"))
        analysed_frameJson = json.dumps(analysed_frame_data).encode()

        # send analysed frame to Dashboard
        await self.exchange_dash_analysed.publish(
            Message(analysed_frameJson),
            routing_key=self.dash_analysed_queue_name,
        )

        # Persist analysed frame on database
        dbm.add_analysed_frame(analysed_frame_data)

        # Save frame in 'frames-analysed' Folder
        await diskwriter.save_file(analysed_frame_data)

    # ----

    async def handle_new_analysed_frame_on_dash_queue(
      self,
      message: IncomingMessage):
        analysed_frame_data_dict = json.loads(message.body.decode("utf-8"))
        analysed_frame_data_dict["_debug_rmq_off_time"] = int(
            round(time.time() * 1000))
        analysed_frame_data = json.dumps(analysed_frame_data_dict)

        return

        # # Print incoming message
        # print(analysed_frame_data)
        # print("did fanout analysed")
