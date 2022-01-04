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
static void calculateOutputSCD();
static void calculateOutputSHT();

//I2C
static void resetSCD();
static void initializeSCD();
static void checkReadySCD(); //stump
static void callReadSCD();
static void readSCD();
static void callReadSHT(uint8_t);
static void readSHT(uint8_t);



static void callbackcmdSCD(bool);
static void callbackrdSCD(bool);
static void callbackcmdSHT(bool);
static void callbackrdSHT(bool);

static HAL_I2cDescriptor_t i2cdescriptorcmdSCD;
static HAL_I2cDescriptor_t i2cdescriptorrdSCD;
static HAL_I2cDescriptor_t i2cdescriptorcmdSHT;
static HAL_I2cDescriptor_t i2cdescriptorrdSHT;

uint8_t scdcmd[2];
uint8_t scddata[9];
uint16_t scd_rd_co2;
uint16_t scd_rd_temp;
uint16_t scd_rd_rh;
uint8_t co2_output_SCD[] = " XXXXX ppm CO2 \r\n";

bool result;
bool tempNegativ;
uint8_t sht21cmd;
uint8_t sht21data[2];
uint16_t sht21_rd_tmp;
uint16_t sht21_rd_rh;
int32_t vorkomma;
int32_t nachkomma;

uint8_t t_output_SHT21[] = "+xxx.xx degree Celsius \r\n";
uint8_t t_output_SHT21_sensorbytes[] = "0xXXXX sensor \r\n";

uint8_t rh_output_SHT21[] = "+xx.xx percent relative Humidity \r\n";
uint8_t rh_output_SHT21_sensorbytes[] = "0xXXXX sensor \r\n";

/***********************************************
I2C-CALLBACK
***********************************************/
/************
SCD-CALLBACK
************/

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

/************
SHT-CALLBACK
************/
static void callbackcmdSHT(bool result){
	if(!result){
		appWriteDataToUsart((uint8_t*)"callbackcmd called with 0\r\n", sizeof("callbackcmd called with 1\r\n")-1);
	}
	HAL_CloseI2cPacket(&i2cdescriptorcmdSHT);
}

static void callbackrdSHT(bool result){
	if(!result){
		appWriteDataToUsart((uint8_t*)"callbackrd called with 0\r\n", sizeof("callbackrd called with 1\r\n")-1);
	}
	HAL_CloseI2cPacket(&i2cdescriptorrdSHT);
}




/***********************************************
I2C-DESCRIPTOR
***********************************************/
/************
SCD-DESCRIPTOR
************/
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

/************
SHT-DESCRIPTOR
************/
static HAL_I2cDescriptor_t i2cdescriptorcmdSHT={
	.tty = TWI_CHANNEL_0,
	.clockRate = I2C_CLOCK_RATE_62,
	.f = callbackcmdSHT,
	.id = 0x40,
	.data = &sht21cmd,
	.length = 1,
	.lengthAddr = HAL_NO_INTERNAL_ADDRESS
};

static HAL_I2cDescriptor_t i2cdescriptorrdSHT={
	.tty = TWI_CHANNEL_0,
	.clockRate = I2C_CLOCK_RATE_62,
	.f = callbackrdSHT,
	.id = 0x40,
	.data = sht21data,
	.length = 2,
	.lengthAddr = HAL_NO_INTERNAL_ADDRESS
};

/***********************************************
Calculation-Methods
***********************************************/
/************
SCD-CALCULATION
************/
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

/************
SHT-CALCULATION
************/
void calculateOutputSHT(){
	uint64_t conversionfactortmp = 26812744140625; // Datasheetformula: -46.85 + 175.72 * sensordata/65536 :: conversionfactor is 175.72/65536 scaled by 10^16 to avoid floating numbers.
	uint64_t correctionoffsettmp = 468500000000000000; // -46.85 scaled by 10^16 and inverted new formula: conversionfactor*sensordata - correctionoffset 
	uint64_t conversionfactorrh = 19073486328125; // Datasheetformula: -6 + 125 * sensordata/65536 :: conversionfactor is 125/65536 scaled by 10^16 to avoid floating numbers.
	uint64_t correctionoffsetrh = 60000000000000000; // -6 scaled by 10^16 and inverted. new formula conversionfactor*sensordata - correctionoffset 
	
	uint64_t temperature = conversionfactortmp * sht21_rd_tmp;
	if(temperature < correctionoffsettmp){
		temperature = correctionoffsettmp - temperature;
		tempNegativ = true;
	}else{
		temperature = temperature - correctionoffsettmp;
		tempNegativ = false;
	}
	
	uint32_t vorkommatmp = temperature/10000000000000000;
	uint32_t nachkommatmp = temperature%10000000000000000;
	if (tempNegativ)
	{
		t_output_SHT21[0] = 0x2d;
	}else{
		t_output_SHT21[0] = 0x2b;
	}
	
	uint64_t relativeHumidity = conversionfactorrh * sht21_rd_rh;
	if(relativeHumidity < correctionoffsetrh){
		relativeHumidity = 0;
	}else{
		relativeHumidity = relativeHumidity - correctionoffsetrh;
	}
	
	uint32_t vorkommarh = relativeHumidity/10000000000000000;
	uint32_t nachkommarh = relativeHumidity%10000000000000000;
	
	
	uint32_to_str((uint8_t *) t_output_SHT21, sizeof(t_output_SHT21),vorkommatmp, 1, 3);
	uint32_to_str((uint8_t *) t_output_SHT21, sizeof(t_output_SHT21),nachkommatmp, 5, 2);
	uint16_to_hexstr((uint8_t *)t_output_SHT21_sensorbytes, sizeof(t_output_SHT21_sensorbytes), sht21_rd_tmp, 2);
	
	uint32_to_str((uint8_t *) rh_output_SHT21, sizeof(rh_output_SHT21),vorkommarh, 1, 2);
	uint32_to_str((uint8_t *) rh_output_SHT21, sizeof(rh_output_SHT21),nachkommarh, 4, 2);
	uint16_to_hexstr((uint8_t *)rh_output_SHT21_sensorbytes, sizeof(rh_output_SHT21_sensorbytes), sht21_rd_rh, 2);
}
/***********************************************
I2C-Methods
***********************************************/
/************
SCD-I2C
************/
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
}


void checkReadySCD(){
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
}

void readSCD(){ 
	if (-1 == HAL_OpenI2cPacket(&i2cdescriptorrdSCD)){
		appWriteDataToUsart((uint8_t*)"open fail scd read\r\n", sizeof("open fail scd read\r\n")-1);
	}
	if (-1 == HAL_ReadI2cPacket(&i2cdescriptorrdSCD)){
		appWriteDataToUsart((uint8_t*)"read fail scd read\r\n", sizeof("read fail scd read\r\n")-1);
	}
}

/************
SHT-I2C
************/
void callReadSHT(uint8_t mode){
	if (mode == MES_TEMP){
		sht21cmd = SHT21_MES_T;
	}else if(mode == MES_RH){
		sht21cmd = SHT21_MES_RH;
	}
	
	if (-1 == HAL_OpenI2cPacket(&i2cdescriptorcmdSHT)){
		appWriteDataToUsart((uint8_t*)"open fail\r\n", sizeof("open fail\r\n")-1);
	}
	
	if (-1 == HAL_WriteI2cPacket(&i2cdescriptorcmdSHT)){
		appWriteDataToUsart((uint8_t*)"write fail\r\n", sizeof("write fail\r\n")-1);
		}
}

void readSHT(uint8_t mode){ 
	if (-1 == HAL_OpenI2cPacket(&i2cdescriptorrdSHT)){
		appWriteDataToUsart((uint8_t*)"open fail\r\n", sizeof("open fail\r\n")-1);
	}
	if (-1 == HAL_ReadI2cPacket(&i2cdescriptorrdSHT)){
		appWriteDataToUsart((uint8_t*)"read fail\r\n", sizeof("read fail\r\n")-1);
	}
	if(mode == MES_TEMP){
		sht21_rd_tmp = sht21data[0];
		sht21_rd_tmp <<= 8;
		sht21_rd_tmp |= sht21data[1];
	}else if(mode == MES_RH){
		sht21_rd_rh = sht21data[0];
		sht21_rd_rh <<= 8;
		sht21_rd_rh |= sht21data[1];
	}
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
	
	delaytimer(SCD_STARTUP_TIME, APP_RESET_SENSOR_STATE);
}

static void delaytimer(uint16_t time, uint8_t _next_appstate){
	delayTimer.interval = time;
	next_appstate = _next_appstate;
	HAL_StartAppTimer(&delayTimer);
}

static void periodicMeasurementTimerComplete(){
	appWriteDataToUsart((uint8_t*)"mesTImer fired\r\n", sizeof("mesTimer fired\r\n")-1);
	appstate = APP_CALL_FOR_READ_SCD_STATE;
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
		
	case APP_RESET_SENSOR_STATE:
		appstate = APP_NOTHING_STATE;
		resetSCD();
		delaytimer(SCD_RESET_DELAY_TIME, APP_INIT_SENSOR_STATE);
	break;
		
	case APP_INIT_SENSOR_STATE:
		appstate=APP_NOTHING_STATE;
		initializeSCD();
		HAL_StartAppTimer(&periodicMeasurementTimer);
	break;
	
	case APP_CALL_FOR_READ_SCD_STATE:
		appstate=APP_NOTHING_STATE;
		callReadSCD();
		delaytimer(SCD_READ_DELAY_TIME, APP_READ_SCD_STATE);
	break;
	
	case APP_READ_SCD_STATE:
		appstate = APP_NOTHING_STATE;
		readSCD();
		delaytimer(SCD_READ_DELAY_TIME, APP_CALL_FOR_READ_TEMP_SHT_STATE);
	break;
	
	case APP_CALL_FOR_READ_TEMP_SHT_STATE:
		appstate=APP_NOTHING_STATE;
		callReadSHT(MES_TEMP);
		delaytimer(SCD_READ_DELAY_TIME, APP_READ_TEMP_SHT_STATE);
	break;
	
	case APP_READ_TEMP_SHT_STATE:
		appstate=APP_NOTHING_STATE;
		readSHT(MES_TEMP);
		delaytimer(SCD_READ_DELAY_TIME, APP_CALL_FOR_READ_RH_SHT_STATE);
	break;
	
	case APP_CALL_FOR_READ_RH_SHT_STATE:
		appstate=APP_NOTHING_STATE;
		callReadSHT(MES_RH);
		delaytimer(SCD_READ_DELAY_TIME, APP_READ_RH_SHT_STATE);
	break;
	
	case APP_READ_RH_SHT_STATE:
		appstate=APP_NOTHING_STATE;
		readSHT(MES_RH);
		delaytimer(SCD_READ_DELAY_TIME, APP_AUSGABE_STATE);
	break;
	
	case APP_AUSGABE_STATE:
		calculateOutputSCD();
		calculateOutputSHT();
		appWriteDataToUsart((uint8_t*)co2_output_SCD, sizeof(co2_output_SCD));
		appWriteDataToUsart((uint8_t*)t_output_SHT21, sizeof(t_output_SHT21));
		appWriteDataToUsart((uint8_t*)t_output_SHT21_sensorbytes, sizeof(t_output_SHT21_sensorbytes));
		appWriteDataToUsart((uint8_t*)rh_output_SHT21, sizeof(rh_output_SHT21));
		appWriteDataToUsart((uint8_t*)rh_output_SHT21_sensorbytes, sizeof(rh_output_SHT21_sensorbytes));
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
