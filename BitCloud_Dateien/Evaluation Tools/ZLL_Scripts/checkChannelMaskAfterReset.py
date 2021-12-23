"""
@testcase
@description

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
from levelControlCluster import *
sys.path.remove(scriptPath)

#*****************************************************************************************
# Initialization
#*****************************************************************************************\
portList = []
prChannelMask = 0x1800

configureCommunication()

ed1 = deviceScannerGetAssociatedPort(TEST_DEVICE_TYPE_END_DEVICE, portList)
r1 = deviceScannerGetAssociatedPort(TEST_DEVICE_TYPE_ROUTER, portList)

#*****************************************************************************************
#Script body - feature checking
#*****************************************************************************************
writeLog("1 Resetting nodes to FN")
resetRouterToFN([r1])
resetEndDeviceToFN([ed1])
clearPorts([r1, ed1])

writeLog("2 Setting channel masks")
setPrimaryChannelMask([r1], prChannelMask)
setSecondaryChannelMask([r1], 0x8000)
setPrimaryChannelMask([ed1], prChannelMask)
setSecondaryChannelMask([ed1], 0x8000)

writeLog("3 R1 creates network")
joinNetwork(r1, 1, 11, 1, 1, 1)
setPermitJoinReq(r1, 0xFF)
receiveSetPermitJoinResp(r1, BC_SUCCESS_STATUS)

writeLog("4 ED1 joins network via association")
nwkAssociation(ed1, BC_SUCCESS_STATUS, BC_SUCCESS_STATUS)

writeLog("5 ED1 sends ZCL command to R1")
sendSimpleLevelControlCommand(ed1, ZCL_LEVEL_CONTROL_CLUSTER_STOP_COMMAND_ID)

writeLog("6 Reset R1 to FN")
resetRouterToFN([r1])

writeLog("7 Reset ED1")
resetEndDevice([ed1])

writeLog("8 ED1 tries to send ZCL command to R1")
sendCommand(ed1, levelControlCmd % ZCL_LEVEL_CONTROL_CLUSTER_STOP_COMMAND_ID)
receiveAndCheck(ed1, "Disconnected")

writeLog("9 Check ED1 channel mask")
sendCommand(ed1, "getCsChannelMask")
buffer = receiveNextStr(ed1)
chMask = int(buffer, 16)
check(prChannelMask == chMask)