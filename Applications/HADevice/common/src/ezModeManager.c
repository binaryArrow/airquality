/************************************************************************//**
  \file ezModeManager.c

  \brief
    EZ-Mode implementation.

  \author
    Atmel Corporation: http://www.atmel.com \n
    Support email: avr@atmel.com

  Copyright (c) 2008-2013, Atmel Corporation. All rights reserved.
  Licensed under Atmel's Limited License Agreement (BitCloudTM).

  \internal
    History:
    10.09.13 N. Fomin - Created.
******************************************************************************/

/*******************************************************************************
                    Includes section
*******************************************************************************/
#include <ezModeManager.h>
#include <identifyCluster.h>
#include <zdo.h>
#include <appConsts.h>
#include <zclDevice.h>
#include <zclParser.h>
#include <identifyCluster.h>

/******************************************************************************
                    Defines section
******************************************************************************/
#define EZ_MODE_INTERVAL                180000UL /* three minutes */
#define EZ_MODE_IDENTIFY_QUERY_INTERVAL 30000UL
#define EZ_MODE_IDENTIFY_TIME           180U

#define MAX_MATCH_DESC_RESP_AMOUNT 1 // Maximum amount of stored match descriptors
#define MAX_CLUSTERS_AMOUNT_TO_BIND       15// Maximum amount of cluster to be bound

/******************************************************************************
                    Types section
******************************************************************************/
typedef struct
{
  uint8_t      AppInClustersCount;
  ClusterId_t  AppInClustersList[MAX_CLUSTERS_AMOUNT_TO_BIND];
  uint8_t      AppOutClustersCount;
  ClusterId_t  AppOutClustersList[MAX_CLUSTERS_AMOUNT_TO_BIND];
} MatchedClusterList_t;

typedef struct
{
  ZDO_ZdpReq_t         zdpReq;
  ExtAddr_t            extAddr;
  AppBindReq_t         *appBindReq[APP_ENDPOINTS_AMOUNT];
  uint8_t              matchesReceived;
  uint8_t              clusterNumber;
  uint8_t              endpointNumber;
  ZDO_MatchDescResp_t  matchDescResp[MAX_MATCH_DESC_RESP_AMOUNT];
  MatchedClusterList_t matchedClusterList;
  bool                 client;
  ClusterId_t          clusterId;
  bool                 isInProgress;
  bool                 isBindingStarted;
  void                 (*cb)(void);
} EzModeManagerMem_t;


/******************************************************************************
                    Prototypes section
******************************************************************************/
static void ezModeOpenNetwork(void);
static void zdoPermitJoiningResponse(ZDO_ZdpResp_t *conf);

static void invokeEzModeFindingAndBindingOnTarget(void);
static void invokeEzModeFindingAndBindingOnInitiator(void);

static void ezModeTimerFired(void);
static void ezModeIdentifyQueryTimerFired(void);
static void identifyQueryResponseCb(ZCL_Addressing_t *addressing, ZCL_IdentifyQueryResponse_t *payload);

static void matchBindDevices(void);
static void zdpMatchDescResp(ZDO_ZdpResp_t *resp);
static void matchHandlingFinished(void);
static void doIeeeAddrReq(void);
static void zdpIeeeAddrResp(ZDO_ZdpResp_t *resp);
static void doApsAndZdoBinding(void);
static bool doApsBinding(void);
static void zdpBindResp(ZDO_ZdpResp_t *resp);
static void commissionNextEndpoint(void);
static void doSimpleDescReq(void);
static void zdpSimpleDescResp(ZDO_ZdpResp_t *resp);
static void continueWithApsZdoBinding(void);
static void continueWithOnlyApsBinding(void);
static void clearMatchedClsterList(void);

/******************************************************************************
                    Local variables section
******************************************************************************/
static HAL_AppTimer_t ezModeTimer =
{
  .interval = EZ_MODE_INTERVAL,
  .mode     = TIMER_ONE_SHOT_MODE,
  .callback = ezModeTimerFired,
};
static HAL_AppTimer_t ezModeIdentifyQueryTimer =
{
  .interval = EZ_MODE_IDENTIFY_QUERY_INTERVAL,
  .mode     = TIMER_REPEAT_MODE,
  .callback = ezModeIdentifyQueryTimerFired,
};

static IdentifySubscriber_t subcriber =
{
  .identifyQueryResponse = identifyQueryResponseCb
};

static EzModeManagerMem_t ezModeMem;
static bool isDeviceInitiator;
static bool apsBindingSuccess = false;

/*******************************************************************************
                    Implementation section
*******************************************************************************/
/**************************************************************************//**
\brief Initializes EZ-Mode manager

\param[in] isInitiator - should be set to true is device acts as an initiator
  of EZ-Mode, to false otherwise
******************************************************************************/
void initEzModeManager(bool isInitiator)
{
  isDeviceInitiator = isInitiator;
  identifySubscribe(&subcriber);
}

/**************************************************************************//**
\brief Starts EZ-Mode

\param[in] cb - callback which is called when EZ+Mode is finished
******************************************************************************/
void invokeEzMode(void (*cb)(void))
{
  if (ZDO_IN_NETWORK_STATUS != ZDO_GetNwkStatus())
    return;

  if (ezModeMem.isInProgress)
    return;

  memset(&ezModeMem, 0, sizeof(EzModeManagerMem_t));
  ezModeMem.isInProgress = true;
  ezModeMem.cb = cb;
  ezModeOpenNetwork();
}
/**************************************************************************//**
\brief resets ezmodeInProgress state
******************************************************************************/
void resetEzModeInProgress(void)
{
  ezModeMem.isInProgress = false;
  ezModeMem.isBindingStarted = false;
}

/**************************************************************************//**
\brief Checks whether EZ-Mode commissioning is in progress

\returns true if it is, false otherwise
******************************************************************************/
bool isEzModeInProgress(void)
{
  return ezModeMem.isInProgress;
}

/**************************************************************************//**
\brief Sends broadcast permit join with permit time of 3 minutes
******************************************************************************/
static void ezModeOpenNetwork(void)
{
  ZDO_ZdpReq_t *zdpReq = &ezModeMem.zdpReq;
  ZDO_MgmtPermitJoiningReq_t *permit = &zdpReq->req.reqPayload.mgmtPermitJoiningReq;

  zdpReq->ZDO_ZdpResp             = zdoPermitJoiningResponse;
  zdpReq->reqCluster              = MGMT_PERMIT_JOINING_CLID;
  zdpReq->dstAddrMode             = APS_SHORT_ADDRESS;
  zdpReq->dstAddress.shortAddress = RX_ON_WHEN_IDLE_ADDR;

  permit->permitDuration = EZ_MODE_IDENTIFY_TIME;
  ZDO_ZdpReq(zdpReq);
}

/**************************************************************************//**
\brief Response to permit join request

\param[in] resp - pointer to response
******************************************************************************/
static void zdoPermitJoiningResponse(ZDO_ZdpResp_t *conf)
{
  (void)conf;
  if (isDeviceInitiator)
  {
    uint8_t deviceType;
    CS_ReadParameter(CS_DEVICE_TYPE_ID, &deviceType);
    invokeEzModeFindingAndBindingOnInitiator();
    /* Start identifying also as target */
    if (DEVICE_TYPE_COORDINATOR == deviceType)
      idetifyStartIdentifying(EZ_MODE_IDENTIFY_TIME);
  }
  else
    invokeEzModeFindingAndBindingOnTarget();
}

/**************************************************************************//**
\brief Starts EZ-Mode on Target device
******************************************************************************/
static void invokeEzModeFindingAndBindingOnTarget(void)
{
  idetifyStartIdentifying(EZ_MODE_IDENTIFY_TIME);
  ezModeMem.isInProgress = false;
  if (ezModeMem.cb)
    ezModeMem.cb();
}

/**************************************************************************//**
\brief Starts EZ-Mode on Initiator device
******************************************************************************/
static void invokeEzModeFindingAndBindingOnInitiator(void)
{
  HAL_StopAppTimer(&ezModeTimer);
  HAL_StopAppTimer(&ezModeIdentifyQueryTimer);
  HAL_StartAppTimer(&ezModeTimer);
  HAL_StartAppTimer(&ezModeIdentifyQueryTimer);
  identifySendIdentifyQuery(APS_SHORT_ADDRESS, ALL_DEVICES_IN_PAN_ADDR, APS_BROADCAST_ENDPOINT);
}

/**************************************************************************//**
\brief EZ-Mode timer has fired
******************************************************************************/
static void ezModeTimerFired(void)
{
  HAL_StopAppTimer(&ezModeIdentifyQueryTimer);
  ezModeMem.isInProgress = false;
  ezModeMem.isBindingStarted = false;
}

/**************************************************************************//**
\brief EZ-Mode Identify Query timer has fired
******************************************************************************/
static void ezModeIdentifyQueryTimerFired(void)
{
  identifySendIdentifyQuery(APS_SHORT_ADDRESS, ALL_DEVICES_IN_PAN_ADDR, APS_BROADCAST_ENDPOINT);
}

/**************************************************************************//**
\brief Identify Query response received callback

\param[in] addressing - pointer to addressing information;
\param[in] payload - data pointer
******************************************************************************/
static void identifyQueryResponseCb(ZCL_Addressing_t *addressing, ZCL_IdentifyQueryResponse_t *payload)
{
  if (isEzModeInProgress() && !ezModeMem.isBindingStarted)
  {
    HAL_StopAppTimer(&ezModeIdentifyQueryTimer);
    HAL_StopAppTimer(&ezModeTimer);

    ezModeMem.isBindingStarted = true;
    memcpy(&ezModeMem.appBindReq, getDeviceBindRequest(), sizeof(ezModeMem.appBindReq));
    for (uint8_t epCount = 0; epCount < APP_ENDPOINTS_AMOUNT; epCount++)
      ezModeMem.appBindReq[epCount]->nwkAddrOfInterest = addressing->addr.shortAddress;

    commissionNextEndpoint();
  }
  (void)payload;
}

/**************************************************************************//**
\brief ezmode commissioing on Endpoint
******************************************************************************/
void commissionNextEndpoint(void)
{
  /* Done with all Endpoints on the initiator device */
  if (APP_ENDPOINTS_AMOUNT == ezModeMem.endpointNumber)
  {
    identifyUpdateCommissioningState(true, true);
    identifySendUpdateCommissioningState(APS_SHORT_ADDRESS, ezModeMem.appBindReq[ezModeMem.endpointNumber-1]->nwkAddrOfInterest,
      APS_BROADCAST_ENDPOINT, ZCL_UPDATE_COMMISSIONING_STATE_ACTION_SET, 0x03);

    ezModeMem.isBindingStarted = false;
    ezModeMem.isInProgress = false;

    if (ezModeMem.cb)
      ezModeMem.cb();
  }
  else
  {
    /* reset the ez Mode parameters */
    ezModeMem.client = 0;
    ezModeMem.clusterNumber = 0;

    matchBindDevices();
  }
}

/**************************************************************************//**
\brief Starts service discovery and binding process
******************************************************************************/
static void matchBindDevices(void)
{
  ZDO_ZdpReq_t *zdpReq = &ezModeMem.zdpReq;
  ZDO_MatchDescReq_t *matchDescReq = &zdpReq->req.reqPayload.matchDescReq;
  AppBindReq_t *appBindReq = ezModeMem.appBindReq[ezModeMem.endpointNumber];

  ezModeMem.matchesReceived = 0;

  zdpReq->ZDO_ZdpResp             = zdpMatchDescResp;
  zdpReq->reqCluster              = MATCH_DESCRIPTOR_CLID;
  zdpReq->dstAddrMode             = APS_SHORT_ADDRESS;
  zdpReq->dstAddress.shortAddress = appBindReq->nwkAddrOfInterest;

  matchDescReq->nwkAddrOfInterest = appBindReq->nwkAddrOfInterest;
  matchDescReq->profileId         = appBindReq->profile;

  /* Interested In and Out clusters to bind */
  matchDescReq->numInClusters = appBindReq->remoteServersCnt;
  for (uint8_t i = 0; i < appBindReq->remoteServersCnt; i++)
    matchDescReq->inClusterList[i] = appBindReq->remoteServers[i];

  matchDescReq->numOutClusters = appBindReq->remoteClientsCnt;
  for (uint8_t i = 0; i < appBindReq->remoteClientsCnt; i++)
    matchDescReq->outClusterList[i] = appBindReq->remoteClients[i];

  ZDO_ZdpReq(&ezModeMem.zdpReq);
}

/**************************************************************************//**
\brief Response to match descriptor request

\param[in] resp - pointer to response
******************************************************************************/
static void zdpMatchDescResp(ZDO_ZdpResp_t *resp)
{
  ZDO_MatchDescResp_t *matchResp = &resp->respPayload.matchDescResp;
  ZDO_Status_t status = resp->respPayload.status;

  if (ZDO_CMD_COMPLETED_STATUS == status)
    matchHandlingFinished();
  else if (ZDO_SUCCESS_STATUS != status)
  {
    ezModeMem.endpointNumber++;
    commissionNextEndpoint();
  }
  else if (MAX_MATCH_DESC_RESP_AMOUNT > ezModeMem.matchesReceived)
    memcpy(&ezModeMem.matchDescResp[ezModeMem.matchesReceived++], matchResp, sizeof(ZDO_MatchDescResp_t));
}

/**************************************************************************//**
\brief Clearing the matched clster list before going for next matched dendpoint
*******************************************************************************/
static void clearMatchedClsterList(void)
{
  memset(&ezModeMem.matchedClusterList, 0, sizeof(MatchedClusterList_t));
}

/**************************************************************************//**
\brief Processing after each match handling
*******************************************************************************/
static void matchHandlingFinished(void)
{
  clearMatchedClsterList();
  if ((ezModeMem.matchesReceived) && (ezModeMem.matchDescResp[ezModeMem.matchesReceived-1].matchLength))
    doSimpleDescReq();
  else //done with all matched endpoints in the match desc resp, continue with next ep on initiator,if any
  {
    ezModeMem.matchesReceived = 0;
    ezModeMem.endpointNumber++;
    commissionNextEndpoint();
  }
}

/**************************************************************************//**
\brief Sends the simple Descriptor request

\param[in] nwkAddrOfInterest - nwk Address of Interest
\param[in] endpoint          - Endpoint for which the simple desctiptor is requested
******************************************************************************/
static void doSimpleDescReq(void)
{
  ZDO_ZdpReq_t *zdpReq = &ezModeMem.zdpReq;
  ZDO_SimpleDescReq_t *simpleDescReq = &zdpReq->req.reqPayload.simpleDescReq;
  ZDO_MatchDescResp_t *resp = &ezModeMem.matchDescResp[ezModeMem.matchesReceived - 1];

  zdpReq->ZDO_ZdpResp              = zdpSimpleDescResp;
  zdpReq->reqCluster               = SIMPLE_DESCRIPTOR_CLID;
  zdpReq->dstAddrMode              = APS_SHORT_ADDRESS; 

  zdpReq->dstAddress.shortAddress  = resp->nwkAddrOfInterest;
  simpleDescReq->nwkAddrOfInterest = resp->nwkAddrOfInterest;
  simpleDescReq->endpoint          = resp->matchList[resp->matchLength-1];

  ZDO_ZdpReq(zdpReq);
}

/**************************************************************************//**
\brief simple Descriptor response callback

\param[in] resp - response payload
******************************************************************************/
static void zdpSimpleDescResp(ZDO_ZdpResp_t *resp)
{
  DeviceType_t deviceType;
  AppBindReq_t *appBindReq = ezModeMem.appBindReq[ezModeMem.endpointNumber];
  ZDO_SimpleDescResp_t* simpleDesResp = &resp->respPayload.simpleDescResp;

  CS_ReadParameter(CS_DEVICE_TYPE_ID, &deviceType);

  if (ZDO_SUCCESS_STATUS == resp->respPayload.status)
  {
    for (uint8_t i = 0;i < simpleDesResp->simpleDescriptor.AppInClustersCount ;i++)
      for (uint8_t j = 0;j < appBindReq->remoteServersCnt; j++)
        if (simpleDesResp->simpleDescriptor.AppInClustersList[i] == appBindReq->remoteServers[j])
          ezModeMem.matchedClusterList.AppInClustersList[ezModeMem.matchedClusterList.AppInClustersCount++] = appBindReq->remoteServers[j];

    for (uint8_t i = 0;i < simpleDesResp->simpleDescriptor.AppOutClustersCount; i++)
      for (uint8_t j = 0;j < appBindReq->remoteClientsCnt; j++)
        if (simpleDesResp->simpleDescriptor.AppOutClustersList[i] == appBindReq->remoteClients[j])
          ezModeMem.matchedClusterList.AppOutClustersList[ezModeMem.matchedClusterList.AppOutClustersCount++] = appBindReq->remoteClients[j];

    if (!ezModeMem.extAddr)
    {
      doIeeeAddrReq();
      return;
    }
    /* Continue with binding as IEEE Address is known */ 
    if (DEVICE_TYPE_END_DEVICE == deviceType)
      continueWithOnlyApsBinding();
    else
      continueWithApsZdoBinding();
  }
  else //continue with the next enpoint in the match desc response, if any
  {
    ezModeMem.matchDescResp[ezModeMem.matchesReceived-1].matchLength--;
    matchHandlingFinished();
  }
}

/**************************************************************************//**
\brief Performs IEEE adddress request
*******************************************************************************/
static void doIeeeAddrReq(void)
{
  ZDO_ZdpReq_t *zdpReq = &ezModeMem.zdpReq;
  ZDO_IeeeAddrReq_t *ieeeAddrReq = &zdpReq->req.reqPayload.ieeeAddrReq;

  ieeeAddrReq->nwkAddrOfInterest = ezModeMem.matchDescResp[ezModeMem.matchesReceived - 1].nwkAddrOfInterest;
  ieeeAddrReq->reqType           = 0;
  ieeeAddrReq->startIndex        = 0;

  zdpReq->ZDO_ZdpResp             = zdpIeeeAddrResp;
  zdpReq->reqCluster              = IEEE_ADDR_CLID;
  zdpReq->dstAddrMode             = APS_SHORT_ADDRESS;
  zdpReq->dstAddress.shortAddress = ieeeAddrReq->nwkAddrOfInterest;
  zdpReq->ZDO_ZdpResp             = zdpIeeeAddrResp;
  zdpReq->reqCluster              = IEEE_ADDR_CLID;

  ZDO_ZdpReq(zdpReq);
}

/**************************************************************************//**
\brief ZDP IEEE response callback

\param[in] resp - pointer to response
*******************************************************************************/
static void zdpIeeeAddrResp(ZDO_ZdpResp_t *resp)
{
  if (ZDO_SUCCESS_STATUS == resp->respPayload.status)
  {
    DeviceType_t deviceType;
    CS_ReadParameter(CS_DEVICE_TYPE_ID, &deviceType);
    ezModeMem.extAddr = ((ZDO_IeeeAddrResp_t *)&resp->respPayload.ieeeAddrResp)->ieeeAddrRemote;  

    if (DEVICE_TYPE_END_DEVICE == deviceType)
      continueWithOnlyApsBinding();
    else
      continueWithApsZdoBinding();
  }
  else //continue with the next enpoint in the matched list
  {
    ezModeMem.matchDescResp[ezModeMem.matchesReceived-1].matchLength--;
    matchHandlingFinished();
  }
}

/**************************************************************************//**
\brief binding the matched clusters - aps binding
*******************************************************************************/
static void continueWithOnlyApsBinding(void)
{
  while (ezModeMem.matchedClusterList.AppInClustersCount != ezModeMem.clusterNumber)
  {
     ezModeMem.clusterId = ezModeMem.matchedClusterList.AppInClustersList[ezModeMem.clusterNumber];
     if (doApsBinding() && (ezModeMem.appBindReq[ezModeMem.endpointNumber]->callback))
     {
       ezModeMem.appBindReq[ezModeMem.endpointNumber]->callback(ezModeMem.clusterId);
     }
     ezModeMem.clusterNumber++;
  }

  ezModeMem.clusterNumber = 0;

  while (ezModeMem.matchedClusterList.AppOutClustersCount != ezModeMem.clusterNumber)
  {
     ezModeMem.clusterId = ezModeMem.matchedClusterList.AppOutClustersList[ezModeMem.clusterNumber];
     if (doApsBinding() && (ezModeMem.appBindReq[ezModeMem.endpointNumber]->callback))
     {
       ezModeMem.appBindReq[ezModeMem.endpointNumber]->callback(ezModeMem.clusterId);
     }
     ezModeMem.clusterNumber++;
  }

  ezModeMem.clusterNumber = 0;
  ezModeMem.matchDescResp[ezModeMem.matchesReceived-1].matchLength--;
  matchHandlingFinished();
}

/**************************************************************************//**
\brief binding the matched clusters - aps and zdo binding
*******************************************************************************/
static void continueWithApsZdoBinding(void)
{
  if (!ezModeMem.client)
  {
    if (ezModeMem.matchedClusterList.AppInClustersCount == ezModeMem.clusterNumber)
    {
      ezModeMem.client = true;
      ezModeMem.clusterNumber = 0;
    }
    else
    {
      ezModeMem.clusterId = ezModeMem.matchedClusterList.AppInClustersList[ezModeMem.clusterNumber];
      doApsAndZdoBinding();
      ezModeMem.clusterNumber++;
      return;
    }
  }

  if (ezModeMem.matchedClusterList.AppOutClustersCount == ezModeMem.clusterNumber)
  {
    ezModeMem.matchDescResp[ezModeMem.matchesReceived-1].matchLength--;
    ezModeMem.client = false;
    ezModeMem.clusterNumber = 0;
    matchHandlingFinished();
    return;
  }

  ezModeMem.clusterId = ezModeMem.matchedClusterList.AppOutClustersList[ezModeMem.clusterNumber];
  doApsAndZdoBinding();
  ezModeMem.clusterNumber++;
}

/**************************************************************************//**
\brief Initiates APS binding

\param[in] ieeeAddr - address to bind
\returns true in case of success, false incase of fail
*******************************************************************************/
static bool doApsBinding(void)
{
  APS_BindReq_t apsBindReq;
  ExtAddr_t ownExtAddr;
  ZDO_MatchDescResp_t *resp;
  AppBindReq_t *appBindReq = ezModeMem.appBindReq[ezModeMem.endpointNumber];
  CS_ReadParameter(CS_UID_ID, &ownExtAddr);

  resp = &ezModeMem.matchDescResp[ezModeMem.matchesReceived - 1];
  // APS binding  
  apsBindReq.srcAddr = ownExtAddr;
  apsBindReq.srcEndpoint = appBindReq->srcEndpoint;
  apsBindReq.clusterId = ezModeMem.clusterId;
  apsBindReq.dstAddrMode = APS_EXT_ADDRESS;
  apsBindReq.dst.unicast.extAddr = ezModeMem.extAddr;
  apsBindReq.dst.unicast.endpoint = resp->matchList[resp->matchLength-1];
  APS_BindReq(&apsBindReq);

  if (APS_SUCCESS_STATUS != apsBindReq.confirm.status)
    return false;

  return true;
}

/**************************************************************************//**
\brief Initiates APS and ZDO binding

\param[in] ieeeAddr - address to bind
*******************************************************************************/
static void doApsAndZdoBinding(void)
{
  ZDO_ZdpReq_t *zdpReq = &ezModeMem.zdpReq;
  ZDO_BindReq_t *zdoBindReq = &zdpReq->req.reqPayload.bindReq;
  ExtAddr_t ownExtAddr;
  ZDO_MatchDescResp_t *resp;
  AppBindReq_t *appBindReq = ezModeMem.appBindReq[ezModeMem.endpointNumber];
  DeviceType_t deviceType;

  resp = &ezModeMem.matchDescResp[ezModeMem.matchesReceived - 1];

  CS_ReadParameter(CS_UID_ID, &ownExtAddr);
  CS_ReadParameter(CS_DEVICE_TYPE_ID, &deviceType);

  apsBindingSuccess = doApsBinding();

  zdpReq->ZDO_ZdpResp = zdpBindResp;
  zdpReq->reqCluster = BIND_CLID;
  zdpReq->dstAddrMode = APS_EXT_ADDRESS;
  COPY_EXT_ADDR(zdpReq->dstAddress.extAddress, ezModeMem.extAddr);

  COPY_EXT_ADDR(zdoBindReq->srcAddr, ezModeMem.extAddr);
  zdoBindReq->srcEndpoint = resp->matchList[resp->matchLength-1];
  zdoBindReq->clusterId = ezModeMem.clusterId;
  zdoBindReq->dstAddrMode = APS_EXT_ADDRESS;
  COPY_EXT_ADDR(zdoBindReq->dstExtAddr, ownExtAddr);
  zdoBindReq->dstEndpoint = appBindReq->srcEndpoint;

  ZDO_ZdpReq(zdpReq);
}

/**************************************************************************//**
\brief Response to ZDP Bind request

\param[in] resp - pointer to response
*******************************************************************************/
static void zdpBindResp(ZDO_ZdpResp_t *resp)
{
  if (apsBindingSuccess && (!resp->respPayload.bindResp.status) && (ezModeMem.appBindReq[ezModeMem.endpointNumber]->callback))
    ezModeMem.appBindReq[ezModeMem.endpointNumber]->callback(ezModeMem.clusterId);

  (void)resp;
  continueWithApsZdoBinding();
}

// eof ezModeManager.c
