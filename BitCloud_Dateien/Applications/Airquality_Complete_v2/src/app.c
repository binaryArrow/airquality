/***************************************************************************
  \file app.c

  \brief Basis-Anwendung.

  \author Markus Krau�e, Achim Glaesmann, Lucas Merkert, Friedrich
  ******************************************************************************/
  /*>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>*/
  /*>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>*/
  // Netzwerkcode von Friedrich
  /*<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<*/
  /*<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<*/
  /*(((((((((((((((((((((((((((((((((((((((((((((*/
  /*(((((((((((((((((((((((((((((((((((((((((((((*/
  // CCS811 Code von Lucas
  /*)))))))))))))))))))))))))))))))))))))))))))))*/
  /*)))))))))))))))))))))))))))))))))))))))))))))*/

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

/*>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>*/
/*>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>*/
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

static HAL_AppTimer_t receiveTimerLed;
static HAL_AppTimer_t transmitTimerLed;
static void receiveTimerLedFired(void);
static void transmitTimerLedFired(void);
/*<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<*/
/*<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<*/


static HAL_AppTimer_t periodicMeasurementTimer;
static HAL_AppTimer_t delayTimer;
static void delaytimer(uint16_t, uint8_t);

static void initTimer();

static void periodicMeasurementTimerComplete();
static void delayTimerComplete();
/*(((((((((((((((((((((((((((((((((((((((((((((*/ //Lucas und Friedrich darauf ansprechen, dass sie die Funktionen hier schon deklarieren sollen.
/*(((((((((((((((((((((((((((((((((((((((((((((*/
	static void calculateCCS();
	static void changeCCSAppstate();
	static void readCCSHWIDReg();
	static void readccsResultReg();
	static void readccsStatusReg();
	static void resetCCS();
	static void writeCCSHWIDReg();
	static void writeccsResultReg();
	static void writeccsStatusReg();
	static void writeMeasModeCCS();
	
	
/*)))))))))))))))))))))))))))))))))))))))))))))*/
/*)))))))))))))))))))))))))))))))))))))))))))))*/
//Calculate
static void calculateOutputSCD();
static void calculateOutputSHT();

uint16_t CCS_co2;
uint16_t CCS_tvoc;


uint32_t SHT_rh_vorkomma;
uint32_t SHT_rh_nachkomma;
uint32_t SHT_tmp_vorkomma;
uint32_t SHT_tmp_nachkomma;
bool result;
bool tempNegativ;

//I2C
//CCS
bool checkHWID = false;
bool checkStatus = false;
uint8_t ccs5Byte[5];
uint8_t ccsOneByte;
uint8_t ccsTwoByte[2];
uint8_t ccs4Byte[4];

static HAL_I2cDescriptor_t i2cdescriptorCCSOneByte;
static HAL_I2cDescriptor_t i2cdescriptorCCSTwoByte;
static HAL_I2cDescriptor_t i2cdescriptorCCS4Byte;
static HAL_I2cDescriptor_t i2cdescriptorCCS5Byte;

//SHT SCD
static void resetSCD();
static void initializeSCD();
static void callReadSCD();
static void readSCD();
static void callReadSHT(uint8_t);
static void readSHT(uint8_t);

static void callbackcmdSCD(bool);
static void callbackrdSCD(bool);
static void callbackcmdSHT(bool);
static void callbackrdSHT(bool);

static void callbackCCSOneByte(bool result);
static void callbackCCSTwoByte(bool result);
static void callbackCCS4Byte(bool result);
static void callbackCCS5Byte(bool result);

static HAL_I2cDescriptor_t i2cdescriptorcmdSCD;
static HAL_I2cDescriptor_t i2cdescriptorrdSCD;
static HAL_I2cDescriptor_t i2cdescriptorcmdSHT;
static HAL_I2cDescriptor_t i2cdescriptorrdSHT;

uint8_t scdcmd[2];
uint8_t scddata[9];
uint16_t scd_rd_co2;
//uint16_t scd_rd_temp;		//>> uint16_t
//uint16_t scd_rd_rh;		//>> uint16_t
//neu
int32_t scd_rd_temp;		//>> uint16_t 
uint32_t scd_rd_rh;			//>> uint16_t
int32_t scd_temp;
uint32_t scd_rh;



uint8_t sht21cmd;
uint8_t sht21data[2];
uint16_t sht21_rd_tmp;
uint16_t sht21_rd_rh;

//OUTPUT
uint8_t t_output_SHT21[] = "+xxx.xx degree Celsius SHT \r\n";
uint8_t t_output_SHT21_sensorbytes[] = "0xXXXX sensor SHT Temp \r\n";
uint8_t rh_output_SHT21[] = "+xx.xx percent relative Humidity SHT \r\n";
uint8_t rh_output_SHT21_sensorbytes[] = "0xXXXX sensor SHT rh\r\n";

uint8_t co2_output_SCD[] = " XXXXX ppm CO2 SCD\r\n";
uint8_t t_output_SCD[] = " XXXXX degree Celsius SCD\r\n";
uint8_t rh_output_SCD[] = " XXXXX relative Humidity  SCD\r\n";

uint8_t tvoc_output_CCS[] = " XXXXX ppb TVOC CCS\r\n";
uint8_t co2_output_CCS[] = " XXXXX ppm CO2 CCS\r\n";


/***********************************************
Zustandsautomat
***********************************************/

void APL_TaskHandler(void){
	switch(appstate){
		case APP_STARTUP_STATE:
		appstate=APP_NOTHING_STATE;
		appInitUsartManager();
		initTimer();
		/*>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>*/
		/*>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>*/
		BSP_OpenLeds();
		appstate = APP_STARTJOIN_NETWORK;	
		SYS_PostTask(APL_TASK_ID);
		break;
		
		case APP_STARTJOIN_NETWORK:
		BSP_OnLed(LED_GREEN);
		networkParams.ZDO_StartNetworkConf = ZDO_StartNetworkConf;
		ZDO_StartNetworkReq(&networkParams);
		appstate=APP_INIT_ENDPOINT;
		appWriteDataToUsart((uint8_t*)"StartJoin Network\r\n", sizeof("StartJoin Network\r\n")-1);
		SYS_PostTask(APL_TASK_ID);
		break;
		
		case APP_INIT_ENDPOINT:
		initEndpoint();
		appstate=APP_INIT_TRANSMITDATA;
		appWriteDataToUsart((uint8_t*)"INIT ENDPOINT\r\n", sizeof("INIT ENDPOINT\r\n")-1);
		SYS_PostTask(APL_TASK_ID);
		break;
		
		case APP_INIT_TRANSMITDATA:
		initTransmitData();
		appstate=APP_NOTHING_STATE;
		delaytimer(SCD_STARTUP_TIME, APP_RESET_CCS_SW_STATE);
		break;
		
		case APP_TRANSMIT:
		appWriteDataToUsart((uint8_t*)"TRANSMIT\r\n", sizeof("TRANSMIT\r\n")-1);
		
		
		transmitData.data[0]='3';
		uint8_t tmp[] = "1SHT;XXXXX;XXXX;SCD;XXXXX;XXXX;XXXX;CCS;XXXX;XXXX";
		//					  5	    11       20    26   31       40   45
		uint32_to_str(tmp, sizeof(tmp),SHT_tmp_vorkomma, 6, 2);
		uint32_to_str(tmp, sizeof(tmp),SHT_tmp_nachkomma, 8, 2);
		uint32_to_str(tmp, sizeof(tmp),SHT_rh_vorkomma, 11, 2);
		uint32_to_str(tmp, sizeof(tmp),SHT_rh_nachkomma, 13, 2);
		if (tempNegativ)
		{
			tmp[5] = 0x2d;
			}else{
			tmp[5] = 0x2b;
		}
		/*
		uint16_t scd_rd_co2;
		uint16_t scd_rd_temp;
		uint16_t scd_rd_rh;
		int32_t scd_temp;
		uint32_t scd_rh;
		*/
		int32_to_str(tmp, sizeof(tmp),scd_temp, 20, 5);
		uint32_to_str(tmp, sizeof(tmp),scd_rh, 26, 4);
		uint32_to_str(tmp, sizeof(tmp),scd_rd_co2, 31, 4);
		
		/*
		uint16_t CCS_co2;
		uint16_t CCS_tvoc;
		*/
		uint32_to_str(tmp, sizeof(tmp),CCS_co2, 40, 4);
		uint32_to_str(tmp, sizeof(tmp),CCS_tvoc, 45, 4);
		
		
		int16_t size = sizeof(tmp)-1;
		for(int16_t i = 0; i <= size; i++ ){
			transmitData.data[i] = tmp[i];
		}
		APS_DataReq(&dataReq);
		break;
		/*<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<*/
		/*<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<*/
		  /*(((((((((((((((((((((((((((((((((((((((((((((*/
		  /*(((((((((((((((((((((((((((((((((((((((((((((*/
		case APP_RESET_CCS_SW_STATE:
			appstate=APP_NOTHING_STATE;
			resetCCS();
			delaytimer(CCS_MIN_DELAY, APP_CCS_HW_ID_WRITE_REG_STATE);
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
			delaytimer(CCS_DRIVE_STATUS_DELAY, APP_CCS_WRITE_STATUS_REG_STATE);
		break;
		
		case APP_CCS_WRITE_STATUS_REG_STATE:
			appstate=APP_NOTHING_STATE;
			writeccsStatusReg();
			delaytimer(CCS_MIN_DELAY, APP_CCS_READ_STATUS_REG_STATE);
		break;
		
		case APP_CCS_READ_STATUS_REG_STATE:
			appstate=APP_NOTHING_STATE;
			readccsStatusReg();
			delaytimer(CCS_MIN_DELAY, APP_RESET_SCD_STATE);
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
		  /*)))))))))))))))))))))))))))))))))))))))))))))*/
		  /*)))))))))))))))))))))))))))))))))))))))))))))*/
		  
		case APP_RESET_SCD_STATE:
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
		delaytimer(SCD_READ_DELAY_TIME, APP_CCS_WRITE_RESULT_REG_STATE);
		break;
		
		case APP_AUSGABE_STATE:
		appstate=APP_NOTHING_STATE;
		calculateOutputSCD();
		calculateOutputSHT();
		calculateCCS();
		appWriteDataToUsart((uint8_t*)co2_output_CCS, sizeof(co2_output_CCS));
		appWriteDataToUsart((uint8_t*)tvoc_output_CCS, sizeof(tvoc_output_CCS));
		
		appWriteDataToUsart((uint8_t*)co2_output_SCD, sizeof(co2_output_SCD));
		appWriteDataToUsart((uint8_t*)t_output_SCD, sizeof(t_output_SCD));
		appWriteDataToUsart((uint8_t*)rh_output_SCD, sizeof(rh_output_SCD));
		
		appWriteDataToUsart((uint8_t*)t_output_SHT21, sizeof(t_output_SHT21));
		appWriteDataToUsart((uint8_t*)rh_output_SHT21, sizeof(rh_output_SHT21));
		//appWriteDataToUsart((uint8_t*)t_output_SHT21_sensorbytes, sizeof(t_output_SHT21_sensorbytes));
		//appWriteDataToUsart((uint8_t*)rh_output_SHT21_sensorbytes, sizeof(rh_output_SHT21_sensorbytes));
		delaytimer(CCS_MIN_DELAY, APP_TRANSMIT);
		break;
		
		case APP_NOTHING_STATE:
		break;
		
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
 /*>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>*/
 /*>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>*/
	transmitTimerLed.interval= 500;
	transmitTimerLed.mode= TIMER_ONE_SHOT_MODE;
	transmitTimerLed.callback=transmitTimerLedFired;
	
	receiveTimerLed.interval= 500;
	receiveTimerLed.mode= TIMER_ONE_SHOT_MODE;
	receiveTimerLed.callback=receiveTimerLedFired;
  /*<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<*/
  /*<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<*/
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
 /*>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>*/
 /*>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>*/
static void transmitTimerLedFired(void){
	BSP_OffLed(LED_YELLOW);
}
static void receiveTimerLedFired(void){
	BSP_OffLed(LED_RED);
}
  /*<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<*/
  /*<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<*/

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
I2C-Methods
***********************************************/
/************
CCS-I2C
************/
static void resetCCS(){
	
	ccs5Byte[0] = (CCS_RESET_SW_CMD & 0xFF00000000) >> 32;
	ccs5Byte[1] = (CCS_RESET_SW_CMD & 0x00FF000000) >> 24;
	ccs5Byte[2] = (CCS_RESET_SW_CMD & 0x0000FF0000) >> 16;
	ccs5Byte[3] = (CCS_RESET_SW_CMD & 0x000000FF00) >> 8;
	ccs5Byte[4] = CCS_RESET_SW_CMD & 0x00000000FF;

	if (-1 == HAL_OpenI2cPacket(&i2cdescriptorCCS5Byte)){
		appWriteDataToUsart((uint8_t*)"open fail ccs reset\r\n", sizeof("open fail ccs reset\r\n")-1);
	}
	if (-1 == HAL_WriteI2cPacket(&i2cdescriptorCCS5Byte)){
		appWriteDataToUsart((uint8_t*)"write fail ccs reset\r\n", sizeof("write fail ccs reset\r\n")-1);
	}
	appWriteDataToUsart((uint8_t*)"CCS Reset \r\n", sizeof("CCS Reset \r\n")-1);

};

static void writeCCSHWIDReg(){
	ccsOneByte = CCS_HWID_REG;
	if (-1 == HAL_OpenI2cPacket(&i2cdescriptorCCSOneByte)){
		appWriteDataToUsart((uint8_t*)"open fail ccs hwid\r\n", sizeof("open fail ccs hwid\r\n")-1);
	}
	if (-1 == HAL_WriteI2cPacket(&i2cdescriptorCCSOneByte)){
		appWriteDataToUsart((uint8_t*)"write fail ccs hwid\r\n", sizeof("write fail ccs hwid\r\n")-1);
	}
	appWriteDataToUsart((uint8_t*)"CCS hwid \r\n", sizeof("CCS hwid \r\n")-1);
}

static void readCCSHWIDReg(){
	checkHWID = true;
	if (-1 == HAL_OpenI2cPacket(&i2cdescriptorCCSOneByte)){
		appWriteDataToUsart((uint8_t*)"open fail ccs hwid\r\n", sizeof("open fail ccs hwid\r\n")-1);
	}
	if (-1 == HAL_ReadI2cPacket(&i2cdescriptorCCSOneByte)){
		appWriteDataToUsart((uint8_t*)"read fail ccs hwid\r\n", sizeof("write fail ccs hwid\r\n")-1);
	}
	appWriteDataToUsart((uint8_t*)"CCS hwid read \r\n", sizeof("CCS hwid read\r\n")-1);
}

static void changeCCSAppstate(){
	ccsOneByte = CCS_BOOTLOADER_APPSTATE;
	if (-1 == HAL_OpenI2cPacket(&i2cdescriptorCCSOneByte)){
		appWriteDataToUsart((uint8_t*)"open fail ccs bootloader\r\n", sizeof("open fail ccs bootloader\r\n")-1);
	}
	if (-1 == HAL_WriteI2cPacket(&i2cdescriptorCCSOneByte)){
		appWriteDataToUsart((uint8_t*)"write fail ccs bootloader\r\n", sizeof("write fail ccs bootloader\r\n")-1);
	}
	appWriteDataToUsart((uint8_t*)"CCS bootloader \r\n", sizeof("CCS bootloader \r\n")-1);
}
static void writeMeasModeCCS(){
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

static void writeccsStatusReg(){
	ccsOneByte = CCS_STATUS_REG;
	if (-1 == HAL_OpenI2cPacket(&i2cdescriptorCCSOneByte)){
		appWriteDataToUsart((uint8_t*)"open fail ccs status reg\r\n", sizeof("open fail ccs status reg\r\n")-1);
	}
	if (-1 == HAL_WriteI2cPacket(&i2cdescriptorCCSOneByte)){
		appWriteDataToUsart((uint8_t*)"write fail ccs status reg\r\n", sizeof("write fail ccs status reg\r\n")-1);
	}
	appWriteDataToUsart((uint8_t*)"CCS status reg \r\n", sizeof("CCS status reg \r\n")-1);
}
static void readccsStatusReg(){
	checkStatus = true;
	if (-1 == HAL_OpenI2cPacket(&i2cdescriptorCCSOneByte)){
		appWriteDataToUsart((uint8_t*)"open fail ccs status reg\r\n", sizeof("open fail ccs status reg\r\n")-1);
	}
	if (-1 == HAL_ReadI2cPacket(&i2cdescriptorCCSOneByte)){
		appWriteDataToUsart((uint8_t*)"write fail ccs status reg\r\n", sizeof("write fail ccs status reg\r\n")-1);
	}
	appWriteDataToUsart((uint8_t*)"CCS status reg \r\n", sizeof("CCS status reg \r\n")-1);
}

static void writeccsResultReg(){
	ccsOneByte = CCS_RESULT_REG;
	if (-1 == HAL_OpenI2cPacket(&i2cdescriptorCCSOneByte)){
		appWriteDataToUsart((uint8_t*)"open fail ccs result reg\r\n", sizeof("open fail ccs result reg\r\n")-1);
	}
	if (-1 == HAL_WriteI2cPacket(&i2cdescriptorCCSOneByte)){
		appWriteDataToUsart((uint8_t*)"write fail ccs result reg\r\n", sizeof("write fail ccs result reg\r\n")-1);
	}
	appWriteDataToUsart((uint8_t*)"CCS result reg \r\n", sizeof("CCS result reg \r\n")-1);
}

static void readccsResultReg(){
	if (-1 == HAL_OpenI2cPacket(&i2cdescriptorCCS4Byte)){
		appWriteDataToUsart((uint8_t*)"open fail ccs read data\r\n", sizeof("open fail ccs read data\r\n")-1);
	}
	if (-1 == HAL_ReadI2cPacket(&i2cdescriptorCCS4Byte)){
		appWriteDataToUsart((uint8_t*)"write fail ccs read data\r\n", sizeof("write fail ccs sread data\r\n")-1);
	}
	appWriteDataToUsart((uint8_t*)"CCS read data \r\n", sizeof("CCS read data \r\n")-1);
}

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
		sht21cmd = SHT21_MES_T_CMD;
		}else if(mode == MES_RH){
		sht21cmd = SHT21_MES_RH_CMD;
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
Calculation-Methods
***********************************************/
/************
CCS-CALCULATION
************/
static void calculateCCS(){
	CCS_co2 = (ccs4Byte[0] << 8) | ccs4Byte[1];
	
	uint32_to_str((uint8_t *) co2_output_CCS, sizeof(co2_output_CCS),CCS_co2, 1, 5);
	
	CCS_tvoc = (ccs4Byte[2] << 8) | ccs4Byte[3];
	
	uint32_to_str((uint8_t *) tvoc_output_CCS, sizeof(tvoc_output_CCS),CCS_tvoc, 1, 5);
}

/************
SCD-CALCULATION
************/
static void calculateOutputSCD(){
	scd_rd_co2 = scddata[0];
	scd_rd_co2 <<= 8;
	scd_rd_co2 |= scddata[1];
	
	scd_rd_temp = scddata[3];
	scd_rd_temp <<= 8;
	scd_rd_temp |= scddata[4];
	scd_temp = (-4500. + (17500. * (scd_rd_temp/65536.)));
	
	scd_rd_rh = scddata[6];
	scd_rd_rh <<= 8;
	scd_rd_rh |= scddata[7];
	scd_rh = (10000. * (scd_rd_rh/65536.));
	
	uint32_to_str((uint8_t *) co2_output_SCD, sizeof(co2_output_SCD),scd_rd_co2, 1, 5);
	int32_to_str((uint8_t *) t_output_SCD, sizeof(t_output_SCD),scd_temp, 1, 5);
	uint32_to_str((uint8_t *) rh_output_SCD, sizeof(rh_output_SCD),scd_rh, 1, 5);
}

/************
SHT-CALCULATION
************/
static void calculateOutputSHT(){
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
	
	SHT_tmp_vorkomma = temperature/10000000000000000;
	SHT_tmp_nachkomma = temperature%10000000000000000;
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
	
	SHT_rh_vorkomma = relativeHumidity/10000000000000000;
	SHT_rh_nachkomma = relativeHumidity%10000000000000000;
	
	
	uint32_to_str((uint8_t *) t_output_SHT21, sizeof(t_output_SHT21),SHT_tmp_vorkomma, 1, 3);
	uint32_to_str((uint8_t *) t_output_SHT21, sizeof(t_output_SHT21),SHT_tmp_nachkomma, 5, 2);
	uint16_to_hexstr((uint8_t *)t_output_SHT21_sensorbytes, sizeof(t_output_SHT21_sensorbytes), sht21_rd_tmp, 2);
	
	uint32_to_str((uint8_t *) rh_output_SHT21, sizeof(rh_output_SHT21),SHT_rh_vorkomma, 1, 2);
	uint32_to_str((uint8_t *) rh_output_SHT21, sizeof(rh_output_SHT21),SHT_rh_nachkomma, 4, 2);
	uint16_to_hexstr((uint8_t *)rh_output_SHT21_sensorbytes, sizeof(rh_output_SHT21_sensorbytes), sht21_rd_rh, 2);
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
