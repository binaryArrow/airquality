/**************************************************************************//**
  \file app.c

  \brief Basis-Anwendung.

  \author Markus Krauße

Alles in Ordnung.

Wie auch zuvor ignorieren Sie keine der Kompiler Warnungen.

Ihre Calback-Funktion benötigt keinen Rückgabewert, allerdings bekommt Sie vom Deskriptor einen Bool-Wert den Sie benutzen können. Wenn Sie die Funktion als void deklarieren und bool result als Parameter übergeben, ist die Kompiler-Warnung nicht mehr vorhanden.

Des Weiteren denken Sie auch beim I2C-Deskriptor daran diesen nach Auslesen des Sensors zu schließen. Aktuell fällt das nicht ins Gewicht, da Sie nur diesen Sensor auslesen. Als bald Sie aber mehrere Sensoren auslesen werden Sie Probleme bekommen, da ihr Sensor dann den Bus des I2C blockieren wird.


******************************************************************************/


#include <appTimer.h>
#include <zdo.h>
#include <app.h>
#include <adc.h>
#include <sysTaskManager.h>
#include <usartManager.h>
#include <i2cPacket.h>
#include <halDelay.h>

#define Measure_T_SHT21 0xf3
#define Measure_RH_SHT21 0xf5



static HAL_AppTimer_t sendeTimer;
static HAL_AppTimer_t mesTimerSHT;
static HAL_AppTimer_t mesTimerSCD;
static AppState_t appstate = APP_INIT_STATE;

static void initTimer(void);
static void sendeTimerFired(void);
static void measureReadySHT(void);
static void measureReadySCD(void);
static HAL_I2cDescriptor_t i2cdescriptorcmdSHT;
static HAL_I2cDescriptor_t i2cdescriptorrdSHT;
static HAL_I2cDescriptor_t i2cdescriptorcmdSCD;
static HAL_I2cDescriptor_t i2cdescriptorrdSCD;

bool result;
bool measurementSHT21neg;
bool measuretempsht21;
bool SCD_ready = false;

uint8_t shtcmd;
uint8_t shtdata[2];
uint16_t sht_rd;
uint8_t scdcmd[2];
uint8_t scddata[9];
uint16_t scd_rd_co2;
uint16_t scd_rd_temp;
uint16_t scd_rd_rh;


int32_t vorkomma;
int32_t nachkomma;

uint8_t t_output_SHT21[] = "+xxx.xx degree Celsius \r\n";
uint8_t rh_output_SHT21[] = "+xxx.xx percent  relative Humidity \r\n";
uint8_t co2_output_SCD[] = "XXXXX ppm CO2 \r\n";

uint8_t t_output_SHT21_sensorbytes[] = "0xXXXX sensor \r\n";




static void callbackcmdSHT(bool result){
	if(!result){
		appWriteDataToUsart((uint8_t*)"Error:SHT  callbackcmd called with 0\r\n", sizeof("Error:SHT callbackcmd called with 1\r\n")-1);
	}
	HAL_CloseI2cPacket(&i2cdescriptorcmdSHT);
	HAL_StartAppTimer(&mesTimerSHT);
}

static void callbackrdSHT(bool result){
	if(!result){
		appWriteDataToUsart((uint8_t*)"Error: SHT callbackrd called with 0\r\n", sizeof("Error: SHT callbackrd called with 0\r\n")-1);
	}
	HAL_CloseI2cPacket(&i2cdescriptorrdSHT);
}

static void callbackcmdSCD(bool result){
	if(!result){
		appWriteDataToUsart((uint8_t*)"Error:SCD callbackcmd called with 0\r\n", sizeof("Error:SCD callbackcmd called with 1\r\n")-1);
		}
	HAL_CloseI2cPacket(&i2cdescriptorcmdSCD);
	HAL_StartAppTimer(&mesTimerSHT);
}

static void callbackrdSCD(bool result){
	if(!result){
		appWriteDataToUsart((uint8_t*)"Error: SCD callbackrd called with 0\r\n", sizeof("Error: SCD callbackrd called with 0\r\n")-1);
		}
	HAL_CloseI2cPacket(&i2cdescriptorrdSCD);
}



/***********************************************
SHT-Descriptor
***********************************************/
static HAL_I2cDescriptor_t i2cdescriptorcmdSHT={						
	.tty = TWI_CHANNEL_0,
	.clockRate = I2C_CLOCK_RATE_62,
	.f = callbackcmdSHT,															
	.id = SHT_21_ADD,
	.data = &shtcmd,
	.length = 1,
	.lengthAddr = HAL_NO_INTERNAL_ADDRESS
};

static HAL_I2cDescriptor_t i2cdescriptorrdSHT={
	.tty = TWI_CHANNEL_0,
	.clockRate = I2C_CLOCK_RATE_62,
	.f = callbackrdSHT,
	.id = SHT_21_ADD,
	.data = shtdata,
	.length = 2,
	.lengthAddr = HAL_NO_INTERNAL_ADDRESS
};
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
	sht_rd = shtdata[0];
	sht_rd <<= 8;
	sht_rd |= shtdata[1]; 
	
	uint64_t measurementsht21 = conversionfactor * sht_rd;
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
	uint16_to_hexstr((uint8_t *)t_output_SHT21_sensorbytes, sizeof(t_output_SHT21_sensorbytes), sht_rd, 2);
	}

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

void initializeSCD(){
	if (-1 == HAL_OpenI2cPacket(&i2cdescriptorcmdSCD)){
		appWriteDataToUsart((uint8_t*)"open fail scd init\r\n", sizeof("open fail scd init\r\n")-1);
	}
	/* uint16_t cmd = SCD41_PERIODIC_MES_CMD; //0x21b1
	scdcmd[0] = cmd >> 8;
	scdcmd[1] = cmd & 0x00FF; */
	scdcmd[0] = 0x21;
	scdcmd[1] = 0xb1;
	if (-1 == HAL_WriteI2cPacket(&i2cdescriptorcmdSCD)){
		appWriteDataToUsart((uint8_t*)"write fail scd init\r\n", sizeof("write fail scd init\r\n")-1);
	}
	appWriteDataToUsart((uint8_t*)"SCD Initialized \r\n", sizeof("SCD Initialized \r\n")-1);
	HAL_StartAppTimer(&mesTimerSCD);
}

void readSHT(){
	if (-1 == HAL_OpenI2cPacket(&i2cdescriptorrdSHT)){
		appWriteDataToUsart((uint8_t*)"open fail sht read\r\n", sizeof("open fail sht read\r\n")-1);
	}
	if (-1 == HAL_ReadI2cPacket(&i2cdescriptorrdSHT)){
		appWriteDataToUsart((uint8_t*)"read fail sht read\r\n", sizeof("read fail sht read\r\n")-1);
	}
	
}

void readSCD(){
	if (-1 == HAL_OpenI2cPacket(&i2cdescriptorcmdSCD)){
		appWriteDataToUsart((uint8_t*)"open fail scd cmd\r\n", sizeof("open fail scd cmd\r\n")-1);
	}
	//uint16_t cmd = SCD41_READ_MES;
	//scdcmd[0] = cmd >> 8;
	//scdcmd[1] = cmd & 0x00FF;
	scdcmd[0] = 0xec;
	scdcmd[1] = 0x05;
	if (-1 == HAL_WriteI2cPacket(&i2cdescriptorcmdSCD)){
		appWriteDataToUsart((uint8_t*)"write fail scd cmd\r\n", sizeof("write fail scd cmd\r\n")-1);
	}
	HAL_Delay(1);
	if (-1 == HAL_OpenI2cPacket(&i2cdescriptorrdSCD)){
		appWriteDataToUsart((uint8_t*)"open fail scd read\r\n", sizeof("open fail scd read\r\n")-1);
	}
	if (-1 == HAL_ReadI2cPacket(&i2cdescriptorrdSCD)){
		appWriteDataToUsart((uint8_t*)"read fail scd read\r\n", sizeof("read fail scd read\r\n")-1);
	}
	SYS_PostTask(APL_TASK_ID);
	appstate = APP_AUSGABE_STATE;
}

void triggerSHT(){
	if(measuretempsht21){
		shtcmd = Measure_T_SHT21;
		}else{
		shtcmd = Measure_RH_SHT21;
	}
	
	if (-1 == HAL_OpenI2cPacket(&i2cdescriptorcmdSHT)){
		appWriteDataToUsart((uint8_t*)"open fail SHT trigger\r\n", sizeof("open fail SHT trigger\r\n")-1);
	}
	
	if (-1 == HAL_WriteI2cPacket(&i2cdescriptorcmdSHT)){
		appWriteDataToUsart((uint8_t*)"write fail SHT trigger\r\n", sizeof("write fail SHT trigger\r\n")-1);
	}
	HAL_StartAppTimer(&mesTimerSHT);  
}
		
/***********************************************
Timer Initialization
***********************************************/

static void initTimer(){
	mesTimerSHT.interval	= SHT_MES_DELAY;
	mesTimerSHT.mode		= TIMER_ONE_SHOT_MODE;
	mesTimerSHT.callback	= measureReadySHT;
	
	mesTimerSCD.interval	= SCD_MES_INTERVAL;			// Timer interval
	mesTimerSCD.mode		= TIMER_REPEAT_MODE;       // Timer-Mode
	mesTimerSCD.callback	= measureReadySCD;         // Callback function
	
	sendeTimer.interval = APP_SENDE_INTERVAL;      // Timer interval
	sendeTimer.mode     = TIMER_REPEAT_MODE;       // Timer-Mode
	sendeTimer.callback = sendeTimerFired;         // Callback function
	HAL_StartAppTimer(&sendeTimer);                // Start sendeTimer
}

static void sendeTimerFired(){
	appstate=APP_TRIGGER_STATE;
	SYS_PostTask(APL_TASK_ID);
}

static void measureReadySHT(){
	appstate=APP_READ_STATE;
	SYS_PostTask(APL_TASK_ID);
}

static void measureReadySCD(){
	SCD_ready = true;
}

/***********************************************
Zustandsautomat
***********************************************/

void APL_TaskHandler(void){
switch(appstate){
	case APP_INIT_STATE:
		appInitUsartManager();
		initTimer();
		initializeSCD();
		appstate=APP_NOTHING_STATE;
	break;
	
	case APP_READ_STATE:
		readSHT();
		if(SCD_ready){
			readSCD();
			SCD_ready = false;
		}

		appstate=APP_AUSGABE_STATE;
	break;
	
	case APP_TRIGGER_STATE:
		triggerSHT();
		appstate=APP_NOTHING_STATE;
	break;
	
	case APP_AUSGABE_STATE:
		calculateOutputSHT21();
		calculateOutputSCD();
		if(measuretempsht21){
		appWriteDataToUsart((uint8_t*)t_output_SHT21, sizeof(t_output_SHT21));
		measuretempsht21 = false;
		}else{
		appWriteDataToUsart((uint8_t*)rh_output_SHT21, sizeof(rh_output_SHT21));
		measuretempsht21 = true;
		}
		appWriteDataToUsart((uint8_t*)co2_output_SCD, sizeof(co2_output_SCD));
		appWriteDataToUsart((uint8_t*)t_output_SHT21_sensorbytes, sizeof(t_output_SHT21_sensorbytes));
		
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
