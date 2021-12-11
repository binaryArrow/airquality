/**********************************************************************//**
  \file USARTManager.c

  \brief Implementation of USART interface.

  \author
    Atmel Corporation: http://www.atmel.com \n
    Support email: avr@atmel.com

  Copyright (c) 2008-2015, Atmel Corporation. All rights reserved.
  Licensed under Atmel's Limited License Agreement (BitCloudTM).

  \internal
  History:
    13/06/07 I. Kalganova - Modified

  Last change:
    $Id: WSNUARTManager.c 28108 2015-07-02 14:52:22Z preethi.prabhakaran $
**************************************************************************/
#ifdef _COORDINATOR_

/*****************************************************************************
                              Includes section
******************************************************************************/
#include <sysUtils.h>
#include <sysTypes.h>
#include <WSNDemoApp.h>
#include <WSNVisualizer.h>
#include <serialInterface.h>
#include <WSNCommandHandler.h>
#if APP_INTERFACE == APP_INTERFACE_USBCDC
#include <usb.h>
#else
#include <usart.h>
#endif

/*****************************************************************************
                              Definitions section
******************************************************************************/
// Magic symbol to start SOF end EOF sequences with. Should be duplicated if
// occured inside the message.
#define APP_MAGIC_SYMBOL        0x10
#define APP_SOF_SEQUENCE        {APP_MAGIC_SYMBOL, 0x02}
#define APP_EOF_SEQUENCE        {APP_MAGIC_SYMBOL, 0x03}
#define APP_DUPLICATED_SYMBOL   {APP_MAGIC_SYMBOL, APP_MAGIC_SYMBOL}

#define APP_LINK_SAFETY_TIMEOUT 100 // ms
#define BULK_SIZE               64

/*****************************************************************************
                              Types section
******************************************************************************/
typedef enum _USARTReceiverState_t
{
  USART_RECEIVER_IDLE_RX_STATE,
  USART_RECEIVER_MAGIC_RX_STATE,
  USART_RECEIVER_SOF_RX_STATE,
  USART_RECEIVER_DATA_RX_STATE,
  USART_RECEIVER_FCS_RX_STATE,
  USART_RECEIVER_ERROR_RX_STATE
} USARTReceiverState_t;

typedef struct
{
  uint8_t payload[MAX_RAW_APP_MESSAGE_SIZE];
  uint8_t size;
} UsartMessage_t;

typedef struct _USARTReceiver_t
{
  USARTReceiverState_t state;
  uint8_t              *por;
  uint8_t              rxBuffer[BULK_SIZE];
  uint8_t              strippedCmd[MAX_RAW_APP_MESSAGE_SIZE];
  uint8_t              fcs;
  HAL_AppTimer_t       linkSafetyTimer;
} USARTReceiver_t;

static struct
{
  UsartMessage_t usartMessageQueue[MAX_USART_MESSAGE_QUEUE_COUNT];
  uint8_t head, tail, size;
} wsn2usart;
/****************************************************************************
                              Static functions prototypes section
******************************************************************************/
#if (APP_USE_OTAU != 1) || !defined(OTAU_SERVER)
static void resetUsartRx(void);
static void linkSafetyTimerFired(void);
static void writeConfirm(void);
  #if APP_INTERFACE == APP_INTERFACE_USBCDC
  static void readByteEvent(HAL_UsbRxIndCallback_t *UsbRxIndication);
  #else
  static void readByteEvent(uint16_t readBytesLen);
  #endif
#endif // (APP_USE_OTAU != 1) || !defined(OTAU_SERVER)
static void sendNextMessage(void);

/*****************************************************************************
                              Local variables section
******************************************************************************/

#if APP_INTERFACE == APP_INTERFACE_USBCDC
typedef HAL_UsbHWDescriptor_t HAL_Descriptor_t;
#else
typedef  HAL_UsartDescriptor_t HAL_Descriptor_t; 
#endif

#if (APP_USE_OTAU != 1) || !defined(OTAU_SERVER)
  static USARTReceiver_t usartRx;
  static const uint8_t sof[] = APP_SOF_SEQUENCE;
  static const uint8_t eof[] = APP_EOF_SEQUENCE;
#endif // (APP_USE_OTAU != 1) || !defined(OTAU_SERVER)
   static HAL_Descriptor_t appDescriptor;

/******************************************************************************
                              Implementations section
******************************************************************************/

/******************************************************************************
  \brief Init USART, register USART callbacks.

  \return none
******************************************************************************/
void appStartUsartManager(void)
{
#if (APP_USE_OTAU != 1) || !defined(OTAU_SERVER)
#if  APP_INTERFACE == APP_INTERFACE_USBCDC
   #if  BSP_SUPPORT == BOARD_SAMR21_XPRO
    appDescriptor.usbVbusDetect = true;
   #else
    appDescriptor.usbVbusDetect = false;
   #endif
  appDescriptor.rxBuffer       = usartRx.rxBuffer;
  appDescriptor.rxBufferLength = sizeof(usartRx.rxBuffer);
  appDescriptor.txBuffer       = NULL;
  appDescriptor.txBufferLength = 0;
  appDescriptor.rxCallback     = readByteEvent;
  appDescriptor.txCallback     = writeConfirm;
  appDescriptor.speed = USB_SPEED_FULL;
  appDescriptor.oprMode = USB_BINARY_MODE;
  OPEN_USART(&appDescriptor);
#else
/* RS-232 level stabilization on Atmel RCB KeyRemote board. */
#if BSP_SUPPORT == BOARD_RCB_KEY_REMOTE
  DDRE = (1 << 5);  // LEDP_SEL
  PORTE = 0;
  DDRB = (1 << 6);  // EN_232
  PORTB = 0;
  PORTE = (1 << 5); // latch low level on EN_232
  PORTE = 0;        // latch low level on EN_232
#endif /* BSP_SUPPORT == BOARD_RCB_KEY_REMOTE */

  appDescriptor.tty            = USART_CHANNEL;
  appDescriptor.mode           = USART_MODE_ASYNC;
  appDescriptor.flowControl    = USART_FLOW_CONTROL_NONE;
  appDescriptor.baudrate       = USART_SPEED;
  appDescriptor.dataLength     = USART_DATA8;
  appDescriptor.parity         = USART_PARITY_NONE;
  appDescriptor.stopbits       = USART_STOPBIT_1;
  appDescriptor.rxBuffer       = usartRx.rxBuffer;
  appDescriptor.rxBufferLength = sizeof(usartRx.rxBuffer);
  appDescriptor.txBuffer       = NULL;
  appDescriptor.txBufferLength = 0;
  appDescriptor.rxCallback     = readByteEvent;
  appDescriptor.txCallback     = writeConfirm;

  OPEN_USART(&appDescriptor);
#endif

  usartRx.linkSafetyTimer.mode = TIMER_ONE_SHOT_MODE;
  usartRx.linkSafetyTimer.interval = APP_LINK_SAFETY_TIMEOUT;
  usartRx.linkSafetyTimer.callback = linkSafetyTimerFired;

  resetUsartRx();

#endif // (APP_USE_OTAU != 1) || !defined(OTAU_SERVER)

  memset(&wsn2usart, 0, sizeof(wsn2usart));
}

/******************************************************************************
  \brief Stops USART.

  \return none
 ******************************************************************************/
void appStopUsartManager(void)
{
  CLOSE_USART(&appDescriptor);
}

#if (APP_USE_OTAU != 1) || !defined(OTAU_SERVER)
/******************************************************************************
  \brief Communication usart receiving block resetting routine.

  \return none
 ******************************************************************************/
static void resetUsartRx(void)
{
  HAL_StopAppTimer(&usartRx.linkSafetyTimer);

  usartRx.state = USART_RECEIVER_IDLE_RX_STATE;
  usartRx.por = usartRx.strippedCmd;
  usartRx.fcs = 0;
}
/******************************************************************************
  \brief Link safety timer fired callback.

  \return none
 ******************************************************************************/
static void linkSafetyTimerFired(void)
{
  resetUsartRx();
}

/******************************************************************************
  \brief New USART bytes were received.

  \param[in] readBytesLen - count of received bytes.

  \return none
******************************************************************************/

#if  APP_INTERFACE == APP_INTERFACE_USBCDC
static void readByteEvent(HAL_UsbRxIndCallback_t *UsbRxIndication)
#else
static void readByteEvent(uint16_t bytesReceived)
#endif
{
#if  APP_INTERFACE == APP_INTERFACE_USBCDC
    uint16_t bytesReceived=(UsbRxIndication->length);
#endif
  uint8_t byte;
  while (bytesReceived)
  {
    bool acceptByte = false;

    if (USART_RECEIVER_ERROR_RX_STATE == usartRx.state)
      return;
    if (READ_USART(&appDescriptor, &byte, 1) <= 0)
    {
      usartRx.state = USART_RECEIVER_ERROR_RX_STATE;
      return;
    }
    (bytesReceived)--;

    switch (usartRx.state)
    {
      case USART_RECEIVER_IDLE_RX_STATE:
        if (APP_MAGIC_SYMBOL == byte)
        {
          usartRx.fcs = 0;
          usartRx.state = USART_RECEIVER_SOF_RX_STATE;
        }
        break;

      case USART_RECEIVER_SOF_RX_STATE:
        if (sof[1] == byte)
        {
          usartRx.state = USART_RECEIVER_DATA_RX_STATE;
        }
        else
          usartRx.state = USART_RECEIVER_IDLE_RX_STATE;
        break;

      case USART_RECEIVER_DATA_RX_STATE:
        if (APP_MAGIC_SYMBOL == byte)
          usartRx.state = USART_RECEIVER_MAGIC_RX_STATE;
        else
          acceptByte = true;
        break;

      case USART_RECEIVER_MAGIC_RX_STATE:
        if (APP_MAGIC_SYMBOL == byte)
        {
          usartRx.state = USART_RECEIVER_DATA_RX_STATE;
          acceptByte = true;
        }
        else if (eof[1] == byte)
          usartRx.state = USART_RECEIVER_FCS_RX_STATE;
        else
          usartRx.state = USART_RECEIVER_ERROR_RX_STATE;
        break;

      case USART_RECEIVER_FCS_RX_STATE:
        if (usartRx.fcs == byte)
        {
          appPcCmdReceived(usartRx.strippedCmd, usartRx.por - usartRx.strippedCmd);
        }

        resetUsartRx();
        return;

      default:
        break;
    }

    usartRx.fcs += byte;

    if (acceptByte && (usartRx.por < usartRx.strippedCmd + sizeof(usartRx.strippedCmd)))
      *usartRx.por++ = byte;
  }

  // Throw bone to link safety timer
  HAL_StopAppTimer(&usartRx.linkSafetyTimer);
  HAL_StartAppTimer(&usartRx.linkSafetyTimer);
}
#endif // (APP_USE_OTAU != 1) || !defined(OTAU_SERVER)

/******************************************************************************
  \brief Send next message from queue.

  \return none
 ******************************************************************************/
static void sendNextMessage(void)
{
  if (wsn2usart.size)
  {
      if (-1 == WRITE_USART(&appDescriptor,
                wsn2usart.usartMessageQueue[wsn2usart.head].payload,
                wsn2usart.usartMessageQueue[wsn2usart.head].size))
      wsn2usart.size = 0;
      #if  APP_INTERFACE == APP_INTERFACE_USBCDC
      (void)&appDescriptor;
      #endif
  }
}

/******************************************************************************
  \brief Writing confirmation has been received. New message can be sent.

  \return none
 ******************************************************************************/
#if (APP_USE_OTAU != 1) || !defined(OTAU_SERVER)
static void writeConfirm(void)
{
  if (wsn2usart.size)
  {
    wsn2usart.size--;

    if (++wsn2usart.head >= MAX_USART_MESSAGE_QUEUE_COUNT)
      wsn2usart.head -= MAX_USART_MESSAGE_QUEUE_COUNT;
  }

  //send next message
  sendNextMessage();
}
#endif // (APP_USE_OTAU != 1) || !defined(OTAU_SERVER)

/******************************************************************************
  \brief New message being sent into USART has to be put into queue.

  \param[in] newMessage - new message fields.

  \return true if sending was successful, false otherwise.
 ******************************************************************************/
bool appSendMessageToUsart(void *data, uint8_t dataLength)
{
  UsartMessage_t *msg;
  uint8_t *p, *q, summ, i;
  q = data;
  summ = 0;

  if (wsn2usart.size < MAX_USART_MESSAGE_QUEUE_COUNT &&
      dataLength <= APP_MAX_PAYLOAD)
  {
    wsn2usart.size++;
    msg = &wsn2usart.usartMessageQueue[wsn2usart.tail];

    if (++wsn2usart.tail >= MAX_USART_MESSAGE_QUEUE_COUNT)
      wsn2usart.tail -= MAX_USART_MESSAGE_QUEUE_COUNT;

    p = msg->payload;
    *p++ = 0x10;
    *p++ = 0x02;

    for (i = 0; i < dataLength; i++)
    {
      if (*q == 0x10)
      {
        *p++ = 0x10;
        summ += 0x10;
      }

      summ += *q;
      *p++ = *q++;
    }

    *p++ = 0x10;
    *p++ = 0x03;
    summ += 0x10 + 0x02 + 0x10 + 0x03;
    *p++ = summ;

    msg->size = p - msg->payload;
    sendNextMessage();

    return true;
  }

  return false;
}

#endif
//eof UARTManager.c
