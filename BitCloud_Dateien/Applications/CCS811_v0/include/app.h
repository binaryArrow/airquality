/**************************************************************************//**
  \file app.h

  \brief Usart-Anwendung Headerdatei.

  \author
    Markus Krauﬂe

******************************************************************************/

#ifndef _APP_H
#define _APP_H

#define CCS_MES_INTERVAL	1000
#define CCS_STARTUP_TIME 2000

#define CCS_MIN_DELAY 1
#define CCS_DRIVE_STATUS_DELAY 1000


#define CCS811_ADD			0x5A		
			
#define CCS_RESET_SW_CMD			0xFF11E5728A //REG: 0xFF SW_RESET: 0x11E5728A
#define CCS_HWID_REG				0x20
#define CCS_HWID					0x81
#define CCS_BOOTLOADER_APPSTATE		0xF4
#define CCS_MEAS_MODE_REG			0x01
#define CCS_MEAS_MODE				0x10
#define CCS_STATUS_REG				0x00
#define CCS_DATA_RDY				0x04
#define CCS_RESULT_REG				0x02

										
#define APP_NOTHING_STATE					0
#define APP_STARTUP_STATE					1
#define APP_AUSGABE_STATE					10
#define APP_RESET_CCS_SW_STATE				11
#define APP_CCS_HW_ID_WRITE_REG_STATE		12
#define APP_CCS_HW_ID_READ_STATE			13
#define APP_CCS_CHANGE_TO_APPSTATE_STATE	14
#define APP_CCS_WRITE_MEAS_REG_STATE		15
#define APP_CCS_WRITE_STATUS_REG_STATE		16
#define APP_CCS_READ_STATUS_REG_STATE		17
#define APP_CCS_WRITE_RESULT_REG_STATE		18
#define APP_CCS_READ_RESULT_REG_STATE		19


#endif
// eof app.h