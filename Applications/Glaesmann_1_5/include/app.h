/**************************************************************************//**
  \file app.h

  \brief Usart-Anwendung Headerdatei.

  \author
    Markus Krau�e

******************************************************************************/

#ifndef _APP_H
#define _APP_H

#define APP_SENDE_INTERVAL    1000

typedef enum{
	APP_INIT_STATE,
	APP_RED_STATE,
	APP_RED_YELLOW_STATE,
	APP_GREEN_STATE,
	APP_YELLOW_STATE
} AppState_t;
#endif
// eof app.h