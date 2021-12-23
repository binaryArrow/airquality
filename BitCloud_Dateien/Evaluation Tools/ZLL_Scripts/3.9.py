"""
@testcase
@description 3.9 TP-CST-TC-09: Identify cluster with server as DUT

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

writeLog("2 Client immediately reads attributes")
identifyTime = readIdentifyClusterAttribute(client1, ZCL_IDENTIFY_CLUSTER_IDENTIFY_TIME_ATTRIBUTE_ID)
check(identifyTime <= 0x003C and identifyTime != 0)

sleep(3)

writeLog("3 After 3s client reads attributes")
identifyTime = readIdentifyClusterAttribute(client1, ZCL_IDENTIFY_CLUSTER_IDENTIFY_TIME_ATTRIBUTE_ID)
check(identifyTime >= 0x0036 and identifyTime <= 0x003C) # 5 percent window near 0x0039

writeLog("4 Client sends an identify query command")
sendIdentifyQueryCommand(client1)
receiveIdentifyQueryResponse(client1)

writeLog("5 Client sends an identify command to stop identifying")
sendIdentifyCommand(client1, identifyTime = 0)
receiveIdentify(server1)

writeLog("6 Client immediately reads attributes")
check(readIdentifyClusterAttribute(client1, ZCL_IDENTIFY_CLUSTER_IDENTIFY_TIME_ATTRIBUTE_ID) == 0)

writeLog("8a Client sends an trigger effect command requesting blink effect")
sendTriggerEffectCommand(client1, ZCL_EFFECT_IDENTIFIER_BLINK, ZCL_EFFECT_VARIANT_DEFAULT)
receiveTriggerEffect(server1, ZCL_EFFECT_IDENTIFIER_BLINK)

writeLog("8b Client sends an trigger effect command requesting breathe effect")
sendTriggerEffectCommand(client1, ZCL_EFFECT_IDENTIFIER_BREATHE, ZCL_EFFECT_VARIANT_DEFAULT)
receiveTriggerEffect(server1, ZCL_EFFECT_IDENTIFIER_BREATHE)

writeLog("8c Client sends an trigger effect command requesting okay effect")
sendTriggerEffectCommand(client1, ZCL_EFFECT_IDENTIFIER_OKAY, ZCL_EFFECT_VARIANT_DEFAULT)
receiveTriggerEffect(server1, ZCL_EFFECT_IDENTIFIER_OKAY)

writeLog("8d Client sends an trigger effect command requesting channel change effect")
sendTriggerEffectCommand(client1, ZCL_EFFECT_IDENTIFIER_CHANNEL_CHANGE, ZCL_EFFECT_VARIANT_DEFAULT)
receiveTriggerEffect(server1, ZCL_EFFECT_IDENTIFIER_CHANNEL_CHANGE)

writeLog("8e Client sends an trigger effect command requesting breathe effect")
sendTriggerEffectCommand(client1, ZCL_EFFECT_IDENTIFIER_BREATHE, ZCL_EFFECT_VARIANT_DEFAULT)
receiveTriggerEffect(server1, ZCL_EFFECT_IDENTIFIER_BREATHE)

writeLog("8f Client sends an trigger effect command requesting finish the current effect")
sendTriggerEffectCommand(client1, ZCL_EFFECT_IDENTIFIER_FINISH_EFFECT, ZCL_EFFECT_VARIANT_DEFAULT)
receiveTriggerEffect(server1, ZCL_EFFECT_IDENTIFIER_FINISH_EFFECT)

writeLog("8g Client sends an trigger effect command requesting breathe effect")
sendTriggerEffectCommand(client1, ZCL_EFFECT_IDENTIFIER_BREATHE, ZCL_EFFECT_VARIANT_DEFAULT)
receiveTriggerEffect(server1, ZCL_EFFECT_IDENTIFIER_BREATHE)

writeLog("8h Client sends an trigger effect command requesting stop effect")
sendTriggerEffectCommand(client1, ZCL_EFFECT_IDENTIFIER_STOP_EFFECT, ZCL_EFFECT_VARIANT_DEFAULT)
receiveTriggerEffect(server1, ZCL_EFFECT_IDENTIFIER_STOP_EFFECT)

writeLog("9 Client sends an trigger effect command with unknown variant")
sendTriggerEffectCommand(client1, ZCL_EFFECT_IDENTIFIER_BLINK, ZCL_EFFECT_VARIANT_UNKNOWN)
receiveTriggerEffect(server1, ZCL_EFFECT_IDENTIFIER_BLINK)

writeLog("9a Wait for 1 Sec")
idle([client1, server1], 1000)

writeLog("10a Client sends a write attributes undivided command")
writeAttributesUndivided(client1,
                         IDENTIFY_CLUSTER_ID,
                         ZCL_IDENTIFY_CLUSTER_IDENTIFY_TIME_ATTRIBUTE_ID, 
                         ZCL_U16BIT_DATA_TYPE_ID, 
                         0x000a, 
                         0x1234, # Unknown attribute ID 
                         ZCL_U16BIT_DATA_TYPE_ID, 
                         0x0044, 
                         retStatus = ZCL_UNSUPPORTED_ATTRIBUTE_STATUS)

writeLog("10b Client immediately reads attributes")
check(readIdentifyClusterAttribute(client1, ZCL_IDENTIFY_CLUSTER_IDENTIFY_TIME_ATTRIBUTE_ID) == 0)

writeLog("11a Client sends a write attributes no response command")
writeAttributesNoResponse(client1,
                          IDENTIFY_CLUSTER_ID,
                          ZCL_IDENTIFY_CLUSTER_IDENTIFY_TIME_ATTRIBUTE_ID, 
                          ZCL_U16BIT_DATA_TYPE_ID, 
                          0x000a)

idle([client1, server1], 5000)

writeLog("11b After 5s client reads attributes")
identifyTime = readIdentifyClusterAttribute(client1, ZCL_IDENTIFY_CLUSTER_IDENTIFY_TIME_ATTRIBUTE_ID)
check(identifyTime >= 0x0004 and identifyTime <= 0x0006) # 10 percent window near 0x0005

writeLog("12 Client sends an trigger effect command requesting stop effect")
sendTriggerEffectCommand(client1, ZCL_EFFECT_IDENTIFIER_STOP_EFFECT, ZCL_EFFECT_VARIANT_DEFAULT)
receiveTriggerEffect(server1, ZCL_EFFECT_IDENTIFIER_STOP_EFFECT)
