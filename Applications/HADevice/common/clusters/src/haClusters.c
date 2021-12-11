/**************************************************************************//**
  \file haClusters.c

  \brief
    Clusters implementation.

  \author
    Atmel Corporation: http://www.atmel.com \n
    Support email: avr@atmel.com

  Copyright (c) 2008-2013, Atmel Corporation. All rights reserved.
  Licensed under Atmel's Limited License Agreement (BitCloudTM).

  \internal
    History:
    10.09.13 N. Fomin - Created.
******************************************************************************/

/******************************************************************************
                    Includes section
******************************************************************************/
#include <haClusters.h>
#include <commandManager.h>
#include <uartManager.h>
#include <clusters.h>
#include <zdo.h>
/******************************************************************************
                    Prototypes section
******************************************************************************/
static void ZCL_ConfigureReportingResp(ZCL_Notify_t *ntfy);
static void zdpSimpleDescResponse(ZDO_ZdpResp_t *resp);
static void zdpMatchDescResponse(ZDO_ZdpResp_t *resp);
/******************************************************************************
                    Local variables section
******************************************************************************/
static DescModeManagerMem_t descModeMem;
/******************************************************************************
                    Implementation section
******************************************************************************/
/**************************************************************************//**
\brief Fills ZCL Request structure

\param[out] req     - pointer to zcl command request;
\param[in]  command - command id;
\param[in] size     - the size of request payload
******************************************************************************/
void fillCommandRequest(ZCL_Request_t *req, uint8_t command, uint8_t size)
{
  req->id              = command;
  req->requestLength   = size;
  req->endpointId      = APP_SRC_ENDPOINT_ID;
  req->defaultResponse = ZCL_FRAME_CONTROL_DISABLE_DEFAULT_RESPONSE;
}

/**************************************************************************//**
\brief Fills zcl addressing structure

\param[out] addressing - pointer to the structure to be filled;
\param[in]  mode       - addressing mode;
\param[in]  addr       - short address of destination mode;
\param[in]  ep         - endpoint number of destination node;
\param[in]  cluster    - cluster id
******************************************************************************/
void fillDstAddressing(ZCL_Addressing_t *addressing, APS_AddrMode_t mode, ShortAddr_t addr, Endpoint_t ep, ClusterId_t cluster)
{
  addressing->addrMode             = mode;
  addressing->addr.shortAddress    = addr;
  addressing->profileId            = PROFILE_ID_HOME_AUTOMATION;
  addressing->endpointId           = ep;
  addressing->clusterId            = cluster;
  addressing->clusterSide          = ZCL_CLUSTER_SIDE_SERVER;
  addressing->manufacturerSpecCode = 0;
  addressing->sequenceNumber       = ZCL_GetNextSeqNumber();
}

/**************************************************************************//**
\brief Fills zcl addressing structure

\param[out] addressing - pointer to the structure to be filled;
\param[in]  mode       - addressing mode;
\param[in]  addr       - short address of destination mode;
\param[in]  ep         - endpoint number of destination node;
\param[in]  cluster    - cluster id
******************************************************************************/
void fillDstAddressingServer(ZCL_Addressing_t *addressing, APS_AddrMode_t mode, ShortAddr_t addr, Endpoint_t ep, ClusterId_t cluster)
{
  addressing->addrMode             = mode;
  addressing->addr.shortAddress    = addr;
  addressing->profileId            = PROFILE_ID_HOME_AUTOMATION;
  addressing->endpointId           = ep;
  addressing->clusterId            = cluster;
  addressing->clusterSide          = ZCL_CLUSTER_SIDE_CLIENT;
  addressing->manufacturerSpecCode = 0;
  addressing->sequenceNumber       = ZCL_GetNextSeqNumber();
}

/**************************************************************************//**
\brief Gets free command buffer

\returns pointer to a command buffer
******************************************************************************/
ZCL_Request_t *getFreeCommand(void)
{
  ZCL_Request_t *req;

  if (!(req = commandManagerAllocCommand()))
  {
    LOG_STRING(insufficientBuffersAmountStr, "\r\nNot enough command buffers\r\n");
    appSnprintf(insufficientBuffersAmountStr);
  }

  return req;
}

/**************************************************************************//**
\brief Fills ZCL Addressing structure

\param[out] srcAddressing - pointer to zcl addressing request of source node;
\param[in]  dstAddressing - pointer to zcl addressing request of destination node;
\param[in]  side          - cluster side of recipient side
******************************************************************************/
void fillDstAddressingViaSourceAddressing(ZCL_Addressing_t *srcAddressing, ZCL_Addressing_t *dstAddressing, uint8_t side)
{
  *srcAddressing = *dstAddressing;
  srcAddressing->clusterSide = side;
}
/*******************************************************************************
\brief Sends the simple Descriptor request

\param[in] addr - nwk Address of Interest
\param[in] ep   - Endpoint for which the simple desctiptor is requested
*****************************************************************************/
void zdpSimpleDescReq(ShortAddr_t addr,uint8_t ep)
{
  ZDO_ZdpReq_t *zdpReq = &descModeMem.zdpReq;
  ZDO_SimpleDescReq_t *simpleDescReq = &zdpReq->req.reqPayload.simpleDescReq;

  zdpReq->ZDO_ZdpResp              =zdpSimpleDescResponse;
  zdpReq->reqCluster               = SIMPLE_DESCRIPTOR_CLID;
  zdpReq->dstAddrMode              = APS_SHORT_ADDRESS; 
  zdpReq->dstAddress.shortAddress  = addr;
  simpleDescReq->nwkAddrOfInterest = addr;
  simpleDescReq->endpoint          = ep;
  ZDO_ZdpReq(zdpReq);
}
/**************************************************************************//**
\brief simple Descriptor response callback

\param[in] resp - response payload
******************************************************************************/
static void zdpSimpleDescResponse(ZDO_ZdpResp_t *resp)
{
  (void)resp;
}
/**************************************************************************//**
\brief Sends the Match Descriptor request

\param[in] addr - nwk Address of Interest
\param[in] ep   - Endpoint which requests Match desctiptor 
******************************************************************************/

void zdpMatchDescReq(ShortAddr_t addr,uint8_t ep)
{
  ZDO_ZdpReq_t *zdpReq = &descModeMem.zdpReq;
  ZDO_MatchDescReq_t *matchDescReq = &zdpReq->req.reqPayload.matchDescReq;
  uint8_t flag=0;
  AppBindReq_t **appBindRequest=getDeviceBindRequest();
  zdpReq->ZDO_ZdpResp             = zdpMatchDescResponse;
  zdpReq->reqCluster              = MATCH_DESCRIPTOR_CLID;
  zdpReq->dstAddrMode             = APS_SHORT_ADDRESS;
  zdpReq->dstAddress.shortAddress = addr;
  matchDescReq->nwkAddrOfInterest = addr;
  matchDescReq->profileId         = PROFILE_ID_HOME_AUTOMATION;
  for (uint8_t epCount = 0; epCount < APP_ENDPOINTS_AMOUNT; epCount++)
  {
    if( appBindRequest[epCount]->srcEndpoint == ep)
    {
      matchDescReq->numInClusters = appBindRequest[epCount]->remoteServersCnt;
      for (uint8_t i = 0; i < appBindRequest[epCount]->remoteServersCnt; i++)
      matchDescReq->inClusterList[i] = appBindRequest[epCount]->remoteServers[i];

      matchDescReq->numOutClusters = appBindRequest[epCount]->remoteClientsCnt;
      for (uint8_t i = 0; i < appBindRequest[epCount]->remoteClientsCnt; i++)
      matchDescReq->outClusterList[i] = appBindRequest[epCount]->remoteClients[i];
      flag++;
      break;
      }
    }
    if(flag==0)
      appSnprintf("Enter valid EP");
    else
      ZDO_ZdpReq(zdpReq);
}
/**************************************************************************//**
\brief Match Descriptor response callback

\param[in] resp - response payload
******************************************************************************/
static void zdpMatchDescResponse(ZDO_ZdpResp_t *resp)
{
  (void)resp;
}
/**************************************************************************//**
\brief Sends configure reporting request to notify another device about reporting

\param[in] endpoint  - destination endpoint;
\param[in] clusterId - cluster id;
\param[in] attrId    - attribute id;
\param[in] period    - report period
******************************************************************************/
void sendConfigureReportingToNotify(Endpoint_t srcEndpoint, Endpoint_t dstEndpoint, ClusterId_t clusterId, ZCL_AttributeId_t attrId, ZCL_ReportTime_t period, ConfigureReportResp_t configureRespCb)
{
  ZCL_Request_t *req;
  ZCL_NextElement_t element;
  ZCL_ConfigureReportingReq_t configureReportingReq;

  if (!(req = getFreeCommand()))
    return;

  configureReportingReq.direction     = ZCL_FRAME_CONTROL_DIRECTION_SERVER_TO_CLIENT;
  configureReportingReq.attributeId   = attrId;
  configureReportingReq.timeoutPeriod = period;

  element.payloadLength = 0;
  element.payload       = req->requestPayload;
  element.id            = ZCL_CONFIGURE_REPORTING_COMMAND_ID;
  element.content       = &configureReportingReq;
  ZCL_PutNextElement(&element);

  fillCommandRequest(req, ZCL_CONFIGURE_REPORTING_COMMAND_ID, element.payloadLength);
  req->endpointId = srcEndpoint;
  fillDstAddressing(&req->dstAddressing, APS_NO_ADDRESS, 0, dstEndpoint, clusterId);
  req->dstAddressing.clusterSide = ZCL_CLUSTER_SIDE_CLIENT;
  if(NULL == configureRespCb)
    req->ZCL_Notify = ZCL_ConfigureReportingResp;
  else
    req->ZCL_Notify = configureRespCb;

  commandManagerSendAttribute(req);
}

/**************************************************************************//**
\brief Indication of configure reporting response

\param[in] resp - pointer to response
******************************************************************************/
static void ZCL_ConfigureReportingResp(ZCL_Notify_t *ntfy)
{
  (void)ntfy;
}

// eof haClusters.c
