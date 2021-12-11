/**************************************************************************//**
  \file app.c

  \brief Basis-Anwendung.

  \author Markus Krauﬂe

******************************************************************************/


#include <appTimer.h>
#include <zdo.h>
#include <app.h>
#include <sysTaskManager.h>
#include <usartManager.h>
#include <leds.h>

//Definition der Timer
static HAL_AppTimer_t blinkTimer; 
static HAL_AppTimer_t blinkTimer2; 
static HAL_AppTimer_t blinkTimer3; 

//Prototypen und globale definitionen der callback funktionen
static void blinkTimerFired(void);  
static void blinkTimer2Fired(void); 
static void blinkTimer3Fired(void);  

static void blinkTimerFired(){
	BSP_ToggleLed(LED_GREEN);
}
static void blinkTimer2Fired(){
	BSP_ToggleLed(LED_YELLOW);
}
static void blinkTimer3Fired(){
	BSP_ToggleLed(LED_RED);
}


void APL_TaskHandler(void){
	BSP_OpenLeds(); 
	blinkTimer.interval = 1000;
	blinkTimer.mode     = TIMER_REPEAT_MODE;
	blinkTimer.callback = blinkTimerFired;
	HAL_StartAppTimer(&blinkTimer);
	
	blinkTimer2.interval = 1500;
	blinkTimer2.mode     = TIMER_REPEAT_MODE;
	blinkTimer2.callback = blinkTimer2Fired;
	HAL_StartAppTimer(&blinkTimer2);
	
	blinkTimer3.interval = 2000;
	blinkTimer3.mode     = TIMER_REPEAT_MODE;
	blinkTimer3.callback = blinkTimer3Fired;
	HAL_StartAppTimer(&blinkTimer3);
	
	
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
