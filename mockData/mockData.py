import serial
import json
import time

# Ein Virtuelles Port Pair erstellen (z.B. COM10 & COM11 mit com0com oder ähnlichem Programm) und dann auf Port COM11 mit PuTTY empfangen (von COM10 wird gesendet)

s = serial.Serial("COM10", 9600)  # Port, Baudrate

# datensätze für Funkmodul 1
jsonData1 = {"id": 1}
Sensor1 = {}
Sensor2 = {}
Sensor3 = {}

jsonData2 = {"id": 2}
Sensor1_2 = {}
Sensor2_2 = {}
Sensor3_2 = {}

jsonData3 = {"id": 3}
Sensor1_3 = {}
Sensor2_3 = {}
Sensor3_3 = {}

for i in range(1, 11):
    Sensor1['temperature'] = i+10
    Sensor1['humidity'] = i+20
    Sensor2['TVOC'] = i+30
    Sensor2['ECO2'] = i+40
    Sensor3['humidity'] = i+50
    Sensor3['temperature'] = i+60
    Sensor3['CO2'] = i+70
    jsonData1['SHT21'] = Sensor1
    jsonData1['CCS811'] = Sensor2
    jsonData1['SCD41'] = Sensor3
    jsonStr1 = json.dumps(jsonData1)
    print(jsonStr1)
    s.write(jsonStr1.encode('utf-8'))
    time.sleep(10)

for i in range(1, 11):
    Sensor1_2['temperature'] = i+11
    Sensor1_2['humidity'] = i+21
    Sensor2_2['TVOC'] = i+31
    Sensor2_2['ECO2'] = i+41
    Sensor3_2['humidity'] = i+51
    Sensor3_2['temperature'] = i+61
    Sensor3_2['CO2'] = i+71
    jsonData2['SHT21'] = Sensor1_2
    jsonData2['CCS811'] = Sensor2_2
    jsonData2['SCD41'] = Sensor3_2
    jsonStr2 = json.dumps(jsonData2)
    print(jsonStr2)
    s.write(jsonStr2.encode('utf-8'))
    time.sleep(10)

for i in range(1, 11):
    Sensor1_3['temperature'] = i+12
    Sensor1_3['humidity'] = i+22
    Sensor2_3['TVOC'] = i+32
    Sensor2_3['ECO2'] = i+42
    Sensor3_3['humidity'] = i+52
    Sensor3_3['temperature'] = i+62
    Sensor3_3['CO2'] = i+72
    jsonData3['SHT21'] = Sensor1_3
    jsonData3['CCS811'] = Sensor2_3
    jsonData3['SCD41'] = Sensor3_3
    jsonStr3 = json.dumps(jsonData3)
    print(jsonStr3)
    s.write(jsonStr3.encode('utf-8'))
    time.sleep(10)


