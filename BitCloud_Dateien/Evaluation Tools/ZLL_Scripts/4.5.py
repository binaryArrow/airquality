"""
@testcase
@description 4.5 TP-NWI-TC-05: Classical joining DUT ZED to non-ZLL network (primary channels)

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
sys.path.remove(scriptPath)

#*****************************************************************************************
# Initialization
#*****************************************************************************************\
portList = []

configureCommunication()
  
ZC = deviceScannerGetAssociatedPort(TEST_DEVICE_TYPE_NON_ZLL_COORDINATOR, portList)
dutZED1 = deviceScannerGetAssociatedPort(TEST_DEVICE_TYPE_END_DEVICE, portList)

#*****************************************************************************************
# Test preparation
#*****************************************************************************************\
writeLog("Item P1: Power on ZC. (Reset device to FN)")
haResetToFN([ZC], BC_SUCCESS_STATUS)

writeLog("Item P2: By application specific means, ZC forms a non-ZLL network on a primary ZLL channel.")
haRestartNwk(ZC, getFirstChannel(zllPrimaryChannelMask), BC_SUCCESS_STATUS)

#*****************************************************************************************
# Test procedure
#*****************************************************************************************\
writeLog("Item 1: Power on DUT ZED1")
resetEndDeviceToFN([dutZED1])

writeLog("Item 2a: By application specific means, DUT ZED1 performs a classical network \
          scan on the primary channels but finds no networks with associate permit set to TRUE")
nwkAssociation(dutZED1, BC_FAILURE_STATUS, BC_FAILURE_STATUS)
writeLog("Item 2b: DUT ZED1 then performs a classical network scan on the secondary \
          channels but finds no networks with associate permit set to TRUE")
sleep(1)
writeLog("Item 2c: DUT ZED1 may repeat the above scans or simply wait for further instructions")
sleep(1)

writeLog("Item 3: By application specific means, the associate permit of the ZLL network is set to TRUE")
setPermitJoinReq(ZC, PERMIT_JOIN_DURATION_INFINITE)
receiveSetPermitJoinResp(ZC, BC_SUCCESS_STATUS)

writeLog("Item 4a: By application specific means, DUT ZED1 performs a classical network scan \
         on the primary channels and finds the ZLL network with associate permit set to TRUE")
dutZED1NwkAddr = nwkAssociation(dutZED1, BC_SUCCESS_STATUS, BC_SUCCESS_STATUS)
check(dutZED1NwkAddr != None)
writeLog("Item 4b: DUT ZED1 attempts to associate to the network through ZC")
sleep(1)
writeLog("Item 4c: ZC confirms the association request and allocates a random address to DUT ZED1")
sleep(1)
writeLog("Item 5: ZR1 transports the network key to DUT ZED1, encrypted with the \
         certification pre-installed link key")
sleep(1)

writeLog("Item 6: DUT ZED1 announces itself on the network")
idle([ZC, dutZED1])
