from datetime import datetime
import os
import base64


class DiskWriter:
    def __init__(self):
        pass

    def save_file(self, analysed_frame_data: dict, something_detected=False):

        machine_hostname = os.uname()[1]

        folder_path = './{0}'.format(machine_hostname)

        if something_detected:
            folder_path = '{0}/something'.format(folder_path)
        else:
            folder_path = '{0}/nothing'.format(folder_path)

        # Setup all the needed variables
        app_id = analysed_frame_data['take_frame']['app_id']
        img = analysed_frame_data['take_frame']['img']
        timestamp = analysed_frame_data['take_frame']['timestamp']
        gps_lat = analysed_frame_data['location']['lat']
        gps_lng = analysed_frame_data['location']['lng']
        frame_date = datetime.now().strftime("%Y-%m-%d")

        # Decode base64 image
        imgdata = base64.b64decode(img.replace("data:image/jpeg;base64,", ""))

        # Set file name and location
        gps_location = "{0}_{1}".format(gps_lat, gps_lng)
        filepath = "{0}/{1}/{2}".format(folder_path,
                                        frame_date,
                                        app_id)

        if not os.path.exists(filepath):
            os.makedirs(filepath)
            # print("made new directory called {}".format(filepath))

        filename = "{0}_{1}.jpg".format(timestamp, gps_location)
        full_filename = "{0}/{1}".format(filepath, filename)

        # Save file to filesystem
        with open(full_filename, 'wb') as f:
            f.write(imgdata)
            print("File saved called {}".format(full_filename))

        # Return the file location to store this in database
        return full_filename