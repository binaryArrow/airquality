/**************************************************************************//**
  \file app.h

  \brief Usart-Anwendung Headerdatei.

  \author
    Markus Krauße

******************************************************************************/

#ifndef _APP_H
#define _APP_H

#define APP_SENDE_INTERVAL	5500
#define APP_MES_INTERVAL	85
#define SHT_21_ADD			0x40
#define CCS811_ADD			0x2D		//0101 1010 Datasheet Address 0x5A/0x5B for reading and writing
										//0010 1101 shifted address because Bitcloud shifts the address and adds a 1/0 for read/write operations
#define SCD41_ADD			0x31		// 0110 0010 --> 0011 0001; 0x62 (datasheet) --> 0x31 (bitcloud ready)		



typedef enum{
	APP_INIT_STATE,
	APP_READ_STATE,
	APP_WRITE_STATE,
	APP_AUSGABE_STATE,
	APP_NOTHING_STATE
} AppState_t;
#endif
// eof app.h