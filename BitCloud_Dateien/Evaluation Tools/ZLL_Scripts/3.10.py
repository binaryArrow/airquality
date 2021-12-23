"""
@testcase
@description 3.10 TP-CST-TC-10: Identify cluster with client as DUT

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
from identifyCluster import *
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

ed1ExtAddr = getExtAddr(client1)
writeLog("ED1 extended address - %016X" % ed1ExtAddr)

r1ExtAddr = getExtAddr(server1)
writeLog("R1 extended address - %016X" % r1ExtAddr)

writeLog("P1 Power on client and server1")
powerOn([client1, server1])

writeLog("P2 Touchlink client and server")
touchlink(client1, server1)
idle([client1, server1])

r1NwkAddr = getNwkAddress(server1)
writeLog("R1 network address - 0x%04X" % r1NwkAddr)

ed1NwkAddr = getNwkAddress(client1)
writeLog("ED1 network address - 0x%04X" % ed1NwkAddr)

writeLog("Set addressing on client")
setAddressing(client1, APS_SHORT_ADDRESS, r1NwkAddr, APP_ENDPOINT_LIGHT)

writeLog("P3 Client sends on command")
sendOnCommand(client1) 
receiveOnCommand(server1)

#*****************************************************************************************
# Test body
#*****************************************************************************************\
writeLog("1 Client sends identify command")
sendIdentifyCommand(client1)
receiveIdentify(server1)

writeLog("2 Client sends an identify query command")
sendIdentifyQueryCommand(client1)
receiveIdentifyQueryResponse(client1)

writeLog("3 Client sends an identify command to stop identifying")
sendIdentifyCommand(client1, identifyTime = 0)
receiveIdentify(server1)

writeLog("4 Client immediately reads attributes")
check(readIdentifyClusterAttribute(client1, ZCL_IDENTIFY_CLUSTER_IDENTIFY_TIME_ATTRIBUTE_ID) == 0)

writeLog("5a Client sends an trigger effect command requesting blink effect")
sendTriggerEffectCommand(client1, ZCL_EFFECT_IDENTIFIER_BLINK, ZCL_EFFECT_VARIANT_DEFAULT)
receiveTriggerEffect(server1, ZCL_EFFECT_IDENTIFIER_BLINK)

writeLog("5b Client sends an trigger effect command requesting breathe effect")
sendTriggerEffectCommand(client1, ZCL_EFFECT_IDENTIFIER_BREATHE, ZCL_EFFECT_VARIANT_DEFAULT)
receiveTriggerEffect(server1, ZCL_EFFECT_IDENTIFIER_BREATHE)

writeLog("5c Client sends an trigger effect command requesting okay effect")
sendTriggerEffectCommand(client1, ZCL_EFFECT_IDENTIFIER_OKAY, ZCL_EFFECT_VARIANT_DEFAULT)
receiveTriggerEffect(server1, ZCL_EFFECT_IDENTIFIER_OKAY)

writeLog("5d Client sends an trigger effect command requesting channel change effect")
sendTriggerEffectCommand(client1, ZCL_EFFECT_IDENTIFIER_CHANNEL_CHANGE, ZCL_EFFECT_VARIANT_DEFAULT)
receiveTriggerEffect(server1, ZCL_EFFECT_IDENTIFIER_CHANNEL_CHANGE)

writeLog("5e Client sends an trigger effect command requesting breathe effect")
sendTriggerEffectCommand(client1, ZCL_EFFECT_IDENTIFIER_BREATHE, ZCL_EFFECT_VARIANT_DEFAULT)
receiveTriggerEffect(server1, ZCL_EFFECT_IDENTIFIER_BREATHE)

writeLog("5f Client sends an trigger effect command requesting finish the current effect")
sendTriggerEffectCommand(client1, ZCL_EFFECT_IDENTIFIER_FINISH_EFFECT, ZCL_EFFECT_VARIANT_DEFAULT)
receiveTriggerEffect(server1, ZCL_EFFECT_IDENTIFIER_FINISH_EFFECT)

writeLog("5g Client sends an trigger effect command requesting breathe effect")
sendTriggerEffectCommand(client1, ZCL_EFFECT_IDENTIFIER_BREATHE, ZCL_EFFECT_VARIANT_DEFAULT)
receiveTriggerEffect(server1, ZCL_EFFECT_IDENTIFIER_BREATHE)

writeLog("5h Client sends an trigger effect command requesting stop effect")
sendTriggerEffectCommand(client1, ZCL_EFFECT_IDENTIFIER_STOP_EFFECT, ZCL_EFFECT_VARIANT_DEFAULT)
receiveTriggerEffect(server1, ZCL_EFFECT_IDENTIFIER_STOP_EFFECT)
