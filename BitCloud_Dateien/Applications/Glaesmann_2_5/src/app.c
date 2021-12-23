/**************************************************************************//**
  \file app.c

  \brief Basis-Anwendung.

  \author Markus Krauﬂe

******************************************************************************/


#include <appTimer.h>
#include <zdo.h>
#include <app.h>
#include <adc.h>
#include <sysTaskManager.h>
#include <usartManager.h>
#include <i2cPacket.h>


static HAL_AppTimer_t sendeTimer;

static AppState_t appstate = APP_INIT_STATE;

static void initTimer(void);
static void sendeTimerFired(void);


uint8_t lm73Data[2];
int32_t temperature;
uint8_t t_output[]="0x0000 sensorsignal\r\n";




static bool readSensorDoneCb(){
	appstate=APP_AUSGABE_STATE;
	SYS_PostTask(APL_TASK_ID);
	return 1;
}


static HAL_I2cDescriptor_t i2cdescriptor={
	.tty = TWI_CHANNEL_0,
	.clockRate = I2C_CLOCK_RATE_62,
	.f = readSensorDoneCb,
	.id = 0x4D,
	.data = lm73Data,
	.length = 2,
	.lengthAddr = HAL_NO_INTERNAL_ADDRESS
};

void calculateOutput(){
	uint16_t vorkomma;
	uint16_t nachkomma;
	vorkomma = lm73Data[0];
	vorkomma <<= 8;
	vorkomma |= lm73Data[1];
	vorkomma >>= 7;
	
	nachkomma = lm73Data[1] & (0x7F);
	nachkomma >>= 5;
	nachkomma = nachkomma *25;
	
	temperature = vorkomma*100+nachkomma;
	
}

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
	if (1 == HAL_OpenI2cPacket(&i2cdescriptor))
	appWriteDataToUsart((uint8_t*)"open fail\r\n", sizeof("open fail\r\n")-1);
	if (-1 == HAL_ReadI2cPacket(&i2cdescriptor))
	appWriteDataToUsart((uint8_t*)"read fail\r\n", sizeof("read fail\r\n")-1);
	appstate=APP_NOTHING_STATE;
	break;
	
	case APP_AUSGABE_STATE:
	calculateOutput();
	int32_to_str(t_output,sizeof(t_output),temperature/100,0,4);
	uint32_to_str(t_output,sizeof(t_output),abs(temperature)%100,5,2);
	appWriteDataToUsart(t_output, sizeof(t_output));
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
