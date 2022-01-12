/**************************************************************************//**
  \file app.h

  \brief Usart-Anwendung Headerdatei.

  \author
    Markus Krau�e

******************************************************************************/

#ifndef _APP_H
#define _APP_H

#define APP_SENDE_INTERVAL	10000
#define APP_MES_INTERVAL	1000
#define APP_START_INTERVAL  1000

typedef enum{
	APP_INIT_STATE,
	APP_READ_STATE,
	APP_WRITE_READ_REGISTER_STATE,
	APP_WRITE_STATE,
	APP_AUSGABE_STATE,
	APP_NOTHING_STATE
} AppState_t;
#endif
// eof app.h