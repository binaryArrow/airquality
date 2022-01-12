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

uint8_t appstate = APP_STARTUP_STATE;
uint8_t next_appstate = APP_NOTHING_STATE;


/************
SCD-TIMER
************/
static HAL_AppTimer_t periodicMeasurementTimer;
static HAL_AppTimer_t delayTimer;

static void delaytimer(uint16_t, uint8_t);

static void initTimer();

static void periodicMeasurementTimerComplete();
static void delayTimerComplete();

//Calculate
uint16_t ccs_co2;
uint8_t co2_output_CCS[] = " XXXXX ppm CO2 \r\n";
uint16_t ccs_tvoc;
uint8_t tvoc_output_CCS[] = " XXXXX ppb TVOC \r\n";


//I2C
bool checkHWID = false;
bool checkStatus = false;
uint8_t ccs5Byte[5] = {0xFF,0x11, 0xE5, 0x72, 0x8A};
uint8_t ccsOneByte;
uint8_t ccsTwoByte[2];
uint8_t ccs4Byte[4];

static HAL_I2cDescriptor_t i2cdescriptorCCSOneByte;
static HAL_I2cDescriptor_t i2cdescriptorCCSTwoByte;
static HAL_I2cDescriptor_t i2cdescriptorCCS4Byte;
static HAL_I2cDescriptor_t i2cdescriptorCCS5Byte;


/***********************************************
I2C-CALLBACK
***********************************************/

/************
CCS-CALLBACK
************/
static void callbackCCS5Byte(bool result){
	if(!result){
		appWriteDataToUsart((uint8_t*)"callbackCCSResetSw called with 0\r\n", sizeof("callbackCCS5Byte called with 1\r\n")-1);
	}
	HAL_CloseI2cPacket(&i2cdescriptorCCS5Byte);
}

static void callbackCCSOneByte(bool result){
	if(!result){
		appWriteDataToUsart((uint8_t*)"callbackCCSOneByte called with 0\r\n", sizeof("callbackCCSOneByte called with 1\r\n")-1);
	}
	HAL_CloseI2cPacket(&i2cdescriptorCCSOneByte);
	if(checkHWID && (ccsOneByte != CCS_HWID)){
		appWriteDataToUsart((uint8_t*)"HWID not 0x81\r\n", sizeof("HWID not 0x81\r\n")-1);
		checkHWID = false;
	}
	
	if(checkStatus && ((ccsOneByte & 0x04) != CCS_DATA_RDY)){
		appWriteDataToUsart((uint8_t*)"Status not rdy\r\n", sizeof("Status not rdy\r\n")-1);
		checkStatus = false;
	} else {
		appWriteDataToUsart((uint8_t*)"Status rdy\r\n", sizeof("Status rdy\r\n")-1);
		checkStatus = false;
	}
}
static void callbackCCSTwoByte(bool result){
	if(!result){
		appWriteDataToUsart((uint8_t*)"callbackCCSTwoByte called with 0\r\n", sizeof("callbackCCSTwoByte called with 1\r\n")-1);
	}
	HAL_CloseI2cPacket(&i2cdescriptorCCSTwoByte);
}

static void callbackCCS4Byte(bool result){
	if(!result){
		appWriteDataToUsart((uint8_t*)"callbackCCS4Byte called with 0\r\n", sizeof("callbackCCS4Byte called with 1\r\n")-1);
	}
	HAL_CloseI2cPacket(&i2cdescriptorCCS4Byte);
}

/***********************************************
I2C-DESCRIPTOR
***********************************************/
/************
CCS-DESCRIPTOR
************/
static HAL_I2cDescriptor_t i2cdescriptorCCS5Byte={
	.tty = TWI_CHANNEL_0,
	.clockRate = I2C_CLOCK_RATE_62,
	.f = callbackCCS5Byte,
	.id = CCS811_ADD,
	.data = ccs5Byte,
	.length = 5,
	.lengthAddr = HAL_NO_INTERNAL_ADDRESS
};

static HAL_I2cDescriptor_t i2cdescriptorCCSOneByte={
	.tty = TWI_CHANNEL_0,
	.clockRate = I2C_CLOCK_RATE_62,
	.f = callbackCCSOneByte,
	.id = CCS811_ADD,
	.data = &ccsOneByte,
	.length = 1,
	.lengthAddr = HAL_NO_INTERNAL_ADDRESS
};

static HAL_I2cDescriptor_t i2cdescriptorCCSTwoByte={
	.tty = TWI_CHANNEL_0,
	.clockRate = I2C_CLOCK_RATE_62,
	.f = callbackCCSTwoByte,
	.id = CCS811_ADD,
	.data = ccsTwoByte,
	.length = 2,
	.lengthAddr = HAL_NO_INTERNAL_ADDRESS
};

static HAL_I2cDescriptor_t i2cdescriptorCCS4Byte={
	.tty = TWI_CHANNEL_0,
	.clockRate = I2C_CLOCK_RATE_62,
	.f = callbackCCS4Byte,
	.id = CCS811_ADD,
	.data = ccs4Byte,
	.length = 4,
	.lengthAddr = HAL_NO_INTERNAL_ADDRESS
};
/***********************************************
Calculation-Methods
***********************************************/
/************
CCS-CALCULATION
************/
void calculateCCS(){
	ccs_co2 = (ccs4Byte[0] << 8) | ccs4Byte[1];
	
	uint32_to_str((uint8_t *) co2_output_CCS, sizeof(co2_output_CCS),ccs_co2, 1, 5);
	
	ccs_tvoc = (ccs4Byte[2] << 8) | ccs4Byte[3];
	
	uint32_to_str((uint8_t *) tvoc_output_CCS, sizeof(tvoc_output_CCS),ccs_tvoc, 1, 5);
}

/************
SHT-CALCULATION
************/

/***********************************************
I2C-Methods
***********************************************/
/************
CCS-I2C
************/
void resetCCS(){
	
	/*
	ccs5Byte[0] = 0xFF;//(CCS_RESET_SW_CMD & 0xFF00000000) >> 32;
	ccs5Byte[1] = 0x11;//(CCS_RESET_SW_CMD & 0x00FF000000) >> 24;
	ccs5Byte[2] = 0xE5;//(CCS_RESET_SW_CMD & 0x0000FF0000) >> 16;
	ccs5Byte[3] = 0x72;//(CCS_RESET_SW_CMD & 0x000000FF00) >> 8;
	ccs5Byte[4] = 0x8a;//CCS_RESET_SW_CMD & 0x00000000FF;
	*/
	if (-1 == HAL_OpenI2cPacket(&i2cdescriptorCCS5Byte)){
		appWriteDataToUsart((uint8_t*)"open fail ccs reset\r\n", sizeof("open fail ccs reset\r\n")-1);
	}
	if (-1 == HAL_WriteI2cPacket(&i2cdescriptorCCS5Byte)){
		appWriteDataToUsart((uint8_t*)"write fail ccs reset\r\n", sizeof("write fail ccs reset\r\n")-1);
	}
	appWriteDataToUsart((uint8_t*)"CCS Reset \r\n", sizeof("CCS Reset \r\n")-1);

};

void writeCCSHWIDReg(){
	ccsOneByte = CCS_HWID_REG;
	if (-1 == HAL_OpenI2cPacket(&i2cdescriptorCCSOneByte)){
		appWriteDataToUsart((uint8_t*)"open fail ccs hwid\r\n", sizeof("open fail ccs hwid\r\n")-1);
	}
	if (-1 == HAL_WriteI2cPacket(&i2cdescriptorCCSOneByte)){
		appWriteDataToUsart((uint8_t*)"write fail ccs hwid\r\n", sizeof("write fail ccs hwid\r\n")-1);
	}
	appWriteDataToUsart((uint8_t*)"CCS hwid \r\n", sizeof("CCS hwid \r\n")-1);
}

void readCCSHWIDReg(){
	checkHWID = true;
	if (-1 == HAL_OpenI2cPacket(&i2cdescriptorCCSOneByte)){
		appWriteDataToUsart((uint8_t*)"open fail ccs hwid\r\n", sizeof("open fail ccs hwid\r\n")-1);
	}
	if (-1 == HAL_ReadI2cPacket(&i2cdescriptorCCSOneByte)){
		appWriteDataToUsart((uint8_t*)"read fail ccs hwid\r\n", sizeof("write fail ccs hwid\r\n")-1);
	}
	appWriteDataToUsart((uint8_t*)"CCS hwid read \r\n", sizeof("CCS hwid read\r\n")-1);
}

void changeCCSAppstate(){
	ccsOneByte = CCS_BOOTLOADER_APPSTATE;
	if (-1 == HAL_OpenI2cPacket(&i2cdescriptorCCSOneByte)){
		appWriteDataToUsart((uint8_t*)"open fail ccs bootloader\r\n", sizeof("open fail ccs bootloader\r\n")-1);
	}
	if (-1 == HAL_WriteI2cPacket(&i2cdescriptorCCSOneByte)){
		appWriteDataToUsart((uint8_t*)"write fail ccs bootloader\r\n", sizeof("write fail ccs bootloader\r\n")-1);
	}
	appWriteDataToUsart((uint8_t*)"CCS bootloader \r\n", sizeof("CCS bootloader \r\n")-1);
}
void writeMeasModeCCS(){
	ccsTwoByte[0] = CCS_MEAS_MODE_REG;
	ccsTwoByte[1] = CCS_MEAS_MODE;
	if (-1 == HAL_OpenI2cPacket(&i2cdescriptorCCSTwoByte)){
		appWriteDataToUsart((uint8_t*)"open fail ccs measmode\r\n", sizeof("open fail ccs measmode\r\n")-1);
	}
	if (-1 == HAL_WriteI2cPacket(&i2cdescriptorCCSTwoByte)){
		appWriteDataToUsart((uint8_t*)"write fail ccs measmode\r\n", sizeof("write fail ccs measmode\r\n")-1);
	}
	appWriteDataToUsart((uint8_t*)"CCS measmode \r\n", sizeof("CCS measmode \r\n")-1);
}

void writeccsStatusReg(){
	ccsOneByte = CCS_STATUS_REG;
	if (-1 == HAL_OpenI2cPacket(&i2cdescriptorCCSOneByte)){
		appWriteDataToUsart((uint8_t*)"open fail ccs status reg\r\n", sizeof("open fail ccs status reg\r\n")-1);
	}
	if (-1 == HAL_WriteI2cPacket(&i2cdescriptorCCSOneByte)){
		appWriteDataToUsart((uint8_t*)"write fail ccs status reg\r\n", sizeof("write fail ccs status reg\r\n")-1);
	}
	appWriteDataToUsart((uint8_t*)"CCS status reg \r\n", sizeof("CCS status reg \r\n")-1);
}
void readccsStatusReg(){
	checkStatus = true;
	if (-1 == HAL_OpenI2cPacket(&i2cdescriptorCCSOneByte)){
		appWriteDataToUsart((uint8_t*)"open fail ccs status reg\r\n", sizeof("open fail ccs status reg\r\n")-1);
	}
	if (-1 == HAL_ReadI2cPacket(&i2cdescriptorCCSOneByte)){
		appWriteDataToUsart((uint8_t*)"write fail ccs status reg\r\n", sizeof("write fail ccs status reg\r\n")-1);
	}
	appWriteDataToUsart((uint8_t*)"CCS status reg \r\n", sizeof("CCS status reg \r\n")-1);
}

void writeccsResultReg(){
	ccsOneByte = CCS_RESULT_REG;
	if (-1 == HAL_OpenI2cPacket(&i2cdescriptorCCSOneByte)){
		appWriteDataToUsart((uint8_t*)"open fail ccs result reg\r\n", sizeof("open fail ccs result reg\r\n")-1);
	}
	if (-1 == HAL_WriteI2cPacket(&i2cdescriptorCCSOneByte)){
		appWriteDataToUsart((uint8_t*)"write fail ccs result reg\r\n", sizeof("write fail ccs result reg\r\n")-1);
	}
	appWriteDataToUsart((uint8_t*)"CCS result reg \r\n", sizeof("CCS result reg \r\n")-1);
}

void readccsResultReg(){
	if (-1 == HAL_OpenI2cPacket(&i2cdescriptorCCS4Byte)){
		appWriteDataToUsart((uint8_t*)"open fail ccs read data\r\n", sizeof("open fail ccs read data\r\n")-1);
	}
	if (-1 == HAL_ReadI2cPacket(&i2cdescriptorCCS4Byte)){
		appWriteDataToUsart((uint8_t*)"write fail ccs read data\r\n", sizeof("write fail ccs sread data\r\n")-1);
	}
	appWriteDataToUsart((uint8_t*)"CCS read data \r\n", sizeof("CCS read data \r\n")-1);
}

		
/***********************************************
Timer
***********************************************/

static void initTimer(){
	periodicMeasurementTimer.interval	=	SCD_MES_INTERVAL;		 
	periodicMeasurementTimer.mode		=	TIMER_REPEAT_MODE;       
	periodicMeasurementTimer.callback	=	periodicMeasurementTimerComplete;         
	
	delayTimer.interval = SCD_READ_DELAY_TIME;
	delayTimer.mode		= TIMER_ONE_SHOT_MODE;
	delayTimer.callback = delayTimerComplete;  
	
	delaytimer(SCD_STARTUP_TIME, APP_RESET_CCS_SW_STATE);
}

static void delaytimer(uint16_t time, uint8_t _next_appstate){
	delayTimer.interval = time;
	next_appstate = _next_appstate;
	HAL_StartAppTimer(&delayTimer);
}

static void periodicMeasurementTimerComplete(){
	appWriteDataToUsart((uint8_t*)"mesTimer fired\r\n", sizeof("mesTimer fired\r\n")-1);
	appstate = APP_CCS_WRITE_RESULT_REG_STATE;
	SYS_PostTask(APL_TASK_ID);
}

static void delayTimerComplete(){
	appstate = next_appstate;
	SYS_PostTask(APL_TASK_ID);
}



/***********************************************
Zustandsautomat
***********************************************/

void APL_TaskHandler(void){
switch(appstate){
	case APP_STARTUP_STATE:
		appstate=APP_NOTHING_STATE;
		appInitUsartManager();
		initTimer();
		
	break;
		
	case APP_RESET_CCS_SW_STATE:
		appstate=APP_NOTHING_STATE;
		resetCCS();
		delaytimer(SCD_STARTUP_TIME, APP_CCS_HW_ID_WRITE_REG_STATE);
	break;
	case APP_CCS_HW_ID_WRITE_REG_STATE:
		appstate=APP_NOTHING_STATE;
		writeCCSHWIDReg();
		delaytimer(CCS_MIN_DELAY, APP_CCS_HW_ID_READ_STATE);
		break;
	case APP_CCS_HW_ID_READ_STATE:			
		appstate=APP_NOTHING_STATE;
		readCCSHWIDReg();
		delaytimer(CCS_MIN_DELAY, APP_CCS_CHANGE_TO_APPSTATE_STATE);
		break;
	case APP_CCS_CHANGE_TO_APPSTATE_STATE:	
		appstate=APP_NOTHING_STATE;
		changeCCSAppstate();
		delaytimer(CCS_MIN_DELAY, APP_CCS_WRITE_MEAS_REG_STATE);
		break;
	case APP_CCS_WRITE_MEAS_REG_STATE:		
		appstate=APP_NOTHING_STATE;
		writeMeasModeCCS();
		delaytimer(CSS_DRIVE_STATUS_DELAY, APP_CCS_WRITE_STATUS_REG_STATE);
		break;
	case APP_CCS_WRITE_STATUS_REG_STATE:		
		appstate=APP_NOTHING_STATE;
		writeccsStatusReg();
		delaytimer(CCS_MIN_DELAY, APP_CCS_READ_STATUS_REG_STATE);
		break;
	case APP_CCS_READ_STATUS_REG_STATE:		
		appstate=APP_NOTHING_STATE;
		readccsStatusReg();
		HAL_StartAppTimer(&periodicMeasurementTimer);
		break;
	case APP_CCS_WRITE_RESULT_REG_STATE:		
		appstate=APP_NOTHING_STATE;
		writeccsResultReg();
		delaytimer(CCS_MIN_DELAY, APP_CCS_READ_RESULT_REG_STATE);
		break;
	case APP_CCS_READ_RESULT_REG_STATE:		
		appstate=APP_NOTHING_STATE;
		readccsResultReg();
		delaytimer(CCS_MIN_DELAY, APP_AUSGABE_STATE);
		break;
		
	case APP_AUSGABE_STATE:
		calculateCCS();
		appWriteDataToUsart((uint8_t*)co2_output_CCS, sizeof(co2_output_CCS));
		appWriteDataToUsart((uint8_t*)tvoc_output_CCS, sizeof(tvoc_output_CCS));
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
