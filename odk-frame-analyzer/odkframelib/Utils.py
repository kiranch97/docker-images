from datetime import datetime
import os
import base64


def save_file(analysed_frame_data, something_detected=False):

    machine_hostname = os.uname()[1]

    folder_path = './frames/{0}'.format(machine_hostname)

    if something_detected:
        folder_path = '{0}/something'.format(folder_path)
        app_id = analysed_frame_data['take_frame']['app_id']
        img = analysed_frame_data['take_frame']['img']
        timestamp = analysed_frame_data['take_frame']['timestamp']
        gps_lat = analysed_frame_data['location']['lat']
        gps_lng = analysed_frame_data['location']['lng']

    else:
        folder_path = '{0}/nothing'.format(folder_path)
        app_id = analysed_frame_data['app_id']
        img = analysed_frame_data['img']
        timestamp = analysed_frame_data['timestamp']
        gps_lat = analysed_frame_data['lat']
        gps_lng = analysed_frame_data['lng']

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

# False: do not save frame
# True: frame may be saved
def save_frame_check(counts):
    if counts.get('total') <= 0:
        return False

    del counts['total']

    privacy_flag = False
    others_flag = False
    
    for k, v in counts.items():
        # if either privacy filter is detected set privacy flag on TRUE
        if (k == 'face_privacy_filter' or k == 'license_plate_privacy_filter') and v > 0:
            privacy_flag = True
        
        # if anything other then privacy filter is detected set other flag TRUE
        if k != 'face_privacy_filter' and k != 'license_plate_privacy_filter' and v > 0:
            others_flag = True

    if privacy_flag is True and others_flag is False:
        return False
    if privacy_flag is False and others_flag is False:
        return False
    else:
        return True
