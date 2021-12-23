"""
@testcase
@description 5.12 TP-LLI-TC-11: Single remote, multi vendor

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
V1L1 = deviceScannerGetAssociatedPort(TEST_DEVICE_TYPE_ROUTER, portList)
V1L2 = deviceScannerGetAssociatedPort(TEST_DEVICE_TYPE_ROUTER, portList)
V2L1 = deviceScannerGetAssociatedPort(TEST_DEVICE_TYPE_ROUTER, portList)
V2L2 = deviceScannerGetAssociatedPort(TEST_DEVICE_TYPE_ROUTER, portList)
V3L1 = deviceScannerGetAssociatedPort(TEST_DEVICE_TYPE_ROUTER, portList)
V3L2 = deviceScannerGetAssociatedPort(TEST_DEVICE_TYPE_ROUTER, portList)

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

writeLog("Item 2a: Power on V1L2. (Reset device to FN)")
resetRouterToFN([V1L2])

writeLog("Item 2b: With V1RC1 held close to V1L2, user initiates a touchlink command on V1RC1. \
         Touchlink should succeed.")
touchlink(V1RC1, V1L2)
idle([V1RC1, V1L2])
V1L2NwkAddr = getNwkAddress(V1L2)
writeLog("V1L2 network address - 0x%04X" % V1L2NwkAddr)

writeLog("Item 3a: User initiates a read attribute request command frame on V1RC1 to V1L1 for \
         the ZCLVersion attribute of the basic cluster.")
setAddressing(V1RC1, APS_SHORT_ADDRESS, V1L1NwkAddr, APP_ENDPOINT_LIGHT)
check(readBasicClusterAttribute(V1RC1, ZCL_BASIC_CLUSTER_SERVER_ZCL_VERSION_ATTRIBUTE_ID) == 0x01)

writeLog("Item 3b: User initiates a lighting control command on V1RC1 to V1L1.")
sendOnCommand(V1RC1)
receiveOnCommand(V1L1)

writeLog("Item 4a: User initiates a read attribute request command frame on V1RC1 to V1L2 for \
         the ZCLVersion attribute of the basic cluster.")
setAddressing(V1RC1, APS_SHORT_ADDRESS, V1L2NwkAddr, APP_ENDPOINT_LIGHT)
check(readBasicClusterAttribute(V1RC1, ZCL_BASIC_CLUSTER_SERVER_ZCL_VERSION_ATTRIBUTE_ID) == 0x01)

writeLog("Item 4b: User initiates a lighting control command on V1RC1 to V1L2 \
         (different to that selected for V1L1, if possible).")
sendToggleCommand(V1RC1)
receiveToggleCommand(V1L2)

writeLog("Item 5a: Power on V2L1 and V2L2. (Reset device to FN)")
resetRouterToFN([V2L1, V2L2])

writeLog("Item 5b: With V1RC1 held close to V2L1, user initiates a touchlink command on V1RC1. \
         Touchlink should succeed.")
touchlink(V1RC1, V2L1)
idle([V1RC1, V2L1])
V2L1NwkAddr = getNwkAddress(V2L1)
writeLog("V2L1 network address - 0x%04X" % V2L1NwkAddr)

writeLog("Item 5c: With V1RC1 held close to V2L2, user initiates a touchlink command on V1RC1. \
         Touchlink should succeed.")
touchlink(V1RC1, V2L2)
idle([V1RC1, V2L2])
V2L2NwkAddr = getNwkAddress(V2L2)
writeLog("V2L2 network address - 0x%04X" % V2L2NwkAddr)

writeLog("Item 6a: User initiates a read attribute request command frame on V1RC1 to V1L1 for \
         the ZCLVersion attribute of the basic cluster.")
setAddressing(V1RC1, APS_SHORT_ADDRESS, V1L1NwkAddr, APP_ENDPOINT_LIGHT)
check(readBasicClusterAttribute(V1RC1, ZCL_BASIC_CLUSTER_SERVER_ZCL_VERSION_ATTRIBUTE_ID) == 0x01)

writeLog("Item 6b: User initiates a lighting control command on V1RC1 to V1L1 \
         (different to its current state).")
sendOffCommand(V1RC1)
receiveOffCommand(V1L1)

writeLog("Item 7a: User initiates a read attribute request command frame on V1RC1 to V1L2 for \
         the ZCLVersion attribute of the basic cluster.")
setAddressing(V1RC1, APS_SHORT_ADDRESS, V1L2NwkAddr, APP_ENDPOINT_LIGHT)
check(readBasicClusterAttribute(V1RC1, ZCL_BASIC_CLUSTER_SERVER_ZCL_VERSION_ATTRIBUTE_ID) == 0x01)

writeLog("Item 7b: User initiates a lighting control command on V1RC1 to V1L2 \
         (different to its current state).")
sendToggleCommand(V1RC1)
receiveToggleCommand(V1L2)

writeLog("Item 8a: User initiates a read attribute request command frame on V1RC1 to V2L1 for \
         the ZCLVersion attribute of the basic cluster.")
setAddressing(V1RC1, APS_SHORT_ADDRESS, V2L1NwkAddr, APP_ENDPOINT_LIGHT)
check(readBasicClusterAttribute(V1RC1, ZCL_BASIC_CLUSTER_SERVER_ZCL_VERSION_ATTRIBUTE_ID) == 0x01)

writeLog("Item 8b: User initiates a lighting control command on V1RC1 to V2L1 \
         (different to that selected for V1L1 and V1L2, if possible).")
sendToggleCommand(V1RC1)
receiveToggleCommand(V2L1)

writeLog("Item 9a: User initiates a read attribute request command frame on V1RC1 to \
         V2L2 for the ZCLVersion attribute of the basic cluster.")
setAddressing(V1RC1, APS_SHORT_ADDRESS, V2L2NwkAddr, APP_ENDPOINT_LIGHT)
check(readBasicClusterAttribute(V1RC1, ZCL_BASIC_CLUSTER_SERVER_ZCL_VERSION_ATTRIBUTE_ID) == 0x01)

writeLog("Item 9b: User initiates a lighting control command on V1RC1 to V2L2 \
         (different to that selected for V1L1, V1L2 and V2L1, if possible).")
sendToggleCommand(V1RC1)
receiveToggleCommand(V2L2)

writeLog("Item 10: Power off V1L1 and V1L2.")
powerOff([V1L1, V1L2])

writeLog("Item 11: User initiates a read attribute request command frame on V1RC1 to \
         V1L1 for the ZCLVersion attribute of the basic cluster.")
setAddressing(V1RC1, APS_SHORT_ADDRESS, V1L1NwkAddr, APP_ENDPOINT_LIGHT)
readBasicClusterAttribute(V1RC1, ZCL_BASIC_CLUSTER_SERVER_ZCL_VERSION_ATTRIBUTE_ID, BC_DISCONNECTED_STATUS)
receiveAndCheck(V1RC1, connectedStr)
receiveAndCheck(V1RC1, zclRespReceivedIndStr % ZCL_NO_RESPONSE_ERROR_STATUS)
idle([V1RC1, V1L1])

writeLog("Item 12: User initiates a read attribute request command frame on V1RC1 to V1L2 \
         for the ZCLVersion attribute of the basic cluster.")
setAddressing(V1RC1, APS_SHORT_ADDRESS, V1L2NwkAddr, APP_ENDPOINT_LIGHT)
readBasicClusterAttribute(V1RC1, ZCL_BASIC_CLUSTER_SERVER_ZCL_VERSION_ATTRIBUTE_ID, ZCL_NO_RESPONSE_ERROR_STATUS)

writeLog("Item 13a: User initiates a read attribute request command frame on V1RC1 to V2L1 for \
         the ZCLVersion attribute of the basic cluster.")
setAddressing(V1RC1, APS_SHORT_ADDRESS, V2L1NwkAddr, APP_ENDPOINT_LIGHT)
check(readBasicClusterAttribute(V1RC1, ZCL_BASIC_CLUSTER_SERVER_ZCL_VERSION_ATTRIBUTE_ID) == 0x01)

writeLog("Item 13b: User initiates a lighting control command on V1RC1 to V2L1 \
         (different to that selected for V1L1 and V1L2, if possible).")
sendToggleCommand(V1RC1)
receiveToggleCommand(V2L1)

writeLog("Item 14a: User initiates a read attribute request command frame on V1RC1 to \
         V2L2 for the ZCLVersion attribute of the basic cluster.")
setAddressing(V1RC1, APS_SHORT_ADDRESS, V2L2NwkAddr, APP_ENDPOINT_LIGHT)
check(readBasicClusterAttribute(V1RC1, ZCL_BASIC_CLUSTER_SERVER_ZCL_VERSION_ATTRIBUTE_ID) == 0x01)

writeLog("Item 14b: User initiates a lighting control command on V1RC1 to V2L2 \
         (different to that selected for V1L1, V1L2 and V2L1, if possible).")
sendToggleCommand(V1RC1)
receiveToggleCommand(V2L2)

writeLog("Item 15a: Power on V3L1 and V3L2. (Reset device to FN)")
resetRouterToFN([V3L1, V3L2])

writeLog("Item 15b: With V1RC1 held close to V3L1, user initiates a touchlink command on V1RC1. \
         Touchlink should succeed.")
touchlink(V1RC1, V3L1)
idle([V1RC1, V3L1])
V3L1NwkAddr = getNwkAddress(V3L1)
writeLog("V3L1 network address - 0x%04X" % V3L1NwkAddr)

writeLog("Item 15c: With V1RC1 held close to V3L2, user initiates a touchlink command on V1RC1. \
         Touchlink should succeed.")
touchlink(V1RC1, V3L2)
idle([V1RC1, V3L2])
V3L2NwkAddr = getNwkAddress(V3L2)
writeLog("V3L2 network address - 0x%04X" % V3L2NwkAddr)

writeLog("Item 16: User initiates a read attribute request command frame on V1RC1 to V1L1 \
         for the ZCLVersion attribute of the basic cluster.")
setAddressing(V1RC1, APS_SHORT_ADDRESS, V1L1NwkAddr, APP_ENDPOINT_LIGHT)
readBasicClusterAttribute(V1RC1, ZCL_BASIC_CLUSTER_SERVER_ZCL_VERSION_ATTRIBUTE_ID, ZCL_NO_RESPONSE_ERROR_STATUS)

writeLog("Item 17: User initiates a read attribute request command frame on V1RC1 to V1L2 \
         for the ZCLVersion attribute of the basic cluster.")
setAddressing(V1RC1, APS_SHORT_ADDRESS, V1L2NwkAddr, APP_ENDPOINT_LIGHT)
readBasicClusterAttribute(V1RC1, ZCL_BASIC_CLUSTER_SERVER_ZCL_VERSION_ATTRIBUTE_ID, ZCL_NO_RESPONSE_ERROR_STATUS)

writeLog("Item 18a: User initiates a read attribute request command frame on V1RC1 to V2L1 for \
         the ZCLVersion attribute of the basic cluster.")
setAddressing(V1RC1, APS_SHORT_ADDRESS, V2L1NwkAddr, APP_ENDPOINT_LIGHT)
check(readBasicClusterAttribute(V1RC1, ZCL_BASIC_CLUSTER_SERVER_ZCL_VERSION_ATTRIBUTE_ID) == 0x01)

writeLog("Item 18b: User initiates a lighting control command on V1RC1 to V2L1 \
         (different to that selected for V1L1 and V1L2, if possible).")
sendToggleCommand(V1RC1)
receiveToggleCommand(V2L1)

writeLog("Item 19a: User initiates a read attribute request command frame on V1RC1 to \
         V2L2 for the ZCLVersion attribute of the basic cluster.")
setAddressing(V1RC1, APS_SHORT_ADDRESS, V2L2NwkAddr, APP_ENDPOINT_LIGHT)
check(readBasicClusterAttribute(V1RC1, ZCL_BASIC_CLUSTER_SERVER_ZCL_VERSION_ATTRIBUTE_ID) == 0x01)

writeLog("Item 19b: User initiates a lighting control command on V1RC1 to V2L2 \
         (different to that selected for V1L1, V1L2 and V2L1, if possible).")
sendToggleCommand(V1RC1)
receiveToggleCommand(V2L2)

writeLog("Item 20a: User initiates a read attribute request command frame on V1RC1 to V3L1 for \
         the ZCLVersion attribute of the basic cluster.")
setAddressing(V1RC1, APS_SHORT_ADDRESS, V3L1NwkAddr, APP_ENDPOINT_LIGHT)
check(readBasicClusterAttribute(V1RC1, ZCL_BASIC_CLUSTER_SERVER_ZCL_VERSION_ATTRIBUTE_ID) == 0x01)

writeLog("Item 20b: User initiates a lighting control command on V1RC1 to V3L1 \
         (different to that selected for V1L1 and V1L2, if possible).")
sendToggleCommand(V1RC1)
receiveToggleCommand(V3L1)

writeLog("Item 21a: User initiates a read attribute request command frame on V1RC1 to \
         V3L2 for the ZCLVersion attribute of the basic cluster.")
setAddressing(V1RC1, APS_SHORT_ADDRESS, V3L2NwkAddr, APP_ENDPOINT_LIGHT)
check(readBasicClusterAttribute(V1RC1, ZCL_BASIC_CLUSTER_SERVER_ZCL_VERSION_ATTRIBUTE_ID) == 0x01)

writeLog("Item 21b: User initiates a lighting control command on V1RC1 to V3L2 \
         (different to that selected for V1L1, V1L2 and V2L1, if possible).")
sendToggleCommand(V1RC1)
receiveToggleCommand(V3L2)

writeLog("Item 22: Power on V1L1 and V1L2.")
powerOn([V1L1, V1L2])

writeLog("Item 23a: User initiates a read attribute request command frame on V1RC1 to V1L1 for \
         the ZCLVersion attribute of the basic cluster.")
setAddressing(V1RC1, APS_SHORT_ADDRESS, V1L1NwkAddr, APP_ENDPOINT_LIGHT)
check(readBasicClusterAttribute(V1RC1, ZCL_BASIC_CLUSTER_SERVER_ZCL_VERSION_ATTRIBUTE_ID) == 0x01)

writeLog("Item 23b: User initiates a lighting control command on V1RC1 to V1L1 \
         (different to that selected for V1L1 and V1L1, if possible).")
sendToggleCommand(V1RC1)
receiveToggleCommand(V1L1)

writeLog("Item 24a: User initiates a read attribute request command frame on V1RC1 to V1L2 for \
         the ZCLVersion attribute of the basic cluster.")
setAddressing(V1RC1, APS_SHORT_ADDRESS, V1L2NwkAddr, APP_ENDPOINT_LIGHT)
check(readBasicClusterAttribute(V1RC1, ZCL_BASIC_CLUSTER_SERVER_ZCL_VERSION_ATTRIBUTE_ID) == 0x01)

writeLog("Item 24b: User initiates a lighting control command on V1RC1 to V1L2 \
         (different to that selected for V1L1 and V1L2, if possible).")
sendToggleCommand(V1RC1)
receiveToggleCommand(V1L2)

writeLog("Item 25a: User initiates a read attribute request command frame on V1RC1 to V2L1 for \
         the ZCLVersion attribute of the basic cluster.")
setAddressing(V1RC1, APS_SHORT_ADDRESS, V2L1NwkAddr, APP_ENDPOINT_LIGHT)
check(readBasicClusterAttribute(V1RC1, ZCL_BASIC_CLUSTER_SERVER_ZCL_VERSION_ATTRIBUTE_ID) == 0x01)

writeLog("Item 25b: User initiates a lighting control command on V1RC1 to V2L1 \
         (different to that selected for V1L1 and V1L2, if possible).")
sendToggleCommand(V1RC1)
receiveToggleCommand(V2L1)

writeLog("Item 26a: User initiates a read attribute request command frame on V1RC1 to \
         V2L2 for the ZCLVersion attribute of the basic cluster.")
setAddressing(V1RC1, APS_SHORT_ADDRESS, V2L2NwkAddr, APP_ENDPOINT_LIGHT)
check(readBasicClusterAttribute(V1RC1, ZCL_BASIC_CLUSTER_SERVER_ZCL_VERSION_ATTRIBUTE_ID) == 0x01)

writeLog("Item 26b: User initiates a lighting control command on V1RC1 to V2L2 \
         (different to that selected for V1L1, V1L2 and V2L1, if possible).")
sendToggleCommand(V1RC1)
receiveToggleCommand(V2L2)

writeLog("Item 27a: User initiates a read attribute request command frame on V1RC1 to V3L1 for \
         the ZCLVersion attribute of the basic cluster.")
setAddressing(V1RC1, APS_SHORT_ADDRESS, V3L1NwkAddr, APP_ENDPOINT_LIGHT)
check(readBasicClusterAttribute(V1RC1, ZCL_BASIC_CLUSTER_SERVER_ZCL_VERSION_ATTRIBUTE_ID) == 0x01)

writeLog("Item 27b: User initiates a lighting control command on V1RC1 to V3L1 \
         (different to that selected for V1L1 and V1L2, if possible).")
sendToggleCommand(V1RC1)
receiveToggleCommand(V3L1)

writeLog("Item 28a: User initiates a read attribute request command frame on V1RC1 to \
         V3L2 for the ZCLVersion attribute of the basic cluster.")
setAddressing(V1RC1, APS_SHORT_ADDRESS, V3L2NwkAddr, APP_ENDPOINT_LIGHT)
check(readBasicClusterAttribute(V1RC1, ZCL_BASIC_CLUSTER_SERVER_ZCL_VERSION_ATTRIBUTE_ID) == 0x01)

writeLog("Item 28b: User initiates a lighting control command on V1RC1 to V3L2 \
         (different to that selected for V1L1, V1L2 and V2L1, if possible).")
sendToggleCommand(V1RC1)
receiveToggleCommand(V3L2)

writeLog("Item 29: Power off V2L1 and V2L2.")
powerOff([V2L1, V2L2])

writeLog("Item 30a: User initiates a read attribute request command frame on V1RC1 to \
         V1L1 for the ZCLVersion attribute of the basic cluster.")
setAddressing(V1RC1, APS_SHORT_ADDRESS, V1L1NwkAddr, APP_ENDPOINT_LIGHT)
readBasicClusterAttribute(V1RC1, ZCL_BASIC_CLUSTER_SERVER_ZCL_VERSION_ATTRIBUTE_ID, BC_DISCONNECTED_RECONNECTED_SUCCESS_STATUS)
idle([V1RC1, V1L1])

writeLog("Item 30b: User initiates a lighting control command on V1RC1 to V1L1 \
         (different to its current state).")
sendToggleCommand(V1RC1)
receiveToggleCommand(V1L1)

writeLog("Item 31a: User initiates a read attribute request command frame on V1RC1 to V1L2 \
         for the ZCLVersion attribute of the basic cluster.")
setAddressing(V1RC1, APS_SHORT_ADDRESS, V1L2NwkAddr, APP_ENDPOINT_LIGHT)
check(readBasicClusterAttribute(V1RC1, ZCL_BASIC_CLUSTER_SERVER_ZCL_VERSION_ATTRIBUTE_ID) == 0x01)

writeLog("Item 31b: User initiates a lighting control command on V1RC1 to V1L2 \
         (different to its current state).")
sendToggleCommand(V1RC1)
receiveToggleCommand(V1L2)

writeLog("Item 32: User initiates a read attribute request command frame on V1RC1 to \
         V2L1 for the ZCLVersion attribute of the basic cluster.")
setAddressing(V1RC1, APS_SHORT_ADDRESS, V2L1NwkAddr, APP_ENDPOINT_LIGHT)
readBasicClusterAttribute(V1RC1, ZCL_BASIC_CLUSTER_SERVER_ZCL_VERSION_ATTRIBUTE_ID, ZCL_NO_RESPONSE_ERROR_STATUS)

writeLog("Item 33: User initiates a read attribute request command frame on V1RC1 to \
         V2L2 for the ZCLVersion attribute of the basic cluster.")
setAddressing(V1RC1, APS_SHORT_ADDRESS, V2L2NwkAddr, APP_ENDPOINT_LIGHT)
readBasicClusterAttribute(V1RC1, ZCL_BASIC_CLUSTER_SERVER_ZCL_VERSION_ATTRIBUTE_ID, ZCL_NO_RESPONSE_ERROR_STATUS)

writeLog("Item 34a: User initiates a read attribute request command frame on V1RC1 to V3L1 for \
         the ZCLVersion attribute of the basic cluster.")
setAddressing(V1RC1, APS_SHORT_ADDRESS, V3L1NwkAddr, APP_ENDPOINT_LIGHT)
check(readBasicClusterAttribute(V1RC1, ZCL_BASIC_CLUSTER_SERVER_ZCL_VERSION_ATTRIBUTE_ID) == 0x01)

writeLog("Item 34b: User initiates a lighting control command on V1RC1 to V3L1 \
         (different to that selected for V1L1 and V1L2, if possible).")
sendToggleCommand(V1RC1)
receiveToggleCommand(V3L1)

writeLog("Item 35a: User initiates a read attribute request command frame on V1RC1 to \
         V3L2 for the ZCLVersion attribute of the basic cluster.")
setAddressing(V1RC1, APS_SHORT_ADDRESS, V3L2NwkAddr, APP_ENDPOINT_LIGHT)
check(readBasicClusterAttribute(V1RC1, ZCL_BASIC_CLUSTER_SERVER_ZCL_VERSION_ATTRIBUTE_ID) == 0x01)

writeLog("Item 35b: User initiates a lighting control command on V1RC1 to V3L2 \
         (different to that selected for V1L1, V1L2 and V2L1, if possible).")
sendToggleCommand(V1RC1)
receiveToggleCommand(V3L2)

writeLog("Item 36: Power on V2L1 and V2L2.")
powerOn([V2L1, V2L2])

writeLog("Item 37a: User initiates a read attribute request command frame on V1RC1 to V1L1 for \
         the ZCLVersion attribute of the basic cluster.")
setAddressing(V1RC1, APS_SHORT_ADDRESS, V1L1NwkAddr, APP_ENDPOINT_LIGHT)
check(readBasicClusterAttribute(V1RC1, ZCL_BASIC_CLUSTER_SERVER_ZCL_VERSION_ATTRIBUTE_ID) == 0x01)

writeLog("Item 37b: User initiates a lighting control command on V1RC1 to V1L1 \
         (different to that selected for V1L1 and V1L1, if possible).")
sendToggleCommand(V1RC1)
receiveToggleCommand(V1L1)

writeLog("Item 38a: User initiates a read attribute request command frame on V1RC1 to V1L2 for \
         the ZCLVersion attribute of the basic cluster.")
setAddressing(V1RC1, APS_SHORT_ADDRESS, V1L2NwkAddr, APP_ENDPOINT_LIGHT)
check(readBasicClusterAttribute(V1RC1, ZCL_BASIC_CLUSTER_SERVER_ZCL_VERSION_ATTRIBUTE_ID) == 0x01)

writeLog("Item 38b: User initiates a lighting control command on V1RC1 to V1L2 \
         (different to that selected for V1L1 and V1L2, if possible).")
sendToggleCommand(V1RC1)
receiveToggleCommand(V1L2)

writeLog("Item 39a: User initiates a read attribute request command frame on V1RC1 to V2L1 for \
         the ZCLVersion attribute of the basic cluster.")
setAddressing(V1RC1, APS_SHORT_ADDRESS, V2L1NwkAddr, APP_ENDPOINT_LIGHT)
check(readBasicClusterAttribute(V1RC1, ZCL_BASIC_CLUSTER_SERVER_ZCL_VERSION_ATTRIBUTE_ID) == 0x01)

writeLog("Item 39b: User initiates a lighting control command on V1RC1 to V2L1 \
         (different to that selected for V1L1 and V1L2, if possible).")
sendToggleCommand(V1RC1)
receiveToggleCommand(V2L1)

writeLog("Item 40a: User initiates a read attribute request command frame on V1RC1 to \
         V2L2 for the ZCLVersion attribute of the basic cluster.")
setAddressing(V1RC1, APS_SHORT_ADDRESS, V2L2NwkAddr, APP_ENDPOINT_LIGHT)
check(readBasicClusterAttribute(V1RC1, ZCL_BASIC_CLUSTER_SERVER_ZCL_VERSION_ATTRIBUTE_ID) == 0x01)

writeLog("Item 40b: User initiates a lighting control command on V1RC1 to V2L2 \
         (different to that selected for V1L1, V1L2 and V2L1, if possible).")
sendToggleCommand(V1RC1)
receiveToggleCommand(V2L2)

writeLog("Item 41a: User initiates a read attribute request command frame on V1RC1 to V3L1 for \
         the ZCLVersion attribute of the basic cluster.")
setAddressing(V1RC1, APS_SHORT_ADDRESS, V3L1NwkAddr, APP_ENDPOINT_LIGHT)
check(readBasicClusterAttribute(V1RC1, ZCL_BASIC_CLUSTER_SERVER_ZCL_VERSION_ATTRIBUTE_ID) == 0x01)

writeLog("Item 41b: User initiates a lighting control command on V1RC1 to V3L1 \
         (different to that selected for V1L1 and V1L2, if possible).")
sendToggleCommand(V1RC1)
receiveToggleCommand(V3L1)

writeLog("Item 42a: User initiates a read attribute request command frame on V1RC1 to \
         V3L2 for the ZCLVersion attribute of the basic cluster.")
setAddressing(V1RC1, APS_SHORT_ADDRESS, V3L2NwkAddr, APP_ENDPOINT_LIGHT)
check(readBasicClusterAttribute(V1RC1, ZCL_BASIC_CLUSTER_SERVER_ZCL_VERSION_ATTRIBUTE_ID) == 0x01)

writeLog("Item 42b: User initiates a lighting control command on V1RC1 to V3L2 \
         (different to that selected for V1L1, V1L2 and V2L1, if possible).")
sendToggleCommand(V1RC1)
receiveToggleCommand(V3L2)

idle([V1RC1, V1L1, V1L2, V2L1, V2L2, V3L1, V3L2])
