"""
@testcase
@description 4.10 TP-NWI-TC-10: Classical joining non-ZLL ZED to DUT ZR on ZLL network

@tags
  POSITIVE

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
sys.path.remove(scriptPath)

#*****************************************************************************************
# Initialization
#*****************************************************************************************\
portList = []

configureCommunication()
  
ZED1 = deviceScannerGetAssociatedPort(TEST_DEVICE_TYPE_END_DEVICE, portList)
dutZR1 = deviceScannerGetAssociatedPort(TEST_DEVICE_TYPE_ROUTER, portList)
ZED2 = deviceScannerGetAssociatedPort(TEST_DEVICE_TYPE_NON_ZLL_END_DEVICE, portList)

#*****************************************************************************************
# Test preparation
#*****************************************************************************************\
writeLog("Item P1: Power on ZED1 and DUT ZR1. (Reset devices to FN)")
resetRouterToFN([dutZR1])
resetEndDeviceToFN([ZED1])

writeLog("Item P2: User initiates a touchlink command on ZED1 with ZED1 held close to DUT ZR1. Touchlink should succeed")
touchlink(ZED1, dutZR1)
idle([ZED1, dutZR1])
ZR1NwkAddr = getNwkAddress(dutZR1)
writeLog("DUT ZR1 network address - 0x%04X" % ZR1NwkAddr)

writeLog("Item P3: User initiates a turn on command on ZED1")
setAddressing(ZED1, APS_SHORT_ADDRESS, ZR1NwkAddr, APP_ENDPOINT_LIGHT)
sendOnCommand(ZED1)
receiveOnCommand(dutZR1)

writeLog("Item P4: User initiates a turn off command on ZED1")
sendOffCommand(ZED1)
receiveOffCommand(dutZR1)
sleep(1)

#*****************************************************************************************
# Test procedure
#*****************************************************************************************\
writeLog("Item 1: Power on ZED2")
channel = getChannel(dutZR1)
haResetToFN([ZED2], BC_FAILURE_STATUS)
sleep(5)

writeLog("Item 2a: By application specific means, ZED2 performs a classical network scan on \
         all channels but finds no networks with associate permit set to TRUE.")
haRestartNwk(ZED2, channel, BC_FAILURE_STATUS)
writeLog("Item 2b: ZED2 may repeat the above scans or simply wait for further instructions.")
sleep(1)

writeLog("Item 3: By application specific means, the associate permit of the ZLL network is set to TRUE")
setPermitJoinReq(dutZR1, PERMIT_JOIN_DURATION_INFINITE)
receiveSetPermitJoinResp(dutZR1, BC_SUCCESS_STATUS)

writeLog("Item 4a: By application specific means, ZED2 performs a classical network scan on all \
         channels and finds the ZLL network with associate permit set to TRUE.")
haRestartNwk(ZED2, channel, BC_FAILURE_STATUS)
writeLog("Item 4b: ZED2 attempts to associate to the network through DUT ZR1")
sleep(1)
writeLog("Item 4c: DUT ZR1 confirms the association request and allocates a random address to ZED2")
sleep(1)
writeLog("Item 5: DUT ZR1 transports the network key to ZED2, setting the source address field to \
         0xffffffffffffffff and encrypted with the certification pre-installed link key.")
sleep(1)

writeLog("Item 6: If the transport key command frame can be decrypted, ZED2 announces itself on \
         the network. Otherwise, ZR2 does not announce itself on the network.")
idle([ZED1, dutZR1, ZED2])
