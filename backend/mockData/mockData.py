import serial
import json
import time

# Ein Virtuelles Port Pair erstellen (z.B. COM10 & COM11 mit com0com oder ähnlichem Programm) und dann auf Port COM11 mit PuTTY empfangen (von COM10 wird gesendet)

s = serial.Serial("COM10", 9600)  # Port, Baudrate

class dataSet:
    def __init__(self, id, sensor1, sensor2, sensor3):
        self.id = id
        self.sensor1 = sensor1
        self.sensor2 = sensor2
        self.sensor3 = sensor3


# datensätze für Funkmodul 1
data1 = list()
data2 = list()
data3 = list()

for i in range(1, 11):
    data1.append(dataSet(1, i + 10, i + 15, i + 20))

# datensätze für Funkmodul 2
for i in range(1, 11):
    data2.append(dataSet(2, i + 11, i + 16, i + 21))

# datensätze für Funkmodul 3
for i in range(1, 11):
    data3.append(dataSet(3, i + 12, i + 17, i + 22))

# Daten in JSON string umwandeln und printen

print("Daten von Funkmodul 1: ")
for dataSet in data1:
    jsonStr = json.dumps(dataSet.__dict__)
    print(jsonStr)
    s.write(jsonStr.encode('utf-8'))
    time.sleep(2)

print("Daten von Funkmodul 2: ")
for dataSet in data2:
    jsonStr = json.dumps(dataSet.__dict__)
    print(jsonStr)
    s.write(jsonStr.encode('utf-8'))
    time.sleep(2)

print("Daten von Funkmodul 3: ")
for dataSet in data3:
    jsonStr = json.dumps(dataSet.__dict__)
    print(jsonStr)
    s.write(jsonStr.encode('utf-8'))
    time.sleep(2)

# data=[
#   {
#        "id": 1,
#        "dataSensor1": {
#            "temp": 20,
#            "LF":   30
#        },
#        "dataSensor2": 20,
#        "dataSensor3": 30
#    },
#    {
#        "id": 2,
#        "dataSensor1": {
#            "temp": 24,
#            "LF":   52
#        },
#        "dataSensor2": 21,
#        "dataSensor3": 35
#    },
#    {
#        "id": 3,
#        "dataSensor1": {
#            "temp": 40,
#            "LF":   26
#        },
#        "dataSensor2": 26,
#        "dataSensor3": 30
#    }
# ]
