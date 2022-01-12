/**************************************************************************//**
  \file app.h

  \brief Usart-Anwendung Headerdatei.

  \author
    Markus Krau�e

******************************************************************************/

#ifndef _APP_H
#define _APP_H

#define APP_SENDE_INTERVAL	2000
#define APP_MES_INTERVAL	85

typedef enum{
	APP_INIT_STATE,
	APP_READ_STATE,
	APP_WRITE_STATE,
	APP_AUSGABE_STATE,
	APP_STARTJOIN_NETWORK,
	APP_INIT_ENDPOINT,
	APP_INIT_TRANSMITDATA,
	APP_NOTHING_STATE
} AppState_t;
#endif
// eof app.h