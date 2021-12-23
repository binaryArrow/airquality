"""
@testcase
@description 5.13 TP-LLI-TC-12: Multi remote, multi vendor

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

writeLog("Item 5a: Power on V2RC1. (Reset device to FN)")
resetEndDeviceToFN([V2RC1])

writeLog("Item 5b: With V1RC1 held close to V2RC1, user initiates a touchlink command on V1RC1. \
         Touchlink should succeed.")
touchlink(V1RC1, V2RC1)
receiveAndCheck(V2RC1, connectedStr)
idle([V1RC1, V2RC1])
V2RC1NwkAddr = getNwkAddress(V2RC1)
writeLog("V2RC1 network address - 0x%04X" % V2RC1NwkAddr)
sleep(2)

writeLog("Item 6a: With V2RC1 held close to V1L1, user initiates a touchlink command on V2RC1. \
         Touchlink should succeed.")
touchlink(V2RC1, V1L1, TOUCHLINK_COMMISSIONING_SKIPPED_STATUS)
idle([V2RC1, V1L1])
sleep(2)

writeLog("Item 6b: With V2RC1 held close to V1L2, user initiates a touchlink command on V2RC1. \
         Touchlink should succeed.")
touchlink(V2RC1, V1L2, TOUCHLINK_COMMISSIONING_SKIPPED_STATUS)
idle([V2RC1, V1L2])

writeLog("Item 7a: User initiates a read attribute request command frame on V2RC1 to V1L1 for \
         the ZCLVersion attribute of the basic cluster.")
setAddressing(V2RC1, APS_SHORT_ADDRESS, V1L1NwkAddr, APP_ENDPOINT_LIGHT)
check(readBasicClusterAttribute(V2RC1, ZCL_BASIC_CLUSTER_SERVER_ZCL_VERSION_ATTRIBUTE_ID) == 0x01)

sleep(1)
writeLog("Item 7b: User initiates a lighting control command on V2RC1 to V1L1 \
         (different to its current state).")
sendOffCommand(V2RC1)
receiveOffCommand(V1L1)

sleep(2)
writeLog("Item 8a: User initiates a read attribute request command frame on V2RC1 to V1L2 for \
         the ZCLVersion attribute of the basic cluster.")
setAddressing(V2RC1, APS_SHORT_ADDRESS, V1L2NwkAddr, APP_ENDPOINT_LIGHT)
check(readBasicClusterAttribute(V2RC1, ZCL_BASIC_CLUSTER_SERVER_ZCL_VERSION_ATTRIBUTE_ID) == 0x01)

writeLog("Item 8b: User initiates a lighting control command on V2RC1 to V1L2 \
         (different to its current state).")
sendToggleCommand(V2RC1)
receiveToggleCommand(V1L2)

writeLog("Item 9a: User initiates a read attribute request command frame on V1RC1 to V1L1 for \
         the ZCLVersion attribute of the basic cluster.")
setAddressing(V1RC1, APS_SHORT_ADDRESS, V1L1NwkAddr, APP_ENDPOINT_LIGHT)
check(readBasicClusterAttribute(V1RC1, ZCL_BASIC_CLUSTER_SERVER_ZCL_VERSION_ATTRIBUTE_ID) == 0x01)

writeLog("Item 9b: UUser initiates a lighting control command on V1RC1 to V1L1 \
         (different to its current state)..")
sendToggleCommand(V1RC1)
receiveToggleCommand(V1L1)

writeLog("Item 10a: User initiates a read attribute request command frame on V1RC1 to \
         V1L2 for the ZCLVersion attribute of the basic cluster.")
setAddressing(V1RC1, APS_SHORT_ADDRESS, V1L2NwkAddr, APP_ENDPOINT_LIGHT)
check(readBasicClusterAttribute(V1RC1, ZCL_BASIC_CLUSTER_SERVER_ZCL_VERSION_ATTRIBUTE_ID) == 0x01)

writeLog("Item 10b: User initiates a lighting control command on V1RC1 to V1L2 \
         (different to its current state).")
sendToggleCommand(V1RC1)
receiveToggleCommand(V1L2)

writeLog("Item 11a: Power on V2L1, V2L2, V3L1 and V3L2 (Reset devices to FN)")
resetRouterToFN([V2L1, V2L2, V3L1, V3L2])

writeLog("Item 11b: With V2RC1 held close to V2L1, user initiates a touchlink command on V2RC1. \
         Touchlink should succeed.")
touchlink(V2RC1, V2L1)
idle([V2RC1, V2L1])
V2L1NwkAddr = getNwkAddress(V2L1)
writeLog("V2L1 network address - 0x%04X" % V2L1NwkAddr)
sleep(2)

writeLog("Item 11c: With V2RC1 held close to V2L2, user initiates a touchlink command on V2RC1. \
         Touchlink should succeed.")
touchlink(V2RC1, V2L2)
idle([V2RC1, V2L2])
V2L2NwkAddr = getNwkAddress(V2L2)
writeLog("V2L2 network address - 0x%04X" % V2L2NwkAddr)
sleep(2)

writeLog("Item 11d: With V2RC1 held close to V3L1, user initiates a touchlink command on V2RC1. \
         Touchlink should succeed.")
touchlink(V2RC1, V3L1)
idle([V2RC1, V3L1])
V3L1NwkAddr = getNwkAddress(V3L1)
writeLog("V3L1 network address - 0x%04X" % V3L1NwkAddr)
sleep(2)

writeLog("Item 11e: With V2RC1 held close to V3L2, user initiates a touchlink command on V2RC1. \
         Touchlink should succeed.")
touchlink(V2RC1, V3L2)
idle([V2RC1, V3L2])
V3L2NwkAddr = getNwkAddress(V3L2)
writeLog("V3L2 network address - 0x%04X" % V3L2NwkAddr)
sleep(2)

writeLog("Item 12a: User initiates a read attribute request command frame on V2RC1 to V1L1 for \
         the ZCLVersion attribute of the basic cluster.")
setAddressing(V2RC1, APS_SHORT_ADDRESS, V1L1NwkAddr, APP_ENDPOINT_LIGHT)
check(readBasicClusterAttribute(V2RC1, ZCL_BASIC_CLUSTER_SERVER_ZCL_VERSION_ATTRIBUTE_ID) == 0x01)

writeLog("Item 12b: User initiates a lighting control command on V2RC1 to V1L1 \
         (different to its current state).")
sendToggleCommand(V2RC1)
receiveToggleCommand(V1L1)

writeLog("Item 13a: User initiates a read attribute request command frame on V2RC1 to V1L2 for \
         the ZCLVersion attribute of the basic cluster.")
setAddressing(V2RC1, APS_SHORT_ADDRESS, V1L2NwkAddr, APP_ENDPOINT_LIGHT)
check(readBasicClusterAttribute(V2RC1, ZCL_BASIC_CLUSTER_SERVER_ZCL_VERSION_ATTRIBUTE_ID) == 0x01)

writeLog("Item 13b: User initiates a lighting control command on V2RC1 to V1L2 \
         (different to its current state).")
sendToggleCommand(V2RC1)
receiveToggleCommand(V1L2)

writeLog("Item 14a: User initiates a read attribute request command frame on V2RC1 to V2L1 for \
         the ZCLVersion attribute of the basic cluster.")
setAddressing(V2RC1, APS_SHORT_ADDRESS, V2L1NwkAddr, APP_ENDPOINT_LIGHT)
check(readBasicClusterAttribute(V2RC1, ZCL_BASIC_CLUSTER_SERVER_ZCL_VERSION_ATTRIBUTE_ID) == 0x01)

writeLog("Item 14b: User initiates a lighting control command on V2RC1 to V2L1 \
         (different to its current state).")
sendToggleCommand(V2RC1)
receiveToggleCommand(V2L1)

writeLog("Item 15a: User initiates a read attribute request command frame on V2RC1 to V2L2 for \
         the ZCLVersion attribute of the basic cluster.")
setAddressing(V2RC1, APS_SHORT_ADDRESS, V2L2NwkAddr, APP_ENDPOINT_LIGHT)
check(readBasicClusterAttribute(V2RC1, ZCL_BASIC_CLUSTER_SERVER_ZCL_VERSION_ATTRIBUTE_ID) == 0x01)

writeLog("Item 15b: User initiates a lighting control command on V2RC1 to V2L2 \
         (different to its current state).")
sendToggleCommand(V2RC1)
receiveToggleCommand(V2L2)

writeLog("Item 16a: User initiates a read attribute request command frame on V2RC1 to V3L1 for \
         the ZCLVersion attribute of the basic cluster.")
setAddressing(V2RC1, APS_SHORT_ADDRESS, V3L1NwkAddr, APP_ENDPOINT_LIGHT)
check(readBasicClusterAttribute(V2RC1, ZCL_BASIC_CLUSTER_SERVER_ZCL_VERSION_ATTRIBUTE_ID) == 0x01)

writeLog("Item 16b: User initiates a lighting control command on V2RC1 to V3L1 \
         (different to its current state).")
sendToggleCommand(V2RC1)
receiveToggleCommand(V3L1)

writeLog("Item 17a: User initiates a read attribute request command frame on V2RC1 to V3L2 for \
         the ZCLVersion attribute of the basic cluster.")
setAddressing(V2RC1, APS_SHORT_ADDRESS, V3L2NwkAddr, APP_ENDPOINT_LIGHT)
check(readBasicClusterAttribute(V2RC1, ZCL_BASIC_CLUSTER_SERVER_ZCL_VERSION_ATTRIBUTE_ID) == 0x01)

writeLog("Item 17b: User initiates a lighting control command on V2RC1 to V3L2 \
         (different to its current state).")
sendToggleCommand(V2RC1)
receiveToggleCommand(V3L2)

writeLog("Item 18a: With V1RC1 held close to V2L1, user initiates a touchlink command on V1RC1. \
         Touchlink should succeed.")
touchlink(V1RC1, V2L1, TOUCHLINK_COMMISSIONING_SKIPPED_STATUS)
idle([V1RC1, V2L1])
sleep(2)

writeLog("Item 18b: With V1RC1 held close to V2L2, user initiates a touchlink command on V1RC1. \
         Touchlink should succeed.")
touchlink(V1RC1, V2L2, TOUCHLINK_COMMISSIONING_SKIPPED_STATUS)
idle([V1RC1, V2L2])
sleep(2)

writeLog("Item 18c: With V1RC1 held close to V3L1, user initiates a touchlink command on V1RC1. \
         Touchlink should succeed.")
touchlink(V1RC1, V3L1, TOUCHLINK_COMMISSIONING_SKIPPED_STATUS)
idle([V1RC1, V3L1])
sleep(2)

writeLog("Item 18d: With V1RC1 held close to V3L2, user initiates a touchlink command on V1RC1. \
         Touchlink should succeed.")
touchlink(V1RC1, V3L2, TOUCHLINK_COMMISSIONING_SKIPPED_STATUS)
idle([V1RC1, V3L2])
sleep(2)

writeLog("Item 19a: User initiates a read attribute request command frame on V1RC1 to V1L1 for \
         the ZCLVersion attribute of the basic cluster.")
setAddressing(V1RC1, APS_SHORT_ADDRESS, V1L1NwkAddr, APP_ENDPOINT_LIGHT)
check(readBasicClusterAttribute(V1RC1, ZCL_BASIC_CLUSTER_SERVER_ZCL_VERSION_ATTRIBUTE_ID) == 0x01)

writeLog("Item 19b: User initiates a lighting control command on V1RC1 to V1L1 \
         (different to its current state).")
sendToggleCommand(V1RC1)
receiveToggleCommand(V1L1)

writeLog("Item 20a: User initiates a read attribute request command frame on V1RC1 to V1L2 for \
         the ZCLVersion attribute of the basic cluster.")
setAddressing(V1RC1, APS_SHORT_ADDRESS, V1L2NwkAddr, APP_ENDPOINT_LIGHT)
check(readBasicClusterAttribute(V1RC1, ZCL_BASIC_CLUSTER_SERVER_ZCL_VERSION_ATTRIBUTE_ID) == 0x01)

writeLog("Item 20b: User initiates a lighting control command on V1RC1 to V1L2 \
         (different to its current state).")
sendToggleCommand(V1RC1)
receiveToggleCommand(V1L2)

writeLog("Item 21a: User initiates a read attribute request command frame on V1RC1 to V2L1 for \
         the ZCLVersion attribute of the basic cluster.")
setAddressing(V1RC1, APS_SHORT_ADDRESS, V2L1NwkAddr, APP_ENDPOINT_LIGHT)
check(readBasicClusterAttribute(V1RC1, ZCL_BASIC_CLUSTER_SERVER_ZCL_VERSION_ATTRIBUTE_ID) == 0x01)

writeLog("Item 21b: User initiates a lighting control command on V1RC1 to V2L1 \
         (different to its current state).")
sendToggleCommand(V1RC1)
receiveToggleCommand(V2L1)

writeLog("Item 22a: User initiates a read attribute request command frame on V1RC1 to V2L2 for \
         the ZCLVersion attribute of the basic cluster.")
setAddressing(V1RC1, APS_SHORT_ADDRESS, V2L2NwkAddr, APP_ENDPOINT_LIGHT)
check(readBasicClusterAttribute(V1RC1, ZCL_BASIC_CLUSTER_SERVER_ZCL_VERSION_ATTRIBUTE_ID) == 0x01)

writeLog("Item 22b: User initiates a lighting control command on V1RC1 to V2L2 \
         (different to its current state).")
sendToggleCommand(V1RC1)
receiveToggleCommand(V2L2)

writeLog("Item 23a: User initiates a read attribute request command frame on V1RC1 to V3L1 for \
         the ZCLVersion attribute of the basic cluster.")
setAddressing(V1RC1, APS_SHORT_ADDRESS, V3L1NwkAddr, APP_ENDPOINT_LIGHT)
check(readBasicClusterAttribute(V1RC1, ZCL_BASIC_CLUSTER_SERVER_ZCL_VERSION_ATTRIBUTE_ID) == 0x01)

writeLog("Item 23b: User initiates a lighting control command on V1RC1 to V3L1 \
         (different to its current state).")
sendToggleCommand(V1RC1)
receiveToggleCommand(V3L1)

writeLog("Item 24a: User initiates a read attribute request command frame on V1RC1 to V3L2 for \
         the ZCLVersion attribute of the basic cluster.")
setAddressing(V1RC1, APS_SHORT_ADDRESS, V3L2NwkAddr, APP_ENDPOINT_LIGHT)
check(readBasicClusterAttribute(V1RC1, ZCL_BASIC_CLUSTER_SERVER_ZCL_VERSION_ATTRIBUTE_ID) == 0x01)

writeLog("Item 24b: User initiates a lighting control command on V1RC1 to V3L2 \
         (different to its current state).")
sendToggleCommand(V1RC1)
receiveToggleCommand(V3L2)

writeLog("Item 25: With V1RC1 and V2RC1 held away from V1L1 (their parent), \
         remove and replace both sets of batteries.")
powerOff([V1RC1, V2RC1])
sleep(3)
sendCommand(V1RC1, resetCmd)
receiveAndCheck(V1RC1, connectedStr)
sendCommand(V2RC1, resetCmd)
receiveAndCheck(V2RC1, connectedStr)

writeLog("Item 26a: User initiates a read attribute request command frame on V1RC1 to V1L1 for \
         the ZCLVersion attribute of the basic cluster.")
setAddressing(V1RC1, APS_SHORT_ADDRESS, V1L1NwkAddr, APP_ENDPOINT_LIGHT)
check(readBasicClusterAttribute(V1RC1, ZCL_BASIC_CLUSTER_SERVER_ZCL_VERSION_ATTRIBUTE_ID) == 0x01)

writeLog("Item 26b: User initiates a lighting control command on V1RC1 to V1L1 \
         (different to its current state).")
sendToggleCommand(V1RC1)
receiveToggleCommand(V1L1)

writeLog("Item 27a: User initiates a read attribute request command frame on V1RC1 to V1L2 for \
         the ZCLVersion attribute of the basic cluster.")
setAddressing(V1RC1, APS_SHORT_ADDRESS, V1L2NwkAddr, APP_ENDPOINT_LIGHT)
check(readBasicClusterAttribute(V1RC1, ZCL_BASIC_CLUSTER_SERVER_ZCL_VERSION_ATTRIBUTE_ID) == 0x01)

writeLog("Item 27b: User initiates a lighting control command on V1RC1 to V1L2 \
         (different to its current state).")
sendToggleCommand(V1RC1)
receiveToggleCommand(V1L2)

writeLog("Item 28a: User initiates a read attribute request command frame on V1RC1 to V2L1 for \
         the ZCLVersion attribute of the basic cluster.")
setAddressing(V1RC1, APS_SHORT_ADDRESS, V2L1NwkAddr, APP_ENDPOINT_LIGHT)
check(readBasicClusterAttribute(V1RC1, ZCL_BASIC_CLUSTER_SERVER_ZCL_VERSION_ATTRIBUTE_ID) == 0x01)

writeLog("Item 28b: User initiates a lighting control command on V1RC1 to V2L1 \
         (different to its current state).")
sendToggleCommand(V1RC1)
receiveToggleCommand(V2L1)

writeLog("Item 29a: User initiates a read attribute request command frame on V1RC1 to V2L2 for \
         the ZCLVersion attribute of the basic cluster.")
setAddressing(V1RC1, APS_SHORT_ADDRESS, V2L2NwkAddr, APP_ENDPOINT_LIGHT)
check(readBasicClusterAttribute(V1RC1, ZCL_BASIC_CLUSTER_SERVER_ZCL_VERSION_ATTRIBUTE_ID) == 0x01)

writeLog("Item 29b: User initiates a lighting control command on V1RC1 to V2L2 \
         (different to its current state).")
sendToggleCommand(V1RC1)
receiveToggleCommand(V2L2)

writeLog("Item 30a: User initiates a read attribute request command frame on V1RC1 to V3L1 for \
         the ZCLVersion attribute of the basic cluster.")
setAddressing(V1RC1, APS_SHORT_ADDRESS, V3L1NwkAddr, APP_ENDPOINT_LIGHT)
check(readBasicClusterAttribute(V1RC1, ZCL_BASIC_CLUSTER_SERVER_ZCL_VERSION_ATTRIBUTE_ID) == 0x01)

writeLog("Item 30b: User initiates a lighting control command on V1RC1 to V3L1 \
         (different to its current state).")
sendToggleCommand(V1RC1)
receiveToggleCommand(V3L1)

writeLog("Item 31a: User initiates a read attribute request command frame on V1RC1 to V3L2 for \
         the ZCLVersion attribute of the basic cluster.")
setAddressing(V1RC1, APS_SHORT_ADDRESS, V3L2NwkAddr, APP_ENDPOINT_LIGHT)
check(readBasicClusterAttribute(V1RC1, ZCL_BASIC_CLUSTER_SERVER_ZCL_VERSION_ATTRIBUTE_ID) == 0x01)

writeLog("Item 31b: User initiates a lighting control command on V1RC1 to V3L2 \
         (different to its current state).")
sendToggleCommand(V1RC1)
receiveToggleCommand(V3L2)

writeLog("Item 32a: User initiates a read attribute request command frame on V2RC1 to V1L1 for \
         the ZCLVersion attribute of the basic cluster.")
setAddressing(V2RC1, APS_SHORT_ADDRESS, V1L1NwkAddr, APP_ENDPOINT_LIGHT)
check(readBasicClusterAttribute(V2RC1, ZCL_BASIC_CLUSTER_SERVER_ZCL_VERSION_ATTRIBUTE_ID) == 0x01)

writeLog("Item 32b: User initiates a lighting control command on V1RC1 to V1L1 \
         (different to its current state).")
sendToggleCommand(V2RC1)
receiveToggleCommand(V1L1)

writeLog("Item 33a: User initiates a read attribute request command frame on V2RC1 to V1L2 for \
         the ZCLVersion attribute of the basic cluster.")
setAddressing(V2RC1, APS_SHORT_ADDRESS, V1L2NwkAddr, APP_ENDPOINT_LIGHT)
check(readBasicClusterAttribute(V2RC1, ZCL_BASIC_CLUSTER_SERVER_ZCL_VERSION_ATTRIBUTE_ID) == 0x01)

writeLog("Item 33b: User initiates a lighting control command on V1RC1 to V1L2 \
         (different to its current state).")
sendToggleCommand(V2RC1)
receiveToggleCommand(V1L2)

writeLog("Item 34a: User initiates a read attribute request command frame on V2RC1 to V2L1 for \
         the ZCLVersion attribute of the basic cluster.")
setAddressing(V2RC1, APS_SHORT_ADDRESS, V2L1NwkAddr, APP_ENDPOINT_LIGHT)
check(readBasicClusterAttribute(V2RC1, ZCL_BASIC_CLUSTER_SERVER_ZCL_VERSION_ATTRIBUTE_ID) == 0x01)

writeLog("Item 34b: User initiates a lighting control command on V1RC1 to V2L1 \
         (different to its current state).")
sendToggleCommand(V2RC1)
receiveToggleCommand(V2L1)

writeLog("Item 35a: User initiates a read attribute request command frame on V2RC1 to V2L2 for \
         the ZCLVersion attribute of the basic cluster.")
setAddressing(V2RC1, APS_SHORT_ADDRESS, V2L2NwkAddr, APP_ENDPOINT_LIGHT)
check(readBasicClusterAttribute(V2RC1, ZCL_BASIC_CLUSTER_SERVER_ZCL_VERSION_ATTRIBUTE_ID) == 0x01)

writeLog("Item 35b: User initiates a lighting control command on V1RC1 to V2L2 \
         (different to its current state).")
sendToggleCommand(V2RC1)
receiveToggleCommand(V2L2)

writeLog("Item 36a: User initiates a read attribute request command frame on V2RC1 to V3L1 for \
         the ZCLVersion attribute of the basic cluster.")
setAddressing(V2RC1, APS_SHORT_ADDRESS, V3L1NwkAddr, APP_ENDPOINT_LIGHT)
check(readBasicClusterAttribute(V2RC1, ZCL_BASIC_CLUSTER_SERVER_ZCL_VERSION_ATTRIBUTE_ID) == 0x01)

writeLog("Item 36b: User initiates a lighting control command on V1RC1 to V3L1 \
         (different to its current state).")
sendToggleCommand(V2RC1)
receiveToggleCommand(V3L1)

writeLog("Item 37a: User initiates a read attribute request command frame on V2RC1 to V3L2 for \
         the ZCLVersion attribute of the basic cluster.")
setAddressing(V2RC1, APS_SHORT_ADDRESS, V3L2NwkAddr, APP_ENDPOINT_LIGHT)
check(readBasicClusterAttribute(V2RC1, ZCL_BASIC_CLUSTER_SERVER_ZCL_VERSION_ATTRIBUTE_ID) == 0x01)

writeLog("Item 37b: User initiates a lighting control command on V1RC1 to V3L2 \
         (different to its current state).")
sendToggleCommand(V2RC1)
receiveToggleCommand(V3L2)

idle([V1RC1, V2RC1, V1L1, V1L2, V2L1, V2L2, V3L1, V3L2])
