from pycomm3 import LogixDriver
import time
import csv

with open("output.csv", mode="w", newline="") as file:
    with LogixDriver('192.168.1.5/0') as plc:
        tags = 'SW0_State', 'Temp', 'PID.SP', 'PID.ERR', 'PID.KP', 'PID.KI', 'PID.KD', 'PID.OUT'
        values = []
        dict = dict.fromkeys({x: x for x in tags}, [])
        print(dict)
        writer = csv.DictWriter(file, dict.keys())
        writer.writeheader()

        while True:
            res = plc.read('SW0_State', 'Temp', 'PID.SP', 'PID.ERR', 'PID.KP', 'PID.KI', 'PID.KD', 'PID.OUT')
            for i in range (0, len(res)):
                dict[res[i].tag] = res[i].value
            time.sleep(0.1)
            writer.writerow(dict)
            print(dict)

