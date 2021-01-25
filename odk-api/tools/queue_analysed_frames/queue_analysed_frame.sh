#!/bin/bash

# -- Analysed Frame Queuing Tool --
#
# Using the `rabbitmqadmin` cli tool for queueing a dummy analysed frame,
# to check function `broker.incoming.handle_analysed_frame`, e.g.:
# $ rabbitmqadmin publish exchange=amq.default routing_key=test payload="hello, world"
#
# Using `docker exec` it will look like this:
# $ docker exec -it odk-rmq rabbitmqadmin --help
# $ docker exec -it odk-rmq rabbitmqadmin -u $RABBITMQ_DEFAULT_USER -p $RABBITMQ_DEFAULT_PASS list queues
#
# Docs: https://www.rabbitmq.com/management-cli.html

# 1) Setup environment variables to connect to RabbitMQ
RABBITMQ_DEFAULT_USER=odk
RABBITMQ_DEFAULT_PASS=development

folder='./dummy_analysed_frames'

# 2) Handling first parameter for options
if [ $1 == "success" ]
  then
    data=`cat $folder/analysed_frame.json`
    echo "Sending 'success' message"
elif [ $1 == "missing-key" ]
  then
    data=`cat $folder/analysed_frame_missing_key.json`
    echo "Sending 'missing-key' message"
elif [ $1 == "missing-data" ]
  then
    data=`cat $folder/analysed_frame_missing_data.json`
    echo "Sending 'missing-data' message"
elif [ $1 == "wrong-key" ]
  then
    data=`cat $folder/analysed_frame_wrong_key.json`
    echo "Sending 'wrong-key' message"
elif [ $1 == "not-json" ]
  then
    data="foobar"
    echo "Sending 'not-json' message"
fi

# 3) Sending JSON frame data to exchange to be queued
docker exec -it odk-rmq rabbitmqadmin -u $RABBITMQ_DEFAULT_USER -p $RABBITMQ_DEFAULT_PASS publish exchange=exchange_analysed_frames routing_key=frame payload="$data"
