/**************************************************************************//**
  \file app.c

  \brief Basis-Anwendung.

  \author Markus Krauße

******************************************************************************/


#include <appTimer.h>
#include <zdo.h>
#include <app.h>
#include <sysTaskManager.h>
#include <usartManager.h>
#include <leds.h>

static AppState_t state = APP_INIT_STATE;
static HAL_AppTimer_t stateSwitchTimer; //Definition des Timers
static void stateSwitchTimerFired(void);  //Prototyp der CB-Funktion des Timers
static void stateSwitchTimerFired(){
	SYS_PostTask(APL_TASK_ID);
}

void APL_TaskHandler(void){
	switch(state){
		case APP_INIT_STATE:
		//Initialisieren der LEDs.
			BSP_OpenLeds(); 
			BSP_OnLed(LED_RED);
			BSP_OffLed(LED_YELLOW);
			BSP_OffLed(LED_GREEN);
			state=APP_RED_STATE;
			stateSwitchTimer.interval = 1000;
			stateSwitchTimer.mode = TIMER_ONE_SHOT_MODE;
			stateSwitchTimer.callback = stateSwitchTimerFired;
			HAL_StartAppTimer(&stateSwitchTimer);
			break;
		case APP_RED_STATE:
			BSP_OnLed(LED_YELLOW); //man könnte erneut alle LEDs dem Zustand entsprechend setzen, bei fehlerfreien betrieb reicht jedoch das setzen der LEDS welche im vergleich mit dem vorherigen Zustand an/aus geschaltet werden müssen.
			state=APP_RED_YELLOW_STATE;
			HAL_StartAppTimer(&stateSwitchTimer);
			break;
		case APP_RED_YELLOW_STATE:
			BSP_OnLed(LED_GREEN);
			BSP_OffLed(LED_RED);
			BSP_OffLed(LED_YELLOW);
			state=APP_GREEN_STATE;
			HAL_StartAppTimer(&stateSwitchTimer);
			break;
		case APP_GREEN_STATE:
			BSP_OffLed(LED_GREEN);
			BSP_OnLed(LED_YELLOW);
			state=APP_YELLOW_STATE;
			HAL_StartAppTimer(&stateSwitchTimer);
			break;
		case APP_YELLOW_STATE:
			BSP_OffLed(LED_YELLOW);
			BSP_OnLed(LED_RED);
			state=APP_RED_STATE;
			HAL_StartAppTimer(&stateSwitchTimer);
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
