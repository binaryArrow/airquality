APP_NAME = ZLLDemo
PROJECT_NAME = ATmega2564RFR2
CONFIG_NAME = All_StdlinkSec_MegaRf_Atmega2564rfr2_8Mhz_Iar

#PROJECT_NAME = ATmega2564RFR2
#CONFIG_NAME = All_StdlinkSec_MegaRf_Atmega2564rfr2_8Mhz_Iar
#CONFIG_NAME = All_StdlinkSec_MegaRf_Atmega2564rfr2_8Mhz_Gcc
#CONFIG_NAME = Router_StdlinkSec_MegaRf_Atmega2564rfr2_8Mhz_Iar
#CONFIG_NAME = Router_StdlinkSec_MegaRf_Atmega2564rfr2_8Mhz_Gcc
#CONFIG_NAME = EndDevice_StdlinkSec_MegaRf_Atmega2564rfr2_8Mhz_Iar
#CONFIG_NAME = EndDevice_StdlinkSec_MegaRf_Atmega2564rfr2_8Mhz_Gcc
#CONFIG_NAME = All_StdlinkSec_MegaRf_Atmega2564rfr2_16Mhz_Iar
#CONFIG_NAME = All_StdlinkSec_MegaRf_Atmega2564rfr2_16Mhz_Gcc
#CONFIG_NAME = Router_StdlinkSec_MegaRf_Atmega2564rfr2_16Mhz_Iar
#CONFIG_NAME = Router_StdlinkSec_MegaRf_Atmega2564rfr2_16Mhz_Gcc
#CONFIG_NAME = EndDevice_StdlinkSec_MegaRf_Atmega2564rfr2_16Mhz_Iar
#CONFIG_NAME = EndDevice_StdlinkSec_MegaRf_Atmega2564rfr2_16Mhz_Gcc

#PROJECT_NAME = ATmega256RFR2
#CONFIG_NAME = All_StdlinkSec_MegaRf_Atmega256rfr2_8Mhz_Iar
#CONFIG_NAME = All_StdlinkSec_MegaRf_Atmega256rfr2_8Mhz_Gcc
#CONFIG_NAME = Router_StdlinkSec_MegaRf_Atmega256rfr2_8Mhz_Iar
#CONFIG_NAME = Router_StdlinkSec_MegaRf_Atmega256rfr2_8Mhz_Gcc
#CONFIG_NAME = EndDevice_StdlinkSec_MegaRf_Atmega256rfr2_8Mhz_Iar
#CONFIG_NAME = EndDevice_StdlinkSec_MegaRf_Atmega256rfr2_8Mhz_Gcc
#CONFIG_NAME = All_StdlinkSec_MegaRf_Atmega256rfr2_16Mhz_Iar
#CONFIG_NAME = All_StdlinkSec_MegaRf_Atmega256rfr2_16Mhz_Gcc
#CONFIG_NAME = Router_StdlinkSec_MegaRf_Atmega256rfr2_16Mhz_Iar
#CONFIG_NAME = Router_StdlinkSec_MegaRf_Atmega256rfr2_16Mhz_Gcc
#CONFIG_NAME = EndDevice_StdlinkSec_MegaRf_Atmega256rfr2_16Mhz_Iar
#CONFIG_NAME = EndDevice_StdlinkSec_MegaRf_Atmega256rfr2_16Mhz_Gcc

all:
	make -C makefiles/$(PROJECT_NAME) -f Makefile_$(CONFIG_NAME) all APP_NAME=$(APP_NAME)

clean:
	make -C makefiles/$(PROJECT_NAME) -f Makefile_$(CONFIG_NAME) clean APP_NAME=$(APP_NAME)
