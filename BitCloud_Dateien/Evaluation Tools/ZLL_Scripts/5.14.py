"""
@testcase
@description 5.14 TP-LLI-TC-13: Steal and steal back scenario

@tags
  POSITIVE

@connection dummyPort = router
"""
#*****************************************************************************************
# Import section
#*****************************************************************************************
import sys
sys.path.append(scriptPath)
from common import *
from deviceScanner import *
from onOffCluster import *
from identifyCluster import *
from basicCluster import *
sys.path.remove(scriptPath)

#*****************************************************************************************
# Initialization
#*****************************************************************************************\
portList = []

configureCommunication()
  
V1RC1 = deviceScannerGetAssociatedPort(TEST_DEVICE_TYPE_END_DEVICE, portList)
V2RC1 = deviceScannerGetAssociatedPort(TEST_DEVICE_TYPE_END_DEVICE, portList)
V1L1 = deviceScannerGetAssociatedPort(TEST_DEVICE_TYPE_ROUTER, portList)
V1L2 = deviceScannerGetAssociatedPort(TEST_DEVICE_TYPE_ROUTER, portList)
V2L1 = deviceScannerGetAssociatedPort(TEST_DEVICE_TYPE_ROUTER, portList)
V2L2 = deviceScannerGetAssociatedPort(TEST_DEVICE_TYPE_ROUTER, portList)

#*****************************************************************************************
# Test preparation
#*****************************************************************************************\
writeLog("Item 1a: Power on V1RC1 and V1L1. (Reset device to FN)")
resetEndDeviceToFN([V1RC1])
resetRouterToFN([V1L1])

writeLog("Item 1b: With V1RC1 held close to V1L1, user initiates a touchlink command on V1RC1. \
         Touchlink should succeed.")
touchlink(V1RC1, V1L1)
idle([V1RC1, V1L1])
V1L1NwkAddr = getNwkAddress(V1L1)
writeLog("V1L1 network address - 0x%04X" % V1L1NwkAddr)

writeLog("Item 2a: Power on V2L1. (Reset device to FN)")
resetRouterToFN([V2L1])

writeLog("Item 2b: With V1RC1 held close to V2L1, user initiates a touchlink command on V1RC1. \
         Touchlink should succeed.")
touchlink(V1RC1, V2L1)
idle([V1RC1, V2L1])
V2L1NwkAddr = getNwkAddress(V2L1)
writeLog("V2L1 network address - 0x%04X" % V2L1NwkAddr)

writeLog("Item 3a: User initiates a read attribute request command frame on V1RC1 to V1L1 for \
         the ZCLVersion attribute of the basic cluster.")
setAddressing(V1RC1, APS_SHORT_ADDRESS, V1L1NwkAddr, APP_ENDPOINT_LIGHT)
check(readBasicClusterAttribute(V1RC1, ZCL_BASIC_CLUSTER_SERVER_ZCL_VERSION_ATTRIBUTE_ID) == 0x01)

writeLog("Item 3b: User initiates a lighting control command on V1RC1 to V1L1.")
sendToggleCommand(V1RC1)
receiveToggleCommand(V1L1)

writeLog("Item 4a: User initiates a read attribute request command frame on V1RC1 to V2L1 for \
         the ZCLVersion attribute of the basic cluster.")
setAddressing(V1RC1, APS_SHORT_ADDRESS, V2L1NwkAddr, APP_ENDPOINT_LIGHT)
check(readBasicClusterAttribute(V1RC1, ZCL_BASIC_CLUSTER_SERVER_ZCL_VERSION_ATTRIBUTE_ID) == 0x01)

writeLog("Item 4b: User initiates a lighting control command on V1RC1 to V1L2 \
         (different to that selected for V1L1, if possible).")
sendToggleCommand(V1RC1)
receiveToggleCommand(V2L1)

writeLog("Item 5a: Power on V2RC1 and V1L2. (Reset device to FN)")
resetEndDeviceToFN([V2RC1])
resetRouterToFN([V1L2])

writeLog("Item 5b: With V2RC1 held close to V1L2, user initiates a touchlink command on V2RC1. \
         Touchlink should succeed.")
touchlink(V2RC1, V1L2)
idle([V2RC1, V1L2])
V1L2NwkAddr = getNwkAddress(V1L2)
writeLog("V1L2 network address - 0x%04X" % V1L2NwkAddr)

writeLog("Item 6a: Power on V2L2. (Reset device to FN)")
resetRouterToFN([V2L2])

writeLog("Item 6b: With V2RC1 held close to V2L2, user initiates a touchlink command on V1RC1. \
         Touchlink should succeed.")
touchlink(V2RC1, V2L2)
idle([V2RC1, V2L2])
V2L2NwkAddr = getNwkAddress(V2L2)
writeLog("V2L2 network address - 0x%04X" % V2L2NwkAddr)

writeLog("Item 7a: User initiates a read attribute request command frame on V2RC1 to V1L2 for \
         the ZCLVersion attribute of the basic cluster.")
setAddressing(V2RC1, APS_SHORT_ADDRESS, V1L2NwkAddr, APP_ENDPOINT_LIGHT)
check(readBasicClusterAttribute(V2RC1, ZCL_BASIC_CLUSTER_SERVER_ZCL_VERSION_ATTRIBUTE_ID) == 0x01)

writeLog("Item 7b: User initiates a lighting control command on V2RC1 to V1L2.")
sendToggleCommand(V2RC1)
receiveToggleCommand(V1L2)

writeLog("Item 8a: User initiates a read attribute request command frame on V1RC1 to V2L2 for \
         the ZCLVersion attribute of the basic cluster.")
setAddressing(V2RC1, APS_SHORT_ADDRESS, V2L2NwkAddr, APP_ENDPOINT_LIGHT)
check(readBasicClusterAttribute(V2RC1, ZCL_BASIC_CLUSTER_SERVER_ZCL_VERSION_ATTRIBUTE_ID) == 0x01)

writeLog("Item 8b: User initiates a lighting control command on V1RC1 to V2L2.")
sendToggleCommand(V2RC1)
receiveToggleCommand(V2L2)

writeLog("Item 9: Power off V2L2.")
sleep(1)
powerOff([V2L2])

writeLog("Item 10: With V1RC1 held close to V1L2, user initiates a touchlink command \
         on V1RC1. Touchlink should succeed.")
touchlink(V1RC1, V1L2)
idle([V1RC1, V1L2])
V1L2NwkAddr = getNwkAddress(V1L2)
writeLog("V1L2 network address - 0x%04X" % V1L2NwkAddr)

writeLog("Item 11a: User initiates a read attribute request command frame on V1RC1 to V1L1 for \
         the ZCLVersion attribute of the basic cluster.")
setAddressing(V1RC1, APS_SHORT_ADDRESS, V1L1NwkAddr, APP_ENDPOINT_LIGHT)
check(readBasicClusterAttribute(V1RC1, ZCL_BASIC_CLUSTER_SERVER_ZCL_VERSION_ATTRIBUTE_ID) == 0x01)

writeLog("Item 11b: User initiates a lighting control command on V1RC1 to V1L1.")
sendToggleCommand(V1RC1)
receiveToggleCommand(V1L1)

writeLog("Item 12a: User initiates a read attribute request command frame on V1RC1 to V2L1 for \
         the ZCLVersion attribute of the basic cluster.")
setAddressing(V1RC1, APS_SHORT_ADDRESS, V2L1NwkAddr, APP_ENDPOINT_LIGHT)
check(readBasicClusterAttribute(V1RC1, ZCL_BASIC_CLUSTER_SERVER_ZCL_VERSION_ATTRIBUTE_ID) == 0x01)

writeLog("Item 12b: User initiates a lighting control command on V1RC1 to V1L2 \
         (different to that selected for V1L1, if possible).")
sendToggleCommand(V1RC1)
receiveToggleCommand(V2L1)

writeLog("Item 13a: User initiates a read attribute request command frame on V1RC1 to V1L2 for \
         the ZCLVersion attribute of the basic cluster.")
setAddressing(V1RC1, APS_SHORT_ADDRESS, V1L2NwkAddr, APP_ENDPOINT_LIGHT)
check(readBasicClusterAttribute(V1RC1, ZCL_BASIC_CLUSTER_SERVER_ZCL_VERSION_ATTRIBUTE_ID) == 0x01)

writeLog("Item 13b: User initiates a lighting control command on V1RC1 to V1L2.")
sendToggleCommand(V1RC1)
receiveToggleCommand(V1L2)

writeLog("Item 14: User initiates a read attribute request command frame on V2RC1 to V1L2 for \
         the ZCLVersion attribute of the basic cluster.")
setAddressing(V2RC1, APS_SHORT_ADDRESS, V1L2NwkAddr, APP_ENDPOINT_LIGHT)
readBasicClusterAttribute(V2RC1, ZCL_BASIC_CLUSTER_SERVER_ZCL_VERSION_ATTRIBUTE_ID, BC_DISCONNECTED_STATUS)
receiveAndCheck(V2RC1, zclConfirmStr % ZDO_FAIL_STATUS)
idle([V2RC1, V1L2])

writeLog("Item 15: User initiates a read attribute request command frame on V2RC1 to V2L2 for \
         the ZCLVersion attribute of the basic cluster.")
setAddressing(V2RC1, APS_SHORT_ADDRESS, V2L2NwkAddr, APP_ENDPOINT_LIGHT)
sendCommand(V2RC1, readBasicClusterAttrCmd % ZCL_BASIC_CLUSTER_SERVER_ZCL_VERSION_ATTRIBUTE_ID)
receiveAndCheck(V2RC1, zclConfirmStr % ZDO_FAIL_STATUS)
idle([V2RC1, V2L2])

writeLog("Item 16a: Power on V2L2.")
powerOn([V2L2])

writeLog("Item 16b: Power off V1L1.")
powerOff([V1L1])

writeLog("Item 17: With V2RC1 held close to V2L1, user initiates a touchlink command on V2RC1. \
         Touchlink should succeed.")
touchlink(V2RC1, V2L1)
receiveAndCheck(V2RC1, connectedStr)
idle([V2RC1, V2L1])
prevV2L1NwkAddr = V2L1NwkAddr
V2L1NwkAddr = getNwkAddress(V2L1)
writeLog("V2L1 network address - 0x%04X" % V2L1NwkAddr)

writeLog("Item 18: User initiates a read attribute request command frame on V1RC1 to V11 for \
         the ZCLVersion attribute of the basic cluster.")
setAddressing(V1RC1, APS_SHORT_ADDRESS, V1L1NwkAddr, APP_ENDPOINT_LIGHT)
readBasicClusterAttribute(V1RC1, ZCL_BASIC_CLUSTER_SERVER_ZCL_VERSION_ATTRIBUTE_ID, BC_DISCONNECTED_STATUS)
receiveAndCheck(V1RC1, connectedStr)
receiveAndCheck(V1RC1, zclRespReceivedIndStr % ZCL_NO_RESPONSE_ERROR_STATUS)
idle([V1RC1, V1L1])

writeLog("Item 19: User initiates a read attribute request command frame on V1RC1 to V2L1 for \
         the ZCLVersion attribute of the basic cluster.")
setAddressing(V1RC1, APS_SHORT_ADDRESS, prevV2L1NwkAddr, APP_ENDPOINT_LIGHT)
sendCommand(V1RC1, readBasicClusterAttrCmd % ZCL_BASIC_CLUSTER_SERVER_ZCL_VERSION_ATTRIBUTE_ID)
receiveAndCheck(V1RC1, zclRespReceivedIndStr % ZCL_NO_RESPONSE_ERROR_STATUS)
idle([V1RC1, V2L1])

writeLog("Item 20a: User initiates a read attribute request command frame on V1RC1 to V1L2 for \
         the ZCLVersion attribute of the basic cluster.")
setAddressing(V1RC1, APS_SHORT_ADDRESS, V1L2NwkAddr, APP_ENDPOINT_LIGHT)
check(readBasicClusterAttribute(V1RC1, ZCL_BASIC_CLUSTER_SERVER_ZCL_VERSION_ATTRIBUTE_ID) == 0x01)

writeLog("Item 20b: User initiates a lighting control command on V1RC1 to V1L2.")
sendToggleCommand(V1RC1)
receiveToggleCommand(V1L2)
sleep(1)

writeLog("Item 21: User initiates a read attribute request command frame on V2RC1 to V1L2 for \
         the ZCLVersion attribute of the basic cluster.")
V1L2ExtAddr = getExtAddr(V1L2)
setAddressing(V2RC1, APS_EXT_ADDRESS, V1L2ExtAddr, APP_ENDPOINT_LIGHT)
sendCommand(V2RC1, readBasicClusterAttrCmd % ZCL_BASIC_CLUSTER_SERVER_ZCL_VERSION_ATTRIBUTE_ID)
receiveAndCheck(V2RC1, zclConfirmStr % APS_NO_SHORT_ADDRESS_STATUS)
idle([V2RC1, V1L2])

writeLog("Item 22a: User initiates a read attribute request command frame on V2RC1 to V2L2 for \
         the ZCLVersion attribute of the basic cluster.")
setAddressing(V2RC1, APS_SHORT_ADDRESS, V2L2NwkAddr, APP_ENDPOINT_LIGHT)
check(readBasicClusterAttribute(V2RC1, ZCL_BASIC_CLUSTER_SERVER_ZCL_VERSION_ATTRIBUTE_ID) == 0x01)

writeLog("Item 22b: User initiates a lighting control command on V2RC1 to V2L2.")
sendToggleCommand(V2RC1)
receiveToggleCommand(V2L2)

writeLog("Item 23a: User initiates a read attribute request command frame on V2RC1 to V2L1 for \
         the ZCLVersion attribute of the basic cluster.")
setAddressing(V2RC1, APS_SHORT_ADDRESS, V2L1NwkAddr, APP_ENDPOINT_LIGHT)
check(readBasicClusterAttribute(V2RC1, ZCL_BASIC_CLUSTER_SERVER_ZCL_VERSION_ATTRIBUTE_ID) == 0x01)

writeLog("Item 23b: User initiates a lighting control command on V2RC1 to V2L1.")
sendToggleCommand(V2RC1)
receiveToggleCommand(V2L1)

writeLog("Item 24: Power on V1L1.")
powerOn([V1L1])

writeLog("Item 25: With V1RC1 held close to V2L1, user initiates a touchlink command \
         on V1RC1. Touchlink should succeed.")
touchlink(V1RC1, V2L1)
idle([V1RC1, V2L1])
prevV2L1NwkAddr = V2L1NwkAddr
V2L1NwkAddr = getNwkAddress(V2L1)
writeLog("V2L1 network address - 0x%04X" % V2L1NwkAddr)
sendCommand(V2RC1, restartActivityCmd)
try:
  receiveAndCheck(V2RC1, disconnectedStr)
  receiveAndCheck(V2RC1, connectedStr)
except:
  pass

writeLog("Item 26: With V2RC1 held close to V1L2, user initiates a touchlink command \
         on V2RC1. Touchlink should succeed.")
touchlink(V2RC1, V1L2)
idle([V2RC1, V1L2])
prevV1L2NwkAddr = V1L2NwkAddr
V1L2NwkAddr = getNwkAddress(V1L2)
writeLog("V1L2 network address - 0x%04X" % V1L2NwkAddr)

writeLog("Item 27a: User initiates a read attribute request command frame on V1RC1 to V1L1 for \
         the ZCLVersion attribute of the basic cluster.")
setAddressing(V1RC1, APS_SHORT_ADDRESS, V1L1NwkAddr, APP_ENDPOINT_LIGHT)
readBasicClusterAttribute(V1RC1, ZCL_BASIC_CLUSTER_SERVER_ZCL_VERSION_ATTRIBUTE_ID, BC_DISCONNECTED_RECONNECTED_SUCCESS_STATUS)
idle([V1RC1, V1L1])

writeLog("Item 27b: User initiates a lighting control command on V2RC1 to V2L1.")
sendToggleCommand(V1RC1)
receiveToggleCommand(V1L1)

writeLog("Item 28a: User initiates a read attribute request command frame on V1RC1 to V2L1 for \
         the ZCLVersion attribute of the basic cluster.")
setAddressing(V1RC1, APS_SHORT_ADDRESS, V2L1NwkAddr, APP_ENDPOINT_LIGHT)
check(readBasicClusterAttribute(V1RC1, ZCL_BASIC_CLUSTER_SERVER_ZCL_VERSION_ATTRIBUTE_ID) == 0x01)

writeLog("Item 28b: User initiates a lighting control command on V1RC1 to V2L1.")
sendToggleCommand(V1RC1)
receiveToggleCommand(V2L1)

writeLog("Item 29: User initiates a read attribute request command frame on V1RC1 to V1L2 for \
         the ZCLVersion attribute of the basic cluster.")
setAddressing(V1RC1, APS_SHORT_ADDRESS, prevV1L2NwkAddr, APP_ENDPOINT_LIGHT)
sendCommand(V1RC1, readBasicClusterAttrCmd % ZCL_BASIC_CLUSTER_SERVER_ZCL_VERSION_ATTRIBUTE_ID)
receiveAndCheck(V1RC1, zclRespReceivedIndStr % ZCL_NO_RESPONSE_ERROR_STATUS)
idle([V1RC1, V1L2])

writeLog("Item 30a: User initiates a read attribute request command frame on V2RC1 to V1L2 for \
         the ZCLVersion attribute of the basic cluster.")
setAddressing(V2RC1, APS_SHORT_ADDRESS, V1L2NwkAddr, APP_ENDPOINT_LIGHT)
check(readBasicClusterAttribute(V2RC1, ZCL_BASIC_CLUSTER_SERVER_ZCL_VERSION_ATTRIBUTE_ID) == 0x01)

writeLog("Item 30b: User initiates a lighting control command on V2RC1 to V1L2.")
sendToggleCommand(V2RC1)
receiveToggleCommand(V1L2)

writeLog("Item 31a: User initiates a read attribute request command frame on V2RC1 to V2L2 for \
         the ZCLVersion attribute of the basic cluster.")
setAddressing(V2RC1, APS_SHORT_ADDRESS, V2L2NwkAddr, APP_ENDPOINT_LIGHT)
check(readBasicClusterAttribute(V2RC1, ZCL_BASIC_CLUSTER_SERVER_ZCL_VERSION_ATTRIBUTE_ID) == 0x01)

writeLog("Item 31b: User initiates a lighting control command on V2RC1 to V2L2.")
sendToggleCommand(V2RC1)
receiveToggleCommand(V2L2)

writeLog("Item 32: User initiates a read attribute request command frame on V2RC1 to V2L1 for \
         the ZCLVersion attribute of the basic cluster.")
setAddressing(V2RC1, APS_SHORT_ADDRESS, prevV2L1NwkAddr, APP_ENDPOINT_LIGHT)
sendCommand(V2RC1, readBasicClusterAttrCmd % ZCL_BASIC_CLUSTER_SERVER_ZCL_VERSION_ATTRIBUTE_ID)
receiveAndCheck(V2RC1, zclRespReceivedIndStr % ZCL_NO_RESPONSE_ERROR_STATUS)
idle([V2RC1, V2L1])

idle([V1RC1, V2RC1, V1L1, V1L2, V2L1, V2L2])
