/**************************************************************************//**
  \file app.c

  \brief Basis-Anwendung.

  \author Markus Krau�e

******************************************************************************/


#include <appTimer.h>
#include <zdo.h>
#include <app.h>
#include <adc.h>
#include <sysTaskManager.h>
#include <usartManager.h>
#include <i2cPacket.h>
#include <bspLeds.h>

uint8_t appstate = APP_STARTUP_STATE;
uint8_t next_appstate = APP_NOTHING_STATE;

BEGIN_PACK
typedef struct _AppMessage_t{
	uint8_t header[APS_ASDU_OFFSET]; //APS header
	uint8_t data[55]; // muss noch angepasst werden
	uint8_t footer[APS_AFFIX_LENGTH - APS_ASDU_OFFSET]; // Footer
} PACK AppMessage_t;
END_PACK

static uint8_t deviceType;
static void ZDO_StartNetworkConf(ZDO_StartNetworkConf_t *confirmInfo);
static ZDO_StartNetworkReq_t networkParams;

static SimpleDescriptor_t simpleDescriptor;
static APS_RegisterEndpointReq_t endPoint;
static void initEndpoint(void);
void APS_DataInd(APS_DataInd_t *indData);

static AppMessage_t transmitData;
APS_DataReq_t dataReq;
static void APS_DataConf(APS_DataConf_t *confInfo);
static void initTransmitData(void);

/************
SCD-TIMER
************/
static HAL_AppTimer_t periodicMeasurementTimer;
static HAL_AppTimer_t delayTimer;

static HAL_AppTimer_t receiveTimerLed;
static HAL_AppTimer_t transmitTimerLed;
static HAL_AppTimer_t transmitTimer;
static void receiveTimerLedFired(void);
static void transmitTimerLedFired(void);
static void transmitTimerFired(void);


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
uint8_t co2_output_SCD[] = " XXXXXppmCO2scd\r\n";

bool result;
bool tempNegativ;
uint8_t sht21cmd;
uint8_t sht21data[2];
uint16_t sht21_rd_tmp;
uint16_t sht21_rd_rh;
int32_t sht21_tempv;
int32_t sht21_tempn;
int32_t sht21_rhv;
int32_t sht21_rhn;
int32_t vorkomma;
int32_t nachkomma;

	uint32_t vorkommatmp;
	uint32_t nachkommatmp;
	uint32_t vorkommarh;
	uint32_t nachkommarh;

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
	
	vorkommatmp = temperature/10000000000000000;
	nachkommatmp = temperature%10000000000000000;
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
	
	vorkommarh = relativeHumidity/10000000000000000;
	nachkommarh = relativeHumidity%10000000000000000;
	
	
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
	
	transmitTimer.interval= 3000;
	transmitTimer.mode= TIMER_REPEAT_MODE;
	transmitTimer.callback=transmitTimerFired;
	
	transmitTimerLed.interval= 500;
	transmitTimerLed.mode= TIMER_ONE_SHOT_MODE;
	transmitTimerLed.callback=transmitTimerLedFired;
	
	receiveTimerLed.interval= 500;
	receiveTimerLed.mode= TIMER_ONE_SHOT_MODE;
	receiveTimerLed.callback=receiveTimerLedFired;
	
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

static void transmitTimerLedFired(void){
	BSP_OffLed(LED_YELLOW);
}
static void receiveTimerLedFired(void){
	BSP_OffLed(LED_RED);
}
static void transmitTimerFired(void){
	appstate=APP_TRANSMIT;
	SYS_PostTask(APL_TASK_ID);
}

/***********************************************
Transmit
***********************************************/
static void initTransmitData(void){
	dataReq.profileId=1;
	dataReq.dstAddrMode =APS_SHORT_ADDRESS;
	dataReq.dstAddress.shortAddress= CPU_TO_LE16(0);
	dataReq.dstEndpoint =1;
	dataReq.asdu=transmitData.data;
	dataReq.asduLength=sizeof(transmitData.data);
	dataReq.srcEndpoint = 1;
	dataReq.APS_DataConf=APS_DataConf;
}


static void APS_DataConf(APS_DataConf_t *confInfo){
	if (confInfo->status == APS_SUCCESS_STATUS){
		BSP_OnLed(LED_YELLOW);
		HAL_StartAppTimer(&transmitTimerLed);
		appstate=APP_NOTHING_STATE;
		SYS_PostTask(APL_TASK_ID);
	}
}

static void initEndpoint(void){
	simpleDescriptor.AppDeviceId = 1;
	simpleDescriptor.AppProfileId = 1;
	simpleDescriptor.endpoint = 1;
	simpleDescriptor.AppDeviceVersion = 1;
	endPoint.simpleDescriptor= &simpleDescriptor;
	endPoint.APS_DataInd = APS_DataInd;
	APS_RegisterEndpointReq(&endPoint);
}

void APS_DataInd(APS_DataInd_t *indData){
	BSP_OnLed(LED_RED);
	HAL_StartAppTimer(&receiveTimerLed);
	appWriteDataToUsart(indData->asdu,indData->asduLength);
	appWriteDataToUsart((uint8_t*)"\r\n",2);
}

void ZDO_StartNetworkConf(ZDO_StartNetworkConf_t *confirmInfo){
	if (ZDO_SUCCESS_STATUS == confirmInfo->status){
		CS_ReadParameter(CS_DEVICE_TYPE_ID,&deviceType);
		if(deviceType==DEV_TYPE_COORDINATOR){
			appWriteDataToUsart((uint8_t*)"Coordinator\r\n", sizeof("Coordinator\r\n")-1);
		}
		BSP_OnLed(LED_YELLOW);
		
		}else{
		appWriteDataToUsart((uint8_t*)"Error\r\n",sizeof("Error\r\n")-1);
	}
	SYS_PostTask(APL_TASK_ID);
}

static void fill_transmit_data(void){
	transmitData.data[0]='3';
		uint8_t tmp[] = "1SHT;XXXXX;XXXX;SCD;XXXXX;XXXXX;XXXXX";
		//					  5     11       20    26    32  
		//bool tempNegativ;
		
		uint32_to_str(tmp, sizeof(tmp),vorkommatmp, 6, 2);
		uint32_to_str(tmp, sizeof(tmp),nachkommatmp, 8, 2);
		uint32_to_str(tmp, sizeof(tmp),vorkommarh, 11, 2);
		uint32_to_str(tmp, sizeof(tmp),nachkommarh, 13, 2);
		if (tempNegativ)
		{
			tmp[5] = 0x2d;
			}else{
			tmp[5] = 0x2b;
		}
		uint32_to_str(tmp, sizeof(tmp), scd_rd_temp, 21, 4);
		uint16_to_hexstr(tmp, sizeof(tmp), scd_rd_rh, 26);
		uint32_to_str(tmp, sizeof(tmp), scd_rd_co2, 32 ,4);	
		/*
		if (tempNegativ)
		{
			tmp[5] = 0x2d;
			}else{
			tmp[5] = 0x2b;
		}
		*/
		
	
		int16_t size = sizeof(tmp)-1;
		for(int16_t i = 0; i <= size; i++ ){
			transmitData.data[i] = tmp[i];
		}
}


/***********************************************
Zustandsautomat
***********************************************/

void APL_TaskHandler(void){
switch(appstate){
	case APP_STARTUP_STATE:
		appstate=APP_NOTHING_STATE;
		appInitUsartManager();
		BSP_OpenLeds();
		initTimer();
		appstate = APP_STARTJOIN_NETWORK;
		SYS_PostTask(APL_TASK_ID);
	break;
	
	case APP_STARTJOIN_NETWORK:
		BSP_OnLed(LED_GREEN);
		networkParams.ZDO_StartNetworkConf = ZDO_StartNetworkConf;
		ZDO_StartNetworkReq(&networkParams);
		appstate=APP_INIT_ENDPOINT;
		SYS_PostTask(APL_TASK_ID);
	break;
	
	case APP_INIT_ENDPOINT:
		initEndpoint();
		appstate=APP_INIT_TRANSMITDATA;
		SYS_PostTask(APL_TASK_ID);
	break;
	
	case APP_INIT_TRANSMITDATA:
		initTransmitData();
		appstate=APP_NOTHING_STATE;
		HAL_StartAppTimer(&transmitTimer);
		SYS_PostTask(APL_TASK_ID);
	break;
	
	case APP_TRANSMIT:
		fill_transmit_data();
		APS_DataReq(&dataReq);
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
