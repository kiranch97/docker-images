from odklib.DatabaseManager import DatabaseManager

dbm = DatabaseManager("postgresql://odk:pgodk@116.203.210.203:5432/odk")

# result_do = dbm.get_detected_objects(
#     "223344",
#     "2019-12-02")
# result_laf = dbm.get_last_analysed_frames(
#     "223344",
#     "2019-12-02")
# result_dsd = dbm.get_dash_stream_devices(
#     "223344+111222",
#     "2019-12-05")
# result_dt = dbm.get_dash_total(
#     "2019-12-13")
result_dmd = dbm.get_dash_map_data(
    "2019-12-13")

print(result_dmd)
