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

static HAL_AppTimer_t mesTimerSCD;
static AppState_t appstate = APP_INIT_STATE;

static void initTimer();
static void mesTimerComplete();



static HAL_I2cDescriptor_t i2cdescriptorcmdSCD;
static HAL_I2cDescriptor_t i2cdescriptorrdSCD;

bool result;
bool measurementSCDneg;
bool SCD_ready = false;
bool ready = false;
uint8_t measurementSCDReady[2] = {0x00,0x00};

uint8_t scdcmd[2];
uint8_t scddata[9];
uint16_t scd_rd_co2;
uint16_t scd_rd_temp;
uint16_t scd_rd_rh;



uint8_t co2_output_SCD[] = "XXXXX ppm CO2 \r\n";

static void callbackcmdSCD(bool result){
	if(!result){
		appWriteDataToUsart((uint8_t*)"SCD callbackcmd called with 0\r\n", sizeof("SCD callbackcmd called with 1\r\n")-1);
		}
}

static void callbackrdSCD(bool result){
	if(!result){
		appWriteDataToUsart((uint8_t*)"SCD callbackrd called with 0\r\n", sizeof("Error: SCD callbackrd called with 0\r\n")-1);
		}
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

void initializeSCD(){
	/* uint16_t cmd = SCD41_PERIODIC_MES_CMD; //0x21b1
	scdcmd[0] = cmd >> 8;
	scdcmd[1] = cmd & 0x00FF; */
	scdcmd[0] = 0x21;
	scdcmd[1] = 0xb1;
	
	if (-1 == HAL_OpenI2cPacket(&i2cdescriptorcmdSCD)){
		appWriteDataToUsart((uint8_t*)"open fail scd init\r\n", sizeof("open fail scd init\r\n")-1);
	}	
	if (-1 == HAL_WriteI2cPacket(&i2cdescriptorcmdSCD)){
		appWriteDataToUsart((uint8_t*)"write fail scd init\r\n", sizeof("write fail scd init\r\n")-1);
	}else{
		appWriteDataToUsart((uint8_t*)"SCD Initialized \r\n", sizeof("SCD Initialized \r\n")-1);
	}
	HAL_CloseI2cPacket(&i2cdescriptorcmdSCD);
	HAL_StartAppTimer(&mesTimerSCD);
}


void checkIfSCDReady(){
	scdcmd[0] = 0xe4;
	scdcmd[1] = 0xb8;
	appWriteDataToUsart((uint8_t*)"Checking if SCD ready to read \r\n", sizeof("Checking if SCD ready to read \r\n")-1);
	if (-1 == HAL_OpenI2cPacket(&i2cdescriptorcmdSCD)){
		appWriteDataToUsart((uint8_t*)"open fail scd cmd\r\n", sizeof("open fail scd cmd\r\n")-1);
	}
	if (-1 == HAL_WriteI2cPacket(&i2cdescriptorcmdSCD)){
		appWriteDataToUsart((uint8_t*)"write fail scd cmd\r\n", sizeof("write fail scd cmd\r\n")-1);
	}
	
	if (-1 == HAL_ReadI2cPacket(&i2cdescriptorrdSCD)){
		appWriteDataToUsart((uint8_t*)"read fail scd read\r\n", sizeof("read fail scd read\r\n")-1);
	}
	
	measurementSCDReady[0] = scddata[0] << 5;
	measurementSCDReady[1] = measurementSCDReady[0] |= measurementSCDReady[1];
	if(measurementSCDReady[1]){
		SCD_ready = true;
		appWriteDataToUsart((uint8_t*)"SCD ready to read \r\n", sizeof("SCD ready to read \r\n")-1);
	}else{
		appWriteDataToUsart((uint8_t*)"SCD NOT ready to read \r\n", sizeof("SCD NOT ready to read \r\n")-1);
		SCD_ready = false;
	}
	
	HAL_CloseI2cPacket(&i2cdescriptorcmdSCD);
}

void readSCD(){ 
	
	
	
			//uint16_t cmd = SCD41_READ_MES;
			//scdcmd[0] = cmd >> 8;
			//scdcmd[1] = cmd & 0x00FF;
		scdcmd[0] = 0xec;
		scdcmd[1] = 0x05;
		
		appWriteDataToUsart((uint8_t*)"Data ready\r\n", sizeof("Data ready\r\n")-1);
		
		if (-1 == HAL_OpenI2cPacket(&i2cdescriptorcmdSCD)){
			appWriteDataToUsart((uint8_t*)"open fail scd cmd\r\n", sizeof("open fail scd cmd\r\n")-1);
		}
		if (-1 == HAL_WriteI2cPacket(&i2cdescriptorcmdSCD)){
			appWriteDataToUsart((uint8_t*)"write fail scd cmd\r\n", sizeof("write fail scd cmd\r\n")-1);
		}
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

static void initTimer(){
	mesTimerSCD.interval	=	SCD_MES_INTERVAL;		 // Timer interval
	mesTimerSCD.mode		=	TIMER_REPEAT_MODE;       // Timer-Mode
	mesTimerSCD.callback	=	mesTimerComplete;         // Callback function
}



static void mesTimerComplete(){
	appWriteDataToUsart((uint8_t*)"mesTImer fired\r\n", sizeof("mesTimer fired\r\n")-1);
	checkIfSCDReady();
	if(SCD_ready){
		appstate=APP_READ_STATE;
	}else{
		appstate=APP_NOTHING_STATE;
		appWriteDataToUsart((uint8_t*)"Data NOT ready\r\n", sizeof("Data NOT ready\r\n")-1);
	}
	SYS_PostTask(APL_TASK_ID);
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
		appWriteDataToUsart((uint8_t*)"read state reached \r\n", sizeof("read state reached \r\n")-1);
		//readSCD();
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
