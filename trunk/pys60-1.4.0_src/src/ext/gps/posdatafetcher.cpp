/*
 * ====================================================================
 *  posdatafetcher.cpp
 *
 *  Python API to Series 60 Location Acquisition API.
 *
 * Copyright (c) 2007 Nokia Corporation
 *
 * Licensed under the Apache License, Version 2.0 (the "License");
 * you may not use this file except in compliance with the License.
 * You may obtain a copy of the License at
 *
 *     http://www.apache.org/licenses/LICENSE-2.0
 *
 * Unless required by applicable law or agreed to in writing, software
 * distributed under the License is distributed on an "AS IS" BASIS,
 * WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
 * See the License for the specific language governing permissions and
 * limitations under the License.
 * ====================================================================
 */

#include "posdatafetcher.h"


CPosDataFetcher* CPosDataFetcher::NewL(RPositioner& positioner)
{
  CPosDataFetcher* self=new (ELeave) CPosDataFetcher(positioner);
  CleanupStack::PushL(self);
  self->ConstructL();
  CleanupStack::Pop(self);
  return self;
};
	
void CPosDataFetcher::ConstructL()
{
  iWait=new (ELeave) CActiveSchedulerWait;
  CActiveScheduler::Add(this);
};
	
CPosDataFetcher::~CPosDataFetcher()
{
  Cancel();
  delete iWait;
};

void CPosDataFetcher::DoCancel()
{
  this->iPositioner.CancelRequest(EPositionerNotifyPositionUpdate);
};

void CPosDataFetcher::RunL()
{   
  this->iWait->AsyncStop();
};

void CPosDataFetcher::FetchData(TPositionInfo& positionInfo, TRequestStatus& status)
{
  this->iPositioner.NotifyPositionUpdate(positionInfo, iStatus);
  this->SetActive();
  this->iWait->Start(); 
  status=this->iStatus;
}
  
CPosDataFetcher::CPosDataFetcher(RPositioner& positioner):CActive(CActive::EPriorityStandard),iPositioner(positioner)
{
};