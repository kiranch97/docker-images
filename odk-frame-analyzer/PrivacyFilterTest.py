from odkframelib.Utils import save_frame_check

# Save frame: YES
count_one_garbage_bag = {
    "total":1,
    "cardboard":0,
    "garbage_bag":1,
    "container_small":0,
    "face_privacy_filter":0,
    "license_plate_privacy_filter":0
}

# Save frame: YES
count_garbage_bag_and_face = {
    "total":2,
    "cardboard":0,
    "garbage_bag":1,
    "container_small":0,
    "face_privacy_filter":1,
    "license_plate_privacy_filter":0
}

# Save frame: NO
count_one_face = {
    "total":1,
    "cardboard":0,
    "garbage_bag":0,
    "container_small":0,
    "face_privacy_filter":1,
    "license_plate_privacy_filter":0
}

# Save frame: NO
count_face_and_car = {
    "total":2,
    "cardboard":0,
    "garbage_bag":0,
    "container_small":0,
    "face_privacy_filter":1,
    "license_plate_privacy_filter":1
}

# Save frame: NO
count_nothing = {
    "total":0,
    "cardboard":0,
    "garbage_bag":0,
    "container_small":0,
    "face_privacy_filter":0,
    "license_plate_privacy_filter":0
}

# Save frame: NO
count_total_count_no_detection = {
    "total":2,
    "cardboard":0,
    "garbage_bag":0,
    "container_small":0,
    "face_privacy_filter":0,
    "license_plate_privacy_filter":0
}

result = save_frame_check(count_one_garbage_bag)
print(result)

result = save_frame_check(count_garbage_bag_and_face)
print(result)

result = save_frame_check(count_one_face)
print(result)

result = save_frame_check(count_face_and_car)
print(result)

result = save_frame_check(count_nothing)
print(result)

result1 = save_frame_check(count_total_count_no_detection)
print(result)