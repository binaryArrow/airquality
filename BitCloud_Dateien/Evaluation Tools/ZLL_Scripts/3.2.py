"""
@testcase
@description 3.2 TP-CST-TC-02: On/off cluster with client as DUT

@tags
  POSITIVE

@connection dummyPort = router
"""

#*****************************************************************************************
#Defines section
#*****************************************************************************************
import sys
sys.path.append(scriptPath)
from common import *
from deviceScanner import *
from onOffCluster import *
from sceneCluster import *
from levelControlCluster import *
sys.path.remove(scriptPath)

#*****************************************************************************************
# Initialization
#*****************************************************************************************\
portList = []

configureCommunication()

client1 = deviceScannerGetAssociatedPort(TEST_DEVICE_TYPE_END_DEVICE, portList)
server1 = deviceScannerGetAssociatedPort(TEST_DEVICE_TYPE_ROUTER, portList)

#*****************************************************************************************
# Test preparation
#*****************************************************************************************\
resetRouterToFN([server1])
resetEndDeviceToFN([client1])
clearPorts([server1, client1])
powerOff([server1, client1])

client1ExtAddr = getExtAddr(client1)
writeLog("ED1 extended address - %016X" % client1ExtAddr)

server1ExtAddr = getExtAddr(server1)
writeLog("R1 extended address - %016X" % server1ExtAddr)

writeLog("P1 Power on client and server")
powerOn([client1, server1])

writeLog("P2 Touchlink client and server")
touchlink(client1, server1)
idle([client1, server1])

server1NwkAddr = getNwkAddress(server1)
writeLog("R1 network address - 0x%04X" % server1NwkAddr)

client1NwkAddr = getNwkAddress(client1)
writeLog("ED1 network address - 0x%04X" % client1NwkAddr)

writeLog("Set addressing on client")
setAddressing(client1, APS_SHORT_ADDRESS, server1NwkAddr, APP_ENDPOINT_LIGHT)

#*****************************************************************************************
# Test body
#*****************************************************************************************\
writeLog("1 Client sends on command")
sendOnCommand(client1) 
receiveOnCommand(server1)

writeLog("2 Client sends off command")
sendOffCommand(client1) 
receiveOffCommand(server1)

writeLog("3 Client sends toggle command")
sendToggleCommand(client1) 
receiveToggleCommand(server1)

writeLog("4 Client sends read attribute command")
check(readOnOffClusterAttribute(client1, ZCL_ONOFF_CLUSTER_ONOFF_SERVER_ATTRIBUTE_ID) == 1)

writeLog("5 Client sends toggle command")
sendToggleCommand(client1) 
receiveToggleCommand(server1)

writeLog("6 Client sends read attribute command")
check(readOnOffClusterAttribute(client1, ZCL_ONOFF_CLUSTER_ONOFF_SERVER_ATTRIBUTE_ID) == 0)

writeLog("7 Client sends off with effect command")
sendOffWithEffectCmd(client1, 0x00, 0x00)

writeLog("8 Client sends on with recall global scene command")
sendOnWithRecallCommand(client1)

writeLog("9 Client sends on with timed off with \'accept only if on\' condition")
sendOnWithTimedOffCmd(client1, 1, 300, 300)
