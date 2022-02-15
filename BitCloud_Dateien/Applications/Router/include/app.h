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
	APP_INIT,
	APP_STARTJOIN_NETWORK,
	APP_INIT_ENDPOINT,
	APP_NOTHING
} AppState_t;
#endif
// eof app.h