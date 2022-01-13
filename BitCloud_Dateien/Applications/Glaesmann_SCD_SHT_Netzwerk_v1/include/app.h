/**************************************************************************//**
  \file app.h

  \brief Usart-Anwendung Headerdatei.

  \author
    Markus Krau�e

******************************************************************************/

#ifndef _APP_H
#define _APP_H

#define MES_TEMP	1
#define MES_RH		2

#define APP_SENDE_INTERVAL	5500
#define SHT_MES_DELAY		85
#define SCD_MES_INTERVAL	5500
#define SCD_STARTUP_TIME 1500
#define SCD_RESET_DELAY_TIME 500
#define SCD_READ_DELAY_TIME 100



#define SHT_21_ADD			0x40
#define CCS811_ADD			0x2D		//0101 1010 Datasheet Address 0x5A/0x5B for reading and writing. 0010 1101 shifted address because Bitcloud shifts the address and adds a 1/0 for read/write operations
#define SCD41_ADD			0x62		// 0110 0010 --> 0011 0001 0x62 (datasheet) --> 0x31 (bitcloud ready)					

#define SHT21_MES_T					0xf3
#define SHT21_MES_RH				0xf5
#define SCD41_PERIODIC_MES_CMD		0x21b1
#define SCD41_STOP_PERIODIC_MES_CMD 0x3F86
#define SCD41_READ_MES				0xec05
										
#define APP_NOTHING_STATE					0
#define APP_STARTUP_STATE					1
#define APP_RESET_SENSOR_STATE				2
#define APP_INIT_SENSOR_STATE				3
#define APP_CALL_FOR_READ_SCD_STATE			4
#define APP_CALL_FOR_READ_TEMP_SHT_STATE	5
#define APP_CALL_FOR_READ_RH_SHT_STATE		6
#define APP_READ_SCD_STATE					7
#define APP_READ_TEMP_SHT_STATE				8
#define APP_READ_RH_SHT_STATE				9
#define APP_AUSGABE_STATE					10

#define APP_STARTJOIN_NETWORK				11
#define APP_INIT_ENDPOINT					12
#define APP_INIT_TRANSMITDATA				13
#define APP_TRANSMIT						14

#endif
// eof app.h