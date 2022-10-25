import pyecowitt.ecowitt as ecowitt
import asyncio
import sys
import csv
from pathlib import Path
import time



def usage():
    print("Usage: {0} port".format(sys.argv[0]))


async def my_handler(data, path):
    # print("In my handler")
    # print(data)
    to_be_saved_data = {}
    capture_fields = ['systemtimeutc', 'stationtype', 'runtime', 'dateutc', 'windspeedms', 'winddir',  'windgustms', 'maxdailygustms', 'rrain_piezo', 'erain_piezo', 'hrain_piezo', 'drain_piezo', 'wrain_piezo', 'mrain_piezo',
                      'yrain_piezo', 'solarradiation', 'uv', 'humidity',  'tempc', 'tempinc',  'baromrelhpa', 'baromabshpa', 'windchillc', 'dewpointc', 'dewpointinc', 'ip_address', 'ws90cap_volt', 'ws90_ver', 'wh90batt',  'model']

    for field in capture_fields:
        if field in data.keys():
            to_be_saved_data[field] = data[field]
    
    timestr = time.strftime("%Y%m%d.csv")
    my_file = Path(path + '/' + timestr)
    print(to_be_saved_data)

    if my_file.is_file():
        with open(my_file, 'a') as csvfile:
            writer = csv.DictWriter(
                csvfile, fieldnames=to_be_saved_data.keys(), lineterminator="\n")
            writer.writerow(to_be_saved_data)
            csvfile.close()
    else:
        with open(my_file, 'w') as csvfile:
            writer = csv.DictWriter(
                csvfile, fieldnames=to_be_saved_data.keys(), lineterminator="\n")
            writer.writeheader()
            writer.writerow(to_be_saved_data)
            csvfile.close()

if __name__ == "__main__":
    if len(sys.argv) < 2:
        usage()
        exit(1)

    print("Firing up webserver to listen on port {0}".format(sys.argv[1]))
    ws = ecowitt.EcoWittListener(port=sys.argv[1])
    ws.path = sys.argv[2]
    Path(ws.path).mkdir(parents=True, exist_ok=True)
    ws.register_listener(my_handler)
    try:
        # asyncio.run(ws.start())
        ws.start()
    except Exception as e:
        print(str(e))
    print("Exiting")
    exit(0)
