/**************************************************************************//**
  \file app.c

  \brief Basis-Anwendung.

  \author Markus Krauße

Kommentare:
			Soweit alles in Ordnung.

			Wenn Sie unbenutzen Quellcode haben, löschen Sie diesen raus. Dadurch, dass Sie den Usart Manager verwenden können Sie die initUsart-Funktion vernachlässigen. X

			Des Weiteren wenn Ihnen der Kompiler Warnungen gibt, sollten Sie diese nicht ignorieren. X

			Ich würde Ihnen empfehlen beim Auslesen des ADC Wertes eher mit Dezimalzahlen als Hexadezimalzahlen zu arbeiten, da diese leichter zu interpretieren sind. X

			Sie können natürlich auch 8-Bit Werte mittels der uint32_to_str-Funktion Arrays zuweisen. X

			Denken Sie daran den ADC-Deskriptor nach dem Auslesen des Sensors wieder zu schließen. X

******************************************************************************/


#include <appTimer.h>
#include <zdo.h>
//#include <types.h>
#include <app.h>
#include <adc.h>
#include <sysTaskManager.h>
#include <usartManager.h>


static HAL_AppTimer_t sendeTimer;

static AppState_t appstate = APP_INIT_STATE;

static void initTimer(void);
static void sendeTimerFired(void);

uint8_t decimal[]="lightlvl: XX \r\n";
uint8_t adcData;

static HAL_AdcDescriptor_t adcdescriptor;

static void readSensorDoneCb(){
	appstate=APP_AUSGABE_STATE;
	HAL_CloseAdc(&adcdescriptor);
	SYS_PostTask(APL_TASK_ID);
}

static HAL_AdcDescriptor_t adcdescriptor = {
	.resolution = RESOLUTION_8_BIT,
	.sampleRate = ADC_4800SPS,
	.voltageReference = AVCC,
	.bufferPointer = &adcData,
	.selectionsAmount = 1,
	.callback = readSensorDoneCb
};


static void initTimer(){
	sendeTimer.interval = APP_SENDE_INTERVAL;      // Timer interval
	sendeTimer.mode     = TIMER_REPEAT_MODE;       // Timer-Mode
	sendeTimer.callback = sendeTimerFired;         // Callback function
	HAL_StartAppTimer(&sendeTimer);                // Start sendeTimer
}
static void sendeTimerFired(){
	appstate=APP_READ_STATE;
	SYS_PostTask(APL_TASK_ID);
}






void APL_TaskHandler(void){
switch(appstate){
	case APP_INIT_STATE:
	appInitUsartManager();
	initTimer();
	
	appstate=APP_NOTHING_STATE;
	HAL_StartAppTimer(&sendeTimer);
	break;
	
	case APP_READ_STATE:
	HAL_OpenAdc(&adcdescriptor);
	HAL_ReadAdc(&adcdescriptor, HAL_ADC_CHANNEL1);
	appstate=APP_NOTHING_STATE;
	break;
	
	case APP_AUSGABE_STATE:
	uint32_to_str(decimal, sizeof(decimal), adcData, 10, 2);
	appWriteDataToUsart(decimal, sizeof(decimal));
	
	appstate=APP_NOTHING_STATE;
	break;
	
	case APP_NOTHING_STATE:
	break;
}
}





/*******************************************************************************
  \brief The function is called by the stack to notify the application about 
  various network-related events. See detailed description in API Reference.
  
  Mandatory function: must be present in any application.

  \param[in] nwkParams - contains notification type and additional data varying
             an event
  \return none
*******************************************************************************/
void ZDO_MgmtNwkUpdateNotf(ZDO_MgmtNwkUpdateNotf_t *nwkParams)
{
  nwkParams = nwkParams;  // Unused parameter warning prevention
}

/*******************************************************************************
  \brief The function is called by the stack when the node wakes up by timer.
  
  When the device starts after hardware reset the stack posts an application
  task (via SYS_PostTask()) once, giving control to the application, while
  upon wake up the stack only calls this indication function. So, to provide 
  control to the application on wake up, change the application state and post
  an application task via SYS_PostTask(APL_TASK_ID) from this function.

  Mandatory function: must be present in any application.
  
  \return none
*******************************************************************************/
void ZDO_WakeUpInd(void)
{
}

#ifdef _BINDING_
/***********************************************************************************
  \brief The function is called by the stack to notify the application that a 
  binding request has been received from a remote node.
  
  Mandatory function: must be present in any application.

  \param[in] bindInd - information about the bound device
  \return none
 ***********************************************************************************/
void ZDO_BindIndication(ZDO_BindInd_t *bindInd)
{
  (void)bindInd;
}

/***********************************************************************************
  \brief The function is called by the stack to notify the application that a 
  binding request has been received from a remote node.

  Mandatory function: must be present in any application.
  
  \param[in] unbindInd - information about the unbound device
  \return none
 ***********************************************************************************/
void ZDO_UnbindIndication(ZDO_UnbindInd_t *unbindInd)
{
  (void)unbindInd;
}
#endif //_BINDING_

/**********************************************************************//**
  \brief The entry point of the program. This function should not be
  changed by the user without necessity and must always include an
  invocation of the SYS_SysInit() function and an infinite loop with
  SYS_RunTask() function called on each step.

  \return none
**************************************************************************/
int main(void)
{
  //Initialization of the System Environment
  SYS_SysInit();

  //The infinite loop maintaing task management
  for(;;)
  {
    //Each time this function is called, the task
    //scheduler processes the next task posted by one
    //of the BitCloud components or the application
    SYS_RunTask();
  }
}

//eof app.c
