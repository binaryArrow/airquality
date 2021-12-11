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


static HAL_AppTimer_t sendeTimer;

static AppState_t appstate = APP_INIT_STATE;

static void initTimer(void);
static void sendeTimerFired(void);
static HAL_I2cDescriptor_t i2cdescriptorwrite;
static HAL_I2cDescriptor_t i2cdescriptorread;

bool result;
uint8_t writeReadOrderSHT[1];
uint8_t readDataSHT[2];
int32_t temperature;
uint8_t t_output[]=" 000.00 degree celcius\r\n";



static void readSensorDoneWrite(bool result){
	appstate=APP_READ_STATE;
	if(result){
		appWriteDataToUsart((uint8_t*)"readSensorDoneWrite called with 1\r\n", sizeof("readSensorDoneWrite called with 1\r\n")-1);
	}
	else{
		appWriteDataToUsart((uint8_t*)"readSensorDoneWrite called with 0\r\n", sizeof("readSensorDoneWrite called with 1\r\n")-1);
		
	}
	HAL_CloseI2cPacket(&i2cdescriptorwrite);
	SYS_PostTask(APL_TASK_ID);
}

static void readSensorDoneRead(bool result){
	appstate=APP_AUSGABE_STATE;
	if(result){
		appWriteDataToUsart((uint8_t*)"readSensorDoneRead called with 1\r\n", sizeof("readSensorDoneRead called with 1\r\n")-1);
	}
	else{
		appWriteDataToUsart((uint8_t*)"readSensorDoneRead called with 0\r\n", sizeof("readSensorDoneRead called with 1\r\n")-1);
		
	}
	HAL_CloseI2cPacket(&i2cdescriptorread);
	SYS_PostTask(APL_TASK_ID);
}



static HAL_I2cDescriptor_t i2cdescriptorwrite={
	.tty = TWI_CHANNEL_0,
	.clockRate = I2C_CLOCK_RATE_62,
	.f = readSensorDoneWrite,
	.id = 0x40,
	.data = writeReadOrderSHT,
	.length = 1,
	.lengthAddr = HAL_NO_INTERNAL_ADDRESS
};

static HAL_I2cDescriptor_t i2cdescriptorread={
	.tty = TWI_CHANNEL_0,
	.clockRate = I2C_CLOCK_RATE_62,
	.f = readSensorDoneRead,
	.id = 0x40,
	.data = readDataSHT,
	.length = 2,
	.lengthAddr = HAL_NO_INTERNAL_ADDRESS
};



void calculateOutput(){
	int16_t vorkomma;
	vorkomma = readDataSHT[0];
	vorkomma <<= 8;
	vorkomma |= readDataSHT[1];
	vorkomma >>= 7;

	uint16_t nachkomma;
	nachkomma = readDataSHT[1] & (0x7F);
	nachkomma >>= 5;
	//invertieren der nachkomma stelle, falls die Temperatur negativ ist
	if(readDataSHT[0]>>7){
		nachkomma = 100 - (nachkomma *25);
		} else {
		nachkomma = nachkomma * 25;
	}
	temperature = vorkomma*100 + nachkomma;
}

static void initTimer(){
	sendeTimer.interval = APP_SENDE_INTERVAL;      // Timer interval
	sendeTimer.mode     = TIMER_REPEAT_MODE;       // Timer-Mode
	sendeTimer.callback = sendeTimerFired;         // Callback function
	HAL_StartAppTimer(&sendeTimer);                // Start sendeTimer
}

static void sendeTimerFired(){
	appstate=APP_WRITE_STATE;
	SYS_PostTask(APL_TASK_ID);
}

void APL_TaskHandler(void){
switch(appstate){
	case APP_INIT_STATE:
		appInitUsartManager();
		initTimer();
		HAL_StartAppTimer(&sendeTimer);
		writeReadOrderSHT[0] = 0xf3;
		appstate=APP_NOTHING_STATE;
	readDataSHT[0] = 0x00;
	readDataSHT[1] = 0x00;

	break;
	
	case APP_READ_STATE:
	if (-1 == HAL_OpenI2cPacket(&i2cdescriptorread)){
		appWriteDataToUsart((uint8_t*)"open fail\r\n", sizeof("open fail\r\n")-1);
	}
	if (-1 == HAL_ReadI2cPacket(&i2cdescriptorread)){
		appWriteDataToUsart((uint8_t*)"read fail\r\n", sizeof("read fail\r\n")-1);
	}
		
		appstate=APP_NOTHING_STATE;
	break;
	
	case APP_WRITE_STATE:
		if (-1 == HAL_OpenI2cPacket(&i2cdescriptorwrite)){
			appWriteDataToUsart((uint8_t*)"open fail\r\n", sizeof("open fail\r\n")-1);
		}
		
		if (-1 == HAL_WriteI2cPacket(&i2cdescriptorwrite)){
			appWriteDataToUsart((uint8_t*)"write fail\r\n", sizeof("write fail\r\n")-1);
		}
		appstate=APP_NOTHING_STATE;
	break;
	
	case APP_AUSGABE_STATE:
		calculateOutput();
		int32_to_str(t_output,sizeof(t_output),temperature/100,0,4);
		uint32_to_str(t_output,sizeof(t_output),abs(temperature)%100,5,2);
		appWriteDataToUsart((uint8_t*)t_output, sizeof(t_output));
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
