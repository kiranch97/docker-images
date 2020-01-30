from datetime import datetime
import os
import base64


class DiskWriter:
    def __init__(self):
        pass

    async def save_file(self, analysed_frame_data: dict):
        # Needed extras
        frame_date = datetime.now().strftime("%Y-%m-%d")

        if 'frame_name' in analysed_frame_data.keys():
            # Frame with objects
            FRAME_DIR = "/data/odk/images/objects/"

            img = analysed_frame_data.get(
                'take_frame', {}).get(
                    'img')
            app_id = analysed_frame_data.get(
                'take_frame', {}).get(
                    'app_id')
            gps_lat = analysed_frame_data.get(
                'take_frame', {}).get(
                    'lat')
            gps_lng = analysed_frame_data.get(
                'take_frame', {}).get(
                    'lng')
            timestamp = analysed_frame_data.get(
                'take_frame', {}).get(
                    'timestamp').replace(
                        ':', '-')
        else:
            # Frame without objects
            FRAME_DIR = "/data/odk/images/no-objects/"

            img = analysed_frame_data.get(
                'img')
            app_id = analysed_frame_data.get(
                'app_id')
            gps_lat = analysed_frame_data.get(
                'lat')
            gps_lng = analysed_frame_data.get(
                'lng')
            timestamp = analysed_frame_data.get(
                'timestamp').replace(
                    ':', '-')

        if app_id is None:
            # print("No Device data, file not saved")
            pass
        elif gps_lat is None or gps_lng is None:
            # print("No GPS data, file not saved")
            pass
        else:
            imgdata = base64.b64decode(img)
            gps_location = "{0}, {1}".format(gps_lat, gps_lng)
            filepath = "{0}/{1}/{2}".format(FRAME_DIR,
                                            frame_date,
                                            app_id)

            if not os.path.exists(filepath):
                os.makedirs(filepath)
                # print("made new directory called {}".format(filepath))

            filename = "{0} {1}.jpg".format(timestamp, gps_location)
            full_filename = "{0}/{1}".format(filepath, filename)

            with open(full_filename, 'wb') as f:
                f.write(imgdata)
                # print("file saved called {}".format(full_filename))
