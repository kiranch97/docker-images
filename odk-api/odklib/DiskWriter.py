from datetime import datetime
import os
import base64


class DiskWriter:
    def __init__(self):
        self.FRAME_DIR = "../frames"

    async def save_file(self, frame_data: dict):
        # Needed extras
        frame_date = datetime.now().strftime("%Y-%m-%d")

        if 'frame_meta' in frame_data.keys():
            # Data from MlWorker
            FRAME_DIR = "frames-analysed"

            img = frame_data.get(
                'take_frame', {}).get(
                    'img')
            app_id = frame_data.get(
                'take_frame', {}).get(
                    'app_id')
            gps_lat = frame_data.get(
                'take_frame', {}).get(
                    'lat')
            gps_lng = frame_data.get(
                'take_frame', {}).get(
                    'lng')
            timestamp = frame_data.get(
                'take_frame', {}).get(
                    'timestamp').replace(
                        ':', '-').split(" ")[1]
        else:
            # Data from client
            FRAME_DIR = "../frames"

            img = frame_data.get(
                'img')
            app_id = frame_data.get(
                'app_id')
            gps_lat = frame_data.get(
                'lat')
            gps_lng = frame_data.get(
                'lng')
            timestamp = frame_data.get(
                'timestamp').replace(
                    ':', '-').split(" ")[1]

        if app_id is None:
            # print("No Device data, file not saved")
            pass
        elif gps_lat is None or gps_lng is None:
            # print("No GPS data, file not saved")
            pass
        else:
            imgdata = base64.b64decode(img)
            gps_location = "{0}-{1}".format(gps_lat, gps_lng)
            filepath = "{0}/{1}/{2}".format(FRAME_DIR,
                                            frame_date,
                                            app_id)

            if not os.path.exists(filepath):
                os.makedirs(filepath)
                # print("made new directory called {}".format(filepath))

            filename = "{0}-{1}.jpeg".format(timestamp, gps_location)
            full_filename = "{0}/{1}".format(filepath, filename)

            with open(full_filename, 'wb') as f:
                f.write(imgdata)
                # print("file saved called {}".format(full_filename))

            # await websocket.send_text("thanks for data!")
            # await data = json.loads(json_data)

    # ----

    def fill_stats_dict(self, stats):
        frame_year = datetime.now().strftime("%Y")
        frame_month = datetime.now().strftime("%Y-%m")

        if 'total_frames' not in stats.keys():
            stats['total_frames'] = 0

        if 'yearly_frames' not in stats.keys():
            stats['yearly_frames'] = {}
            if frame_year not in stats['yearly_frames'].keys():
                stats['yearly_frames'] = {frame_year: {}}

        if 'monthly_frames' not in stats.keys():
            stats['monthly_frames'] = {}
            if frame_year not in stats['monthly_frames'].keys():
                stats['monthly_frames'] = {frame_year: {}}
                if frame_month not in \
                   stats['monthly_frames'][frame_year].keys():
                    stats['monthly_frames'][frame_year] = {frame_month: 0}

        if 'today_frames' not in stats.keys():
            stats['today_frames'] = 0

    # ----

    def count_all_files(self, stats):
        if 'total_frames' in stats.keys():
            stats['total_frames'] = sum([len(total_files) for
                                        p,
                                        d,
                                        total_files in
                                        os.walk(self.FRAME_DIR)])

    # ----

    def count_yearly_files(self, stats):
        if 'yearly_frames' in stats.keys():
            # Needed extras
            yearly_files = 0
            frame_year = datetime.now().strftime("%Y")
            DIR_THIS_YEAR = "frames\\{}".format(frame_year)

            for all_paths, d, f in os.walk(self.FRAME_DIR):
                if all_paths[:-6] == DIR_THIS_YEAR:
                    # Get total amount of files this year
                    yearly_files += sum([len(yearly_files) for
                                        p,
                                        d,
                                        yearly_files in
                                        os.walk(all_paths)])

            stats['yearly_frames'][frame_year] = yearly_files

    # ----

    def count_monthly_files(self, stats):
        if 'monthly_frames' in stats.keys():
            # Needed extras
            monthly_files = 0
            frame_year = datetime.now().strftime("%Y")
            frame_month = datetime.now().strftime("%Y-%m")
            DIR_THIS_MONTH = "frames\\{}".format(frame_month)

            for all_paths, d, f in os.walk(self.FRAME_DIR):
                if all_paths[:-3] == DIR_THIS_MONTH:
                    # Get total amount of files this month
                    monthly_files += sum([len(monthly_files) for
                                          p,
                                          d,
                                          monthly_files in
                                          os.walk(all_paths)])

            stats['monthly_frames'][frame_year][frame_month] = monthly_files

    # ----

    def count_today_files(self, stats):
        if 'today_frames' in stats.keys():
            # Needed extras
            today_files = 0
            frame_date = datetime.now().strftime("%Y-%m-%d")
            DIR_TODAY = "frames\\{}".format(frame_date)

            for all_paths, d, f in os.walk(self.FRAME_DIR):
                if all_paths == DIR_TODAY:
                    # Get total amount of files today
                    today_files += sum([len(today_files) for
                                        p,
                                        d,
                                        today_files in
                                        os.walk(all_paths)])

            stats['today_frames'] = today_files

    # ----

    async def count_app_id_today_files(self,
                                       frame_data,
                                       running_clients,
                                       stats):
        # Data from client
        app_id = frame_data.get('app_id')
        # Needed extras
        frame_date = datetime.now().strftime("%Y-%m-%d")
        DIR_TODAY = "frames\\{}".format(frame_date)

        for all_paths, d, f in os.walk(self.FRAME_DIR):
            if all_paths == DIR_TODAY:
                # Get all folders in path of today
                for today_app_id_paths, d, f, in os.walk(all_paths):
                    DIR_APP_ID_TODAY = "{0}\\{1}".format(DIR_TODAY, app_id)
                    if today_app_id_paths == DIR_APP_ID_TODAY:
                        try:
                            running_clients[app_id]['frames_today'] = sum(
                                [len(today_app_id_files) for
                                 p,
                                 d,
                                 today_app_id_files in
                                 os.walk(today_app_id_paths)])

                        except Exception:
                            pass
                    # amount_of_frames_per_folder_today = sum(
                    # [len(device_files) for
                    #  p,
                    #  d,
                    #  device_files in os.walk(today_app_id_paths)])
                    # print("Folder: {0} # of Photos: {1}".format(
                    #   today_app_id_paths,
                    #   amount_of_frames_per_folder_today))
