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

static HAL_AppTimer_t mesTimerSCD;
static HAL_AppTimer_t startupTimer;
static HAL_AppTimer_t resetDelayTimer;
static HAL_AppTimer_t readDelayTimer;
static AppState_t appstate = APP_STARTUP_STATE;

static void initMesTimer();
static void initStartupTimer();
static void mesTimerComplete();
static void startupTimerComplete();
static void resetDelayTimerComplete();
static void readDelayTimerComplete();

static void resetSCD();
static void initializeSCD();



static HAL_I2cDescriptor_t i2cdescriptorcmdSCD;
static HAL_I2cDescriptor_t i2cdescriptorrdSCD;

uint8_t scdcmd[2];
uint8_t scddata[9];
uint16_t scd_rd_co2;
uint16_t scd_rd_temp;
uint16_t scd_rd_rh;
uint8_t co2_output_SCD[] = " XXXXX ppm CO2 \r\n";

static void callbackcmdSCD(bool result){
	if(!result){
		appWriteDataToUsart((uint8_t*)"SCD callbackcmd called with 0\r\n", sizeof("SCD callbackcmd called with 1\r\n")-1);
		}
		HAL_CloseI2cPacket(&i2cdescriptorcmdSCD);
}

static void callbackrdSCD(bool result){
	if(!result){
		appWriteDataToUsart((uint8_t*)"SCD callbackrd called with 0\r\n", sizeof("Error: SCD callbackrd called with 0\r\n")-1);
		}
	HAL_CloseI2cPacket(&i2cdescriptorrdSCD);
}


/***********************************************
SCD-Descriptor
***********************************************/
static HAL_I2cDescriptor_t i2cdescriptorcmdSCD={
	.tty = TWI_CHANNEL_0,
	.clockRate = I2C_CLOCK_RATE_62,
	.f = callbackcmdSCD,
	.id = SCD41_ADD,
	.data = scdcmd,
	.length = 2,
	.lengthAddr = HAL_NO_INTERNAL_ADDRESS
};

static HAL_I2cDescriptor_t i2cdescriptorrdSCD={
	.tty = TWI_CHANNEL_0,
	.clockRate = I2C_CLOCK_RATE_62,
	.f = callbackrdSCD,
	.id = SCD41_ADD,
	.data = scddata,
	.length = 9,
	.lengthAddr = HAL_NO_INTERNAL_ADDRESS
};

/***********************************************
Calculation-Methods
***********************************************/

void calculateOutputSCD(){
	scd_rd_co2 = scddata[0];
	scd_rd_co2 <<= 8;
	scd_rd_co2 |= scddata[1];
	
	scd_rd_temp = scddata[3];
	scd_rd_temp <<= 8;
	scd_rd_temp |= scddata[4];
	
	scd_rd_rh = scddata[6];
	scd_rd_rh <<= 8;
	scd_rd_rh |= scddata[7];
	
	uint32_to_str((uint8_t *) co2_output_SCD, sizeof(co2_output_SCD),scd_rd_co2, 1, 5);
}

/***********************************************
I2C-Methods
***********************************************/
void resetSCD(){
	uint16_t cmd = SCD41_STOP_PERIODIC_MES_CMD; //0x3F86
	scdcmd[0] = ((cmd & 0xFF00) >> 8);
	scdcmd[1] = cmd & 0x00FF;
	
		 if (-1 == HAL_OpenI2cPacket(&i2cdescriptorcmdSCD)){
			 appWriteDataToUsart((uint8_t*)"open fail scd reset\r\n", sizeof("open fail scd reset\r\n")-1);
		 }
		 if (-1 == HAL_WriteI2cPacket(&i2cdescriptorcmdSCD)){
			 appWriteDataToUsart((uint8_t*)"write fail scd reset\r\n", sizeof("write fail scd reset\r\n")-1);
		 }
		 appWriteDataToUsart((uint8_t*)"SCD Reset \r\n", sizeof("SCD Reset \r\n")-1);
		 
		 HAL_StartAppTimer(&resetDelayTimer);
	
}
void initializeSCD(){ //YELLOW = CLOCK (SCL) GREEN = DATA (SCD)
	uint16_t cmd = SCD41_PERIODIC_MES_CMD; //0x21b1
	scdcmd[0] = ((cmd & 0xFF00) >> 8);
	scdcmd[1] = cmd & 0x00FF;
	
	
	 if (-1 == HAL_OpenI2cPacket(&i2cdescriptorcmdSCD)){
		appWriteDataToUsart((uint8_t*)"open fail scd init\r\n", sizeof("open fail scd init\r\n")-1);
	}	
	if (-1 == HAL_WriteI2cPacket(&i2cdescriptorcmdSCD)){
		appWriteDataToUsart((uint8_t*)"write fail scd init\r\n", sizeof("write fail scd init\r\n")-1);
	} 
	appWriteDataToUsart((uint8_t*)"SCD Initialized \r\n", sizeof("SCD Initialized \r\n")-1);
	
	HAL_StartAppTimer(&mesTimerSCD);
}


void checkIfSCDReady(){
}

void callReadSCD(){
	uint16_t cmd = SCD41_READ_MES;
	scdcmd[0] = ((cmd & 0xFF00) >> 8);
	scdcmd[1] = cmd & 0x00FF;
	
	if (-1 == HAL_OpenI2cPacket(&i2cdescriptorcmdSCD)){
		appWriteDataToUsart((uint8_t*)"open fail scd readcall\r\n", sizeof("open fail scd readcall\r\n")-1);
	}
	if (-1 == HAL_WriteI2cPacket(&i2cdescriptorcmdSCD)){
		appWriteDataToUsart((uint8_t*)"write fail scd readcall\r\n", sizeof("write fail scd readcall\r\n")-1);
	}
	appWriteDataToUsart((uint8_t*)"SCD readcall finished \r\n", sizeof("SCD readcall finished \r\n")-1);
	
	HAL_StartAppTimer(&readDelayTimer);
}
void readSCD(){ 
	if (-1 == HAL_OpenI2cPacket(&i2cdescriptorrdSCD)){
		appWriteDataToUsart((uint8_t*)"open fail scd read\r\n", sizeof("open fail scd read\r\n")-1);
	}
	if (-1 == HAL_ReadI2cPacket(&i2cdescriptorrdSCD)){
		appWriteDataToUsart((uint8_t*)"read fail scd read\r\n", sizeof("read fail scd read\r\n")-1);
	}
	appstate = APP_AUSGABE_STATE;
	SYS_PostTask(APL_TASK_ID);
}

		
/***********************************************
Timer Initialization
***********************************************/

static void initMesTimer(){
	mesTimerSCD.interval	=	SCD_MES_INTERVAL;		 // Timer interval
	mesTimerSCD.mode		=	TIMER_REPEAT_MODE;       // Timer-Mode
	mesTimerSCD.callback	=	mesTimerComplete;         // Callback function
}

static void initStartupTimer(){ //TIMER_ONE_SHOT_MODE or TIMER_REPEAT_MODE
	startupTimer.interval	=	SCD_STARTUP_TIME;		 // Timer interval
	startupTimer.mode		=	TIMER_ONE_SHOT_MODE;		 // Timer-Mode
	startupTimer.callback	=	startupTimerComplete;        // Callback function
	HAL_StartAppTimer(&startupTimer);
}

static void initResetDelayTimer(){ //TIMER_ONE_SHOT_MODE or TIMER_REPEAT_MODE
	resetDelayTimer.interval	=	SCD_DELAY_TIME;				 // Timer interval
	resetDelayTimer.mode		=	TIMER_ONE_SHOT_MODE;		 // Timer-Mode
	resetDelayTimer.callback	=	resetDelayTimerComplete;    // Callback function
}

static void initreadDelayTimer(){ //TIMER_ONE_SHOT_MODE or TIMER_REPEAT_MODE
	readDelayTimer.interval	=	SCD_READ_DELAY_TIME;				 // Timer interval
	readDelayTimer.mode		=	TIMER_ONE_SHOT_MODE;		 // Timer-Mode
	readDelayTimer.callback	=	readDelayTimerComplete;    // Callback function
}



static void mesTimerComplete(){
	appWriteDataToUsart((uint8_t*)"mesTImer fired\r\n", sizeof("mesTimer fired\r\n")-1);
	appstate = APP_CALL_FOR_READ_STATE;
	SYS_PostTask(APL_TASK_ID);
}

static void startupTimerComplete(){
	appWriteDataToUsart((uint8_t*)"startupTimer fired\r\n", sizeof("startupTimer fired\r\n")-1);
	appstate = APP_RESET_SENSOR_STATE;
	SYS_PostTask(APL_TASK_ID);
}

static void resetDelayTimerComplete(){
	appWriteDataToUsart((uint8_t*)"resetDelayTimer fired\r\n", sizeof("resetDelayTimer fired\r\n")-1);
	appstate = APP_INIT_SENSOR_STATE;
	SYS_PostTask(APL_TASK_ID);
}

static void readDelayTimerComplete(){
	appWriteDataToUsart((uint8_t*)"readDelayTimer fired\r\n", sizeof("readDelayTimer fired\r\n")-1);
	appstate = APP_READ_SCD_STATE;
	SYS_PostTask(APL_TASK_ID);
}





/***********************************************
Zustandsautomat
***********************************************/

void APL_TaskHandler(void){
switch(appstate){
	case APP_STARTUP_STATE:
		appInitUsartManager();
		initStartupTimer();
		initResetDelayTimer();
		initreadDelayTimer();
		appstate=APP_NOTHING_STATE;
		SYS_PostTask(APL_TASK_ID);
	break;
		
	case APP_RESET_SENSOR_STATE:
		resetSCD();
	break;
		
	case APP_INIT_SENSOR_STATE:
		initMesTimer();
		initializeSCD();
		appstate=APP_NOTHING_STATE;
		SYS_PostTask(APL_TASK_ID);
	break;
	
	case APP_CALL_FOR_READ_STATE:
		appWriteDataToUsart((uint8_t*)"call for read state reached \r\n", sizeof("call for read state reached \r\n")-1);
		callReadSCD();
	break;
	
	case APP_READ_SCD_STATE:
		readSCD();
	break;
	
	case APP_AUSGABE_STATE:
		calculateOutputSCD();
		appWriteDataToUsart((uint8_t*)co2_output_SCD, sizeof(co2_output_SCD));
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
