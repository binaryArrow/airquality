/**************************************************************************//**
  \file app.h

  \brief Usart-Anwendung Headerdatei.

  \author
    Markus Krauße

******************************************************************************/

#ifndef _APP_H
#define _APP_H

#define APP_SENDE_INTERVAL	5500
#define SHT_MES_DELAY		85
#define SCD_MES_INTERVAL	5500
#define SCD_STARTUP_TIME 1500
#define SCD_DELAY_TIME 500
#define SCD_READ_DELAY_TIME 100



#define SHT_21_ADD			0x40
#define CCS811_ADD			0x2D		//0101 1010 Datasheet Address 0x5A/0x5B for reading and writing. 0010 1101 shifted address because Bitcloud shifts the address and adds a 1/0 for read/write operations
#define SCD41_ADD			0x62		// 0110 0010 --> 0011 0001 0x62 (datasheet) --> 0x31 (bitcloud ready)					

#define SHT21_MES_T					0xf3
#define SHT21_MES_RH				0xf5
#define SCD41_PERIODIC_MES_CMD		0x21b1
#define SCD41_STOP_PERIODIC_MES_CMD 0x3F86
#define SCD41_READ_MES				0xec05
										

typedef enum{
	APP_STARTUP_STATE,
	APP_RESET_SENSOR_STATE,
	APP_INIT_SENSOR_STATE,
	APP_CALL_FOR_READ_STATE,
	APP_READ_SCD_STATE,
	APP_AUSGABE_STATE,
	APP_NOTHING_STATE
} AppState_t;
#endif
// eof app.h