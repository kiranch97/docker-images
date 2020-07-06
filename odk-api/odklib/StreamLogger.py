from datetime import datetime


class StreamLogger:
    def __init__(self):
        pass

    def active_streams_check(self, frame_data, running_clients):
        stream_id = frame_data.get('stream_id')
        state = frame_data.get('state')

        if stream_id not in running_clients.keys():
            new_running_client = {
                'stream_id': stream_id,
                'frames_today': 0,
                'stream_start_time': datetime.now().strftime(
                    "%Y-%m-%d|%H:%M:%S")}
            running_clients[stream_id] = new_running_client
            print("=============================================")
            print("New running Client:")
            print("\t - {}".format(new_running_client['stream_id']))

        running_clients['total_streams'] = len(running_clients.keys()) - 1

        if stream_id in running_clients.keys():
            if not state:
                print("=============================================")
                print("Client stopped:")
                print("\t - {}".format(running_clients[stream_id]['stream_id']))
                del running_clients[stream_id]
                if len(running_clients.keys()) > 1:
                    print("=============================================")
                    if len(running_clients.keys()) == 2:
                        print("1 Running Client:")
                    else:
                        print("{} Running Clients:".format(
                            running_clients['total_streams'] - 1))
                    del running_clients['total_streams']
                    for stream_id in running_clients.keys():
                        print("\t - {0} ({1})".format(
                            running_clients[stream_id]['stream_id'],
                            running_clients[stream_id]['frames_today']))
                else:
                    print("=============================================")
                    print("No Clients active")
                    running_clients['total_streams'] = 0
