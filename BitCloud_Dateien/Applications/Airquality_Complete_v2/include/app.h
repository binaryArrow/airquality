/**************************************************************************//**
  \file app.h

  \brief Usart-Anwendung Headerdatei.

  \author
    Markus Krau�e, Achim Glaesmann, Lucas Merkert, Friedrich ?

******************************************************************************/

#ifndef _APP_H
#define _APP_H

#define MES_TEMP	1
#define MES_RH		2

#define SHT_MES_DELAY			85

#define SCD_MES_INTERVAL		60000
#define SCD_STARTUP_TIME		2000
#define SCD_RESET_DELAY_TIME	500
#define SCD_READ_DELAY_TIME		100

#define CCS_MIN_DELAY			1
#define CCS_DRIVE_STATUS_DELAY	1000



#define SHT_21_ADD					0x40
#define CCS811_ADD					0x5A
#define SCD41_ADD					0x62		
#define SHT21_MES_T_CMD				0xf3
#define SHT21_MES_RH_CMD			0xf5

#define SCD41_PERIODIC_MES_CMD		0x21b1
#define SCD41_STOP_PERIODIC_MES_CMD 0x3F86
#define SCD41_READ_MES				0xec05

#define CCS_RESET_SW_CMD			0xFF11E5728A //REG: 0xFF SW_RESET: 0x11E5728A
#define CCS_HWID_REG				0x20
#define CCS_HWID					0x81
#define CCS_BOOTLOADER_APPSTATE		0xF4
#define CCS_MEAS_MODE_REG			0x01
#define CCS_MEAS_MODE				0x10 //0011 0000
#define CCS_STATUS_REG				0x00
#define CCS_DATA_RDY				0x04
#define CCS_RESULT_REG				0x02
										
#define APP_NOTHING_STATE					0
#define APP_STARTUP_STATE					1

#define APP_RESET_SCD_STATE					2
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

#define APP_RESET_CCS_SW_STATE				15
#define APP_CCS_HW_ID_WRITE_REG_STATE		16
#define APP_CCS_HW_ID_READ_STATE			17
#define APP_CCS_CHANGE_TO_APPSTATE_STATE	18
#define APP_CCS_WRITE_MEAS_REG_STATE		19
#define APP_CCS_WRITE_STATUS_REG_STATE		20
#define APP_CCS_READ_STATUS_REG_STATE		21
#define APP_CCS_WRITE_RESULT_REG_STATE		22
#define APP_CCS_READ_RESULT_REG_STATE		23

#define APP_READ_VCC						24

#endif
// eof app.h
