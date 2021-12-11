from public import *
from common import *

#################################################################
#                     Common parameters
#################################################################

TEST_DEVICE_TYPE_ROUTER              = 0x00
TEST_DEVICE_TYPE_END_DEVICE          = 0x01
TEST_DEVICE_TYPE_NON_ZLL_COORDINATOR = 0x02
TEST_DEVICE_TYPE_NON_ZLL_ROUTER      = 0x03
TEST_DEVICE_TYPE_NON_ZLL_END_DEVICE  = 0x04

#################################################################
#                         Functions
#################################################################
def configureCommunication():
  # Scan the nodes defined in wsnrunner.properties
  portDescriptorsList = env.getNodeList(10000)
  for portDescriptor in portDescriptorsList:
    port = misc.__nodeFactory.create(portDescriptor).getConnection()
    print "Found port: %s" % portDescriptor
    port.setTesterMode(0)
    port.setTimeout(PORT_DEFAULT_TIMEOUT)
    powerOff([port])


def deviceScannerGetAssociatedPort(deviceType, portList):
  deviceTypes = {
    TEST_DEVICE_TYPE_ROUTER             : "ZLL Router",
    TEST_DEVICE_TYPE_END_DEVICE         : "ZLL EndDevice",
    TEST_DEVICE_TYPE_NON_ZLL_COORDINATOR: "Non-ZLL Coordinator",
    TEST_DEVICE_TYPE_NON_ZLL_ROUTER     : "Non-ZLL Router",
    TEST_DEVICE_TYPE_NON_ZLL_END_DEVICE : "Non-ZLL EndDevice"
  }

  deviceCaption = deviceTypes[deviceType]

  # Scan the nodes defined in wsnrunner.properties
  portDescriptorsList = env.getNodeList(10000)
  for portDescriptor in portDescriptorsList:
    port = misc.__nodeFactory.create(portDescriptor).getConnection()

    if port not in portList:
      devType = getDeviceType(port)
      if (deviceType == devType):
        portList.append(port)
        writeLog('Port %s associated with %s ' % (portDescriptor, deviceCaption))
        return port

  writeLog('Device not found: %s ' % deviceCaption)
  check(0)
