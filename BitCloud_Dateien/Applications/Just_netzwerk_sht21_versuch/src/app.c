/**************************************************************************//**
  \file app.c

  \brief Basis-Anwendung.

  \author Markus Krau�e

Alles in Ordnung.

Wie auch zuvor ignorieren Sie keine der Kompiler Warnungen.

Ihre Calback-Funktion ben�tigt keinen R�ckgabewert, allerdings bekommt Sie vom Deskriptor einen Bool-Wert den Sie benutzen k�nnen. Wenn Sie die Funktion als void deklarieren und bool result als Parameter �bergeben, ist die Kompiler-Warnung nicht mehr vorhanden.

Des Weiteren denken Sie auch beim I2C-Deskriptor daran diesen nach Auslesen des Sensors zu schlie�en. Aktuell f�llt das nicht ins Gewicht, da Sie nur diesen Sensor auslesen. Als bald Sie aber mehrere Sensoren auslesen werden Sie Probleme bekommen, da ihr Sensor dann den Bus des I2C blockieren wird.


******************************************************************************/


#include <appTimer.h>
#include <zdo.h>
#include <app.h>
#include <adc.h>
#include <sysTaskManager.h>
#include <usartManager.h>
#include <i2cPacket.h>
#include <bspLeds.h>

#define Measure_T_SHT21 0xf3
#define Measure_RH_SHT21 0xf5
uint8_t tmp[] = "[{\"id\":1,\"SHT21\":{\"temperatur\":xxxxx,\"humidity\":xxxx}}]";

static HAL_AppTimer_t sendeTimer;
static HAL_AppTimer_t mesTimer;
static AppState_t appstate = APP_INIT_STATE;

static void initTimer(void);
static void sendeTimerFired(void);
static void measureTimerFired(void);
static HAL_I2cDescriptor_t i2cdescriptorcmd;
static HAL_I2cDescriptor_t i2cdescriptorrd;

bool result;
bool measurementSHT21neg;
bool measuretempsht21;
uint8_t sht21cmd;
uint8_t sht21data[2];
uint16_t sht21_rd;


int32_t vorkomma;
int32_t nachkomma;

uint8_t t_output_SHT21[] = "+xxx.xx degree Celsius \r\n";
uint8_t rh_output_SHT21[] = "+xxx.xx percent  relative Humidity \r\n";
uint8_t t_output_SHT21_sensorbytes[] = "0xXXXX sensor \r\n";

//Netzwerk
static uint8_t deviceType;
static ZDO_StartNetworkReq_t networkParams;

static SimpleDescriptor_t simpleDescriptor;
static APS_RegisterEndpointReq_t endPoint;

BEGIN_PACK
typedef struct _AppMessage_t{
	uint8_t header[APS_ASDU_OFFSET]; //APS header
	uint8_t data[55];
	uint8_t footer[APS_AFFIX_LENGTH - APS_ASDU_OFFSET]; // Footer
} PACK AppMessage_t;
END_PACK

static AppMessage_t transmitData;
APS_DataReq_t dataReq;

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

void APS_DataInd(APS_DataInd_t *indData){
	BSP_OnLed(LED_RED);
	//HAL_StartAppTimer(&receiveTimerLed);
	appWriteDataToUsart(indData->asdu,indData->asduLength);
	appWriteDataToUsart((uint8_t*)"\r\n",2);
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



static void APS_DataConf(APS_DataConf_t *confInfo){
	if (confInfo->status == APS_SUCCESS_STATUS){
		BSP_OnLed(LED_YELLOW);
		//HAL_StartAppTimer(&transmitTimerLed);
		appstate=APP_NOTHING_STATE;
		SYS_PostTask(APL_TASK_ID);
	}
}

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

static void callbackcmd(bool result){
	appstate=APP_NOTHING_STATE;
	if(!result){
		appWriteDataToUsart((uint8_t*)"Error: callbackcmd called with 0\r\n", sizeof("Error: callbackcmd called with 1\r\n")-1);
	}
	HAL_CloseI2cPacket(&i2cdescriptorcmd);
	HAL_StartAppTimer(&mesTimer);
	SYS_PostTask(APL_TASK_ID);
}

static void callbackrd(bool result){
	appstate=APP_AUSGABE_STATE;
	if(!result){
		appWriteDataToUsart((uint8_t*)"Error: callbackrd called with 0\r\n", sizeof("Error: callbackrd called with 1\r\n")-1);
	}
	HAL_CloseI2cPacket(&i2cdescriptorrd);
	SYS_PostTask(APL_TASK_ID);
}




static HAL_I2cDescriptor_t i2cdescriptorcmd={						
	.tty = TWI_CHANNEL_0,
	.clockRate = I2C_CLOCK_RATE_62,
	.f = callbackcmd,															
	.id = 0x40,
	.data = &sht21cmd,
	.length = 1,
	.lengthAddr = HAL_NO_INTERNAL_ADDRESS
};

static HAL_I2cDescriptor_t i2cdescriptorrd={
	.tty = TWI_CHANNEL_0,
	.clockRate = I2C_CLOCK_RATE_62,
	.f = callbackrd,
	.id = 0x40,
	.data = sht21data,
	.length = 2,
	.lengthAddr = HAL_NO_INTERNAL_ADDRESS
};



void calculateOutputSHT21(){
	uint64_t conversionfactor;
	uint64_t correctionoffset;
	if(measuretempsht21){
		conversionfactor = 26812744140625; // Datasheetformula: -46.85 + 175.72 * sensordata/65536 :: conversionfactor is 175.72/65536 scaled by 10^16 to avoid floating numbers.
		correctionoffset = 468500000000000000; // -46.85 scaled by 10^16 and inverted new formula: conversionfactor*sensordata - correctionoffset
	}else{
		conversionfactor = 19073486328125; //Datasheetformula: -6 + 125 * sensordata/65536 :: conversionfactor is 125/65536 scaled by 10^16 to avoid floating numbers.
		correctionoffset = 60000000000000000; // -6 scaled by 10^16 and inverted new formula: conversionfactor*sensordata - correctionoffset
	}
	sht21_rd = sht21data[0];
	sht21_rd <<= 8;
	sht21_rd |= sht21data[1]; 
	
	uint64_t measurementsht21 = conversionfactor * sht21_rd;
	if(measurementsht21 < correctionoffset){
		measurementsht21 = correctionoffset - measurementsht21;
		measurementSHT21neg = true;
	}else{
		measurementsht21 = measurementsht21 - correctionoffset;
		measurementSHT21neg = false;
	}
		
	uint32_t vorkomma = measurementsht21/10000000000000000;
	uint32_t nachkomma = measurementsht21%10000000000000000;
	if (measurementSHT21neg)
	{
		if(measuretempsht21) t_output_SHT21[0] = 0x2d;
		else rh_output_SHT21[0] = 0x2d;
	}else{
		if(measuretempsht21) t_output_SHT21[0] = 0x2b;
		else rh_output_SHT21[0] = 0x2b;
	}
	if(measuretempsht21){
		uint32_to_str((uint8_t *) t_output_SHT21, sizeof(t_output_SHT21),vorkomma, 1, 3);
		uint32_to_str((uint8_t *) t_output_SHT21, sizeof(t_output_SHT21),nachkomma, 5, 2);
		
	}else{
		uint32_to_str((uint8_t *) rh_output_SHT21, sizeof(rh_output_SHT21),vorkomma, 1, 3);
		uint32_to_str((uint8_t *) rh_output_SHT21, sizeof(rh_output_SHT21),nachkomma, 5, 2);
	}
	uint16_to_hexstr((uint8_t *)t_output_SHT21_sensorbytes, sizeof(t_output_SHT21_sensorbytes), sht21_rd, 2);
	}
		
		


static void initTimer(){
	mesTimer.interval	= APP_MES_INTERVAL;
	mesTimer.mode		= TIMER_ONE_SHOT_MODE;
	mesTimer.callback	= measureTimerFired;
	sendeTimer.interval = APP_SENDE_INTERVAL;      // Timer interval
	sendeTimer.mode     = TIMER_REPEAT_MODE;       // Timer-Mode
	sendeTimer.callback = sendeTimerFired;         // Callback function
	HAL_StartAppTimer(&sendeTimer);                // Start sendeTimer
}

static void sendeTimerFired(){
	appstate=APP_WRITE_STATE;
	SYS_PostTask(APL_TASK_ID);
}

static void measureTimerFired(){
	appstate=APP_READ_STATE;
	SYS_PostTask(APL_TASK_ID);
}

void APL_TaskHandler(void){
switch(appstate){
	case APP_INIT_STATE:
		appInitUsartManager();
		initTimer();
		BSP_OpenLeds();
		appstate=APP_STARTJOIN_NETWORK;
		SYS_PostTask(APL_TASK_ID);
		//appstate=APP_NOTHING_STATE;
	break;
	
	case APP_STARTJOIN_NETWORK:
		networkParams.ZDO_StartNetworkConf = ZDO_StartNetworkConf;
		ZDO_StartNetworkReq(&networkParams);
		appstate=APP_INIT_ENDPOINT;
	break;
	
	case APP_INIT_ENDPOINT:
		initEndpoint();
		#if CS_DEVICE_TYPE == DEV_TYPE_COORDINATOR
		appstate=APP_NOTHING_STATE;
	
		#else
		appstate=APP_INIT_TRANSMITDATA;
		#endif
		SYS_PostTask(APL_TASK_ID);
	break;
	
	case APP_INIT_TRANSMITDATA:
		initTransmitData();
		appstate=APP_NOTHING_STATE;
		//HAL_StartAppTimer(&transmitTimer);
		SYS_PostTask(APL_TASK_ID);
	break;
	
	case APP_READ_STATE:
	if (-1 == HAL_OpenI2cPacket(&i2cdescriptorrd)){
		appWriteDataToUsart((uint8_t*)"open fail\r\n", sizeof("open fail\r\n")-1);
	}
	if (-1 == HAL_ReadI2cPacket(&i2cdescriptorrd)){
		appWriteDataToUsart((uint8_t*)"read fail\r\n", sizeof("read fail\r\n")-1);
	}
		appstate=APP_AUSGABE_STATE;
	break;
	
	case APP_WRITE_STATE:
	if(measuretempsht21){
		sht21cmd = Measure_T_SHT21;
	}else{
		sht21cmd = Measure_RH_SHT21;
	}
		
		if (-1 == HAL_OpenI2cPacket(&i2cdescriptorcmd)){
			appWriteDataToUsart((uint8_t*)"open fail\r\n", sizeof("open fail\r\n")-1);
		}
		
		if (-1 == HAL_WriteI2cPacket(&i2cdescriptorcmd)){
			appWriteDataToUsart((uint8_t*)"write fail\r\n", sizeof("write fail\r\n")-1);
		}
		appstate=APP_NOTHING_STATE;
	break;
	
	case APP_AUSGABE_STATE:
		BSP_OffLed(LED_YELLOW);
		int32_t temp = -2500;
		uint16_t hum = 5400;
		
		int32_to_str(tmp, sizeof(tmp), temp, 31, 5);
		uint32_to_str(tmp, sizeof(tmp), hum, 48, 4);
		
		int16_t size = sizeof(tmp)-1;
		for(int16_t i = 0; i <= size; i++ ){
			transmitData.data[i] = tmp[i];
		}
		
		calculateOutputSHT21();
		if(measuretempsht21){
		appWriteDataToUsart((uint8_t*)t_output_SHT21, sizeof(t_output_SHT21));
		measuretempsht21 = false;
		}else{
		appWriteDataToUsart((uint8_t*)rh_output_SHT21, sizeof(rh_output_SHT21));
		measuretempsht21 = true;
		}
		appWriteDataToUsart((uint8_t*)t_output_SHT21_sensorbytes, sizeof(t_output_SHT21_sensorbytes));
		
		
		APS_DataReq(&dataReq);
		
		
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
