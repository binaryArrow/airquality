/**************************************************************************//**
  \file thermostat.c

  \brief
    Thermostat implementation.

  \author
    Atmel Corporation: http://www.atmel.com \n
    Support email: avr@atmel.com

  Copyright (c) 2008-2015, Atmel Corporation. All rights reserved.
  Licensed under Atmel's Limited License Agreement (BitCloudTM).

  \internal
    History:
    09/09/2014 Unithra.C  - Created
******************************************************************************/
#ifdef APP_DEVICE_TYPE_THERMOSTAT

/******************************************************************************
                             Includes section
******************************************************************************/
#include <thClusters.h>
#include <basicCluster.h>
#include <identifyCluster.h>
#include <thThermostatCluster.h>
#include <thThermostatUiConfCluster.h>
#include <zclDevice.h>
#include <zclSecurityManager.h>
#include <commandManager.h>
#include <uartManager.h>
#include <console.h>
#include <pdsDataServer.h>
#include <ezModeManager.h>
#include <haClusters.h>
#include <otauService.h>
#include <thOccupancySensingCluster.h>
#include <thFanControlCluster.h>
#include <thDiagnosticsCluster.h>
#include <thHumidityMeasurementCluster.h>
#include <thGroupsCluster.h>
#include <thScenesCluster.h>
#include <thTemperatureMeasurementCluster.h>

/******************************************************************************
                   Define(s) section
******************************************************************************/
#define UPDATING_PERIOD                    20000UL

/******************************************************************************
                   type(s) section
******************************************************************************/
typedef enum _ReportingState_t
{
  CONFIG_REPORT_INIT_STATE = 0,
  THERMOSTAT_REPORTING_CONFIGURED,
  OCCUPANCY_REPORTING_CONFIGURED,
  HUMIDITY_MEASURED_VALUE_REPORTING_CONFIGURED,
  HUMIDITY_TOLERANCE_VALUE_REPORTING_CONFIGURED,
  TEMPERATURE_MEASURED_VALUE_REPORTING_CONFIGURED,
  TEMPERATURE_TOLERANCE_VALUE_REPORTING_CONFIGURED,
  CONFIGURE_REPORTING_COMPLETED
}ReportingState_t;

typedef enum _thBoundClustersInEzMode_t
{
  THERMOSTAT_CLUSTER_BOUND = 1,
  OCCUPANCY_SENSING_CLUSTER_BOUND = (1 << 1),
  HUMIDITY_MEASUREMENT_CLUSTER_BOUND = (1 << 2),
  TEMPERATURE_MEASUREMENT_CLUSTER_BOUND = (1 << 3)
}thBoundClustersInEzMode_t;

/*******************************************************************************
                    Static functions section
*******************************************************************************/
static void updateCommissioningStateCb(ZCL_Addressing_t *addressing, ZCL_UpdateCommissioningState_t *payload);
static void updateSensorsAttributeValues(void);
static void handleThConfigReporting(void);

/******************************************************************************
                    Local variables section
******************************************************************************/
static ZCL_DeviceEndpoint_t thEndpoint =
{
  .simpleDescriptor =
  {
    .endpoint            = APP_SRC_ENDPOINT_ID,
    .AppProfileId        = PROFILE_ID_HOME_AUTOMATION,
    .AppDeviceId         = HA_THERMOSTAT_DEVICE_ID,
    .AppInClustersCount  = ARRAY_SIZE(thServerClusterIds),
    .AppInClustersList   = thServerClusterIds,
    .AppOutClustersCount = ARRAY_SIZE(thClientClusterIds),
    .AppOutClustersList  = thClientClusterIds,
  },
  .serverCluster = thServerClusters,
  .clientCluster = thClientClusters,
};

static ZCL_LinkKeyDesc_t thermostatKeyDesc = {APS_UNIVERSAL_EXTENDED_ADDRESS  /*addr*/,
                                         HA_LINK_KEY /*key*/};

static IdentifySubscriber_t subcriber =
{
  .updateCommissioningState = updateCommissioningStateCb
};

static HAL_AppTimer_t sensorAttributeUpdateTimer =
{
  .interval = UPDATING_PERIOD,
  .mode     = TIMER_REPEAT_MODE,
  .callback = updateSensorsAttributeValues,
};

static uint16_t thClustersBoundMask = 0x00;

/******************************************************************************
                    Prototypes section
******************************************************************************/
static void thConfigureReportingResp(ZCL_Notify_t *ntfy);
/******************************************************************************
                    Implementation section
******************************************************************************/

/**************************************************************************//**
\brief Device initialization routine
******************************************************************************/
void appDeviceInit(void)
{
  ZCL_RegisterEndpoint(&thEndpoint);

#if (APP_ENABLE_CONSOLE == 1) || (APP_DEVICE_EVENTS_LOGGING == 1)
  uartInit();
#endif
#if APP_ENABLE_CONSOLE == 1
  initConsole();
#endif
  /* Subscribe the Commissioning update command for Target devices */
  identifySubscribe(&subcriber);

  basicClusterInit();
  identifyClusterInit();
  thermostatClusterInit();
  thermostatUiConfClusterInit();
  occupancySensingClusterInit();
  fanControlClusterInit();
  diagnosticsClusterInit();
  humidityMeasurementClusterInit();
  groupsClusterInit();
  scenesClusterInit();
  thTemperatureMeasurementClusterInit();

  if (PDS_IsAbleToRestore(HA_APP_MEMORY_MEM_ID))
    PDS_Restore(HA_APP_MEMORY_MEM_ID);

  ZCL_StartReporting();

  /* Timer update the attribute values of various sensor types */
  HAL_StartAppTimer(&sensorAttributeUpdateTimer);
}

/**************************************************************************//**
\breif Performs security initialization actions
******************************************************************************/
void appSecurityInit(void)
{
  ZCL_Set_t zclSet;

  ZCL_ResetSecurity();
  zclSet.attr.id = ZCL_LINK_KEY_DESC_ID;
  zclSet.attr.value.linkKeyDesc = &thermostatKeyDesc;
  ZCL_Set(&zclSet);
}
/**************************************************************************//**
\brief Device common task handler
******************************************************************************/
void appDeviceTaskHandler(void)
{
  switch (appDeviceState) // Actual device state when one joined network
  {
    case DEVICE_INITIAL_STATE:
      {
        appDeviceState = DEVICE_ACTIVE_IDLE_STATE;
      }
#ifdef OTAU_CLIENT
      startOtauClient(&thClientClusters[TH_CLIENT_CLUSTERS_COUNT - 1]);
#endif
      break;
    case DEVICE_ACTIVE_IDLE_STATE:
    default:
      break;
  }
}

/**************************************************************************//**
\brief Gets bind request

\return pointer to a bind request used by HA device
******************************************************************************/
AppBindReq_t **getDeviceBindRequest(void)
{
  return NULL;
}

/**************************************************************************//**
\brief Stops application
******************************************************************************/
void appStop(void)
{
  identifyClusterStop();
}

/**************************************************************************//**
\brief Asks device if it is an initiator

\returns true if it is, false otherwise
******************************************************************************/
bool appIsInitiator(void)
{
  return false;
}

/**************************************************************************//**
\brief EZ-Mode done callback

\returns function which is called by EZ-Mode manager when it is done
******************************************************************************/
void appEzModeDone(void)
{}

/**************************************************************************//**
\brief Update Commissioning State received callback

\param[in] addressing - pointer to addressing information;
\param[in] payload - data pointer
******************************************************************************/
static void updateCommissioningStateCb(ZCL_Addressing_t *addressing, ZCL_UpdateCommissioningState_t *payload)
{
  handleThConfigReporting();
  if (thClustersBoundMask)
    ZCL_StartReporting();
  (void)addressing, (void)payload;
}
/**************************************************************************//**
\brief Handling configure reporting after Commissioning

******************************************************************************/
static void handleThConfigReporting(void)
{
  static ReportingState_t configureReportingState = CONFIG_REPORT_INIT_STATE;
  switch (configureReportingState)
  {
    case CONFIG_REPORT_INIT_STATE:
      if (thClustersBoundMask & THERMOSTAT_CLUSTER_BOUND)
      {
        sendConfigureReportingToNotify(APP_SRC_ENDPOINT_ID, APP_ENDPOINT_COMBINED_INTERFACE, THERMOSTAT_CLUSTER_ID,
          ZCL_THERMOSTAT_CLUSTER_LOCAL_TEMPERATURE_SERVER_ATTRIBUTE_ID, THERMOSTAT_LOCAL_TEMPERATURE_MAX_REPORT_PERIOD, thConfigureReportingResp);
        configureReportingState = THERMOSTAT_REPORTING_CONFIGURED;
        thClustersBoundMask &= ~THERMOSTAT_CLUSTER_BOUND;
  	    break;
      }
    case THERMOSTAT_REPORTING_CONFIGURED:
      if (thClustersBoundMask & OCCUPANCY_SENSING_CLUSTER_BOUND)
      {
	    sendConfigureReportingToNotify(APP_SRC_ENDPOINT_ID, APP_ENDPOINT_COMBINED_INTERFACE, OCCUPANCY_SENSING_CLUSTER_ID,
	      ZCL_OCCUPANCY_SENSING_CLUSTER_OCCUPANCY_SERVER_ATTRIBUTE_ID, OCCUPANCY_SENSING_VAL_MAX_REPORT_PERIOD, thConfigureReportingResp);
	    configureReportingState = OCCUPANCY_REPORTING_CONFIGURED;
        thClustersBoundMask &= ~OCCUPANCY_SENSING_CLUSTER_BOUND;
	    break;
      }
    case OCCUPANCY_REPORTING_CONFIGURED:
      if (thClustersBoundMask & HUMIDITY_MEASUREMENT_CLUSTER_BOUND)
      {
	    sendConfigureReportingToNotify(APP_SRC_ENDPOINT_ID, APP_ENDPOINT_COMBINED_INTERFACE, HUMIDITY_MEASUREMENT_CLUSTER_ID,
	      ZCL_HUMIDITY_MEASUREMENT_CLUSTER_SERVER_MEASURED_VALUE_ATTRIBUTE_ID, HUMIDITY_MEASUREMENT_VAL_MAX_REPORT_PERIOD, thConfigureReportingResp);
	    configureReportingState = HUMIDITY_MEASURED_VALUE_REPORTING_CONFIGURED;
	    break;
      }		

    case HUMIDITY_MEASURED_VALUE_REPORTING_CONFIGURED:
      if (thClustersBoundMask & HUMIDITY_MEASUREMENT_CLUSTER_BOUND)
      {
        sendConfigureReportingToNotify(APP_SRC_ENDPOINT_ID, APP_ENDPOINT_COMBINED_INTERFACE, HUMIDITY_MEASUREMENT_CLUSTER_ID,
	      ZCL_HUMIDITY_MEASUREMENT_CLUSTER_SERVER_TOLERANCE_ATTRIBUTE_ID, HUMIDITY_MEASUREMENT_VAL_MAX_REPORT_PERIOD, thConfigureReportingResp);
        configureReportingState = HUMIDITY_TOLERANCE_VALUE_REPORTING_CONFIGURED;
        thClustersBoundMask &= ~HUMIDITY_MEASUREMENT_CLUSTER_BOUND;
        break;
      }

    case HUMIDITY_TOLERANCE_VALUE_REPORTING_CONFIGURED:
      if (thClustersBoundMask & TEMPERATURE_MEASUREMENT_CLUSTER_BOUND)		
      {
	    sendConfigureReportingToNotify(APP_SRC_ENDPOINT_ID, APP_ENDPOINT_COMBINED_INTERFACE, TEMPERATURE_MEASUREMENT_CLUSTER_ID,
	      ZCL_TEMPERATURE_MEASUREMENT_CLUSTER_SERVER_MEASURED_VALUE_ATTRIBUTE_ID, TEMPERATURE_MEASUREMENT_VAL_MAX_REPORT_PERIOD, thConfigureReportingResp);
	    configureReportingState =  TEMPERATURE_MEASURED_VALUE_REPORTING_CONFIGURED;
	    break;
      }

    case TEMPERATURE_MEASURED_VALUE_REPORTING_CONFIGURED:
      if (thClustersBoundMask & TEMPERATURE_MEASUREMENT_CLUSTER_BOUND)
      {
	    sendConfigureReportingToNotify(APP_SRC_ENDPOINT_ID, APP_ENDPOINT_COMBINED_INTERFACE, TEMPERATURE_MEASUREMENT_CLUSTER_ID,
	      ZCL_TEMPERATURE_MEASUREMENT_CLUSTER_SERVER_TOLERANCE_ATTRIBUTE_ID, TEMPERATURE_MEASUREMENT_VAL_MAX_REPORT_PERIOD, thConfigureReportingResp);
	    configureReportingState = CONFIGURE_REPORTING_COMPLETED;
        thClustersBoundMask &= ~TEMPERATURE_MEASUREMENT_CLUSTER_BOUND;
	    break;
      }
    case CONFIGURE_REPORTING_COMPLETED:
      configureReportingState = CONFIG_REPORT_INIT_STATE;
      break;
    default:
    break;
  }
}

/**************************************************************************//**
\brief Indication of configure reporting response

\param[in] resp - pointer to response
******************************************************************************/
static void thConfigureReportingResp(ZCL_Notify_t *ntfy)
{
  handleThConfigReporting();

  (void)ntfy;
}
/**************************************************************************//**
\brief ZDO Binding indication function

\param[out] bindInd - ZDO bind indication parameters structure pointer. For details go to
            ZDO_BindInd_t declaration
******************************************************************************/
void ZDO_BindIndication(ZDO_BindInd_t *bindInd)
{
  switch (bindInd->clusterId)
  {
    case THERMOSTAT_CLUSTER_ID:
      thClustersBoundMask |= THERMOSTAT_CLUSTER_BOUND;
      break;
	case OCCUPANCY_SENSING_CLUSTER_ID:
      thClustersBoundMask |= OCCUPANCY_SENSING_CLUSTER_BOUND;
      break;
    case HUMIDITY_MEASUREMENT_CLUSTER_ID:
      thClustersBoundMask |= HUMIDITY_MEASUREMENT_CLUSTER_BOUND;
      break;
    case TEMPERATURE_MEASUREMENT_CLUSTER_ID:
      thClustersBoundMask |= TEMPERATURE_MEASUREMENT_CLUSTER_BOUND;
      break;
	default:
      break;
  }
  (void)bindInd;
}

/**************************************************************************//**
\brief ZDO Unbinding indication function

\param[out] unbindInd - ZDO unbind indication parameters structure pointer. For details go to
            ZDO_UnbindInd_t declaration
******************************************************************************/
void ZDO_UnbindIndication(ZDO_UnbindInd_t *unbindInd)
{
  (void)unbindInd;
}

/**************************************************************************//**
\brief Periodic update of various attributes of different sensors
*****************************************************************************/
static void updateSensorsAttributeValues(void)
{
  humidityMeasurementUpdateMeasuredValue();
  humidityMeasurementUpdateTolerance();
}

#endif // APP_DEVICE_TYPE_THERMOSTAT
// eof thermostat.c
