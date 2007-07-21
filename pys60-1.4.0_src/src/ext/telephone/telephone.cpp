/**
 * ====================================================================
 * telephone.cpp
 * Copyright (c) 2005 - 2007 Nokia Corporation
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

#include "telephone.h"

#ifdef EKA2
extern "C"
void telephone_mod_cleanup();

class TStaticData {
public:
  CTelephony *telephony;
};

TStaticData* GetTelephony()
{
  if (Dll::Tls())
  {
      return static_cast<TStaticData*>(Dll::Tls());
  }
  else 
  {
      TInt error = KErrNone;
      TStaticData* sd = NULL;
      TRAP(error, {
        sd = new (ELeave) TStaticData;
      });
      if(error!=KErrNone){
        return (TStaticData*) SPyErr_SetFromSymbianOSErr(error);
      }
      
      TRAP(error, sd->telephony = CTelephony::NewL());
      
      if (error != KErrNone){
        delete sd;
        return (TStaticData*) SPyErr_SetFromSymbianOSErr(error);
      }
      error = Dll::SetTls(sd);
      if(error!=KErrNone){
        delete sd->telephony;
        delete sd;
        return (TStaticData*) SPyErr_SetFromSymbianOSErr(error);
      }    
         
      PyThread_AtExit(telephone_mod_cleanup);
      return static_cast<TStaticData*>(Dll::Tls()); 
  }   
}

extern "C" {
  void telephone_mod_cleanup()
  {
    TStaticData* sd = NULL;
    sd = GetTelephony();
    
    if(sd!=NULL){
      delete sd->telephony;
      delete sd;
      Dll::SetTls(NULL);
    }
  }
}
#endif

//A helper function for the implementation of callbacks
//from C/C++ code to Python callables (modified from appuifwmodule.cpp)
/*TInt TPyPhoneCallBack::StateChange(TInt aPreviousState, TInt aCurrentState, TInt aErrorCode)
  {
  PyEval_RestoreThread(PYTHON_TLS->thread_state);
 
  TInt error = KErrNone;
  
  PyObject* arg = Py_BuildValue("(iii)", aPreviousState, aCurrentState, aErrorCode);
  PyObject* rval = PyEval_CallObject(iCb, arg);
  
  Py_DECREF(arg);
  if (!rval) {
    error = KErrPython;
    if (PyErr_Occurred() == PyExc_OSError) {
      PyObject *type, *value, *traceback;
      PyErr_Fetch(&type, &value, &traceback);
      if (PyInt_Check(value))
        error = PyInt_AS_LONG(value);
    }
  }
  else
    Py_DECREF(rval);

  PyEval_SaveThread();
  return error;
  }*/

//////////////

CPhoneCall* CPhoneCall::NewL()
  {
  CPhoneCall* self = NewLC();
  CleanupStack::Pop(self); 
  return self;
  }

CPhoneCall* CPhoneCall::NewLC()
  {
  CPhoneCall* self = new (ELeave) CPhoneCall();
  CleanupStack::PushL(self);
  self->ConstructL();
  return self;
  }

CPhoneCall::CPhoneCall()
  : CActive(CActive::EPriorityStandard) 
  {
  CActiveScheduler::Add(this);
  }
  
void CPhoneCall::SetNumber(TDes& aNumber) 
  {
  iNumber = aNumber;
  iNumberSet = ETrue;
  }

#ifndef EKA2
void CPhoneCall::ConstructL()
  {
  iCallState = ENotCalling;
  iNumberSet = EFalse;
  }

CPhoneCall::~CPhoneCall()
  {
  Cancel();

  //This is the state where we should be. If not, then we need to close the
  //servers
  if (iCallState != ENotCalling) 
    {
#ifndef __WINS__
	  //Close the phone, line and call connections
	  //NOTE: This does not hang up the call
    iPhone.Close();
    iLine.Close();
    iCall.Close();

    //XXX error code
    //Unload the phone device driver
    /*error =*/ iServer.UnloadPhoneModule(KTsyName);
    /*if (error != KErrNone)
      return error;*/

	  //Close the connection to the tel server
    iServer.Close();
#endif /* __WINS__ */
    }
  }

void CPhoneCall::RunL()
  {
  switch (iCallState) 
    {
    case ECalling:
      iCallState = ECallInProgress;
      break;
    default:
      break;
    }
  }
   
void CPhoneCall::DoCancel()
  {
  iCall.DialCancel();
  iCallState = EInitialised;
  }
  
TInt CPhoneCall::Initialise()
  {
  TInt error = KErrNone;
  if (iCallState != ENotCalling)
    return EInitialiseCalledAlready;
#ifndef __WINS__

	//Create a connection to the tel server
  error = iServer.Connect();
  if (error != KErrNone)
    return error;

	//Load in the phone device driver
  error = iServer.LoadPhoneModule(KTsyName);
  if (error != KErrNone)
    return error;
  
	//Find the number of phones available from the tel server
	TInt numberPhones;
  error = iServer.EnumeratePhones(numberPhones);
  if (error != KErrNone)
    return error;

	//Check there are available phones
	if (numberPhones < 1)
		{
		return KErrNotFound;
    }

	//Get info about the first available phone
  error = iServer.GetPhoneInfo(0, iInfo);
  if (error != KErrNone)
    return error;

	//Use this info to open a connection to the phone, the phone is identified by its name
  error = iPhone.Open(iServer, iInfo.iName);
  if (error != KErrNone)
    return error;
    
  //"The phone hardware is usually automatically initialised before 
  //the first command is sent" (from SDK), no need for Initialise()

	//Get info about the first line from the phone
  error = iPhone.GetLineInfo(0, iLineInfo);
  if (error != KErrNone)
    return error;

	//Use this to open a line
  error = iLine.Open(iPhone, iLineInfo.iName);
  if (error != KErrNone)
    return error;

	//Open a new call on this line
  error = iCall.OpenNewCall(iLine, iNewCallName);
  if (error != KErrNone)
    return error;
#endif /* __WINS__ */
  iCallState = EInitialised;
    
  return error;
  }
  
TInt CPhoneCall::UnInitialise()
  {
  TInt error = KErrNone;
  
  if (IsActive())
    return EAlreadyCalling;
    
  if (iCallState == ENotCalling)
    return ENotInitialised;

#ifndef __WINS__
	//Close the phone, line and call connections
	//NOTE: This does not hang up the call
  iPhone.Close();
  iLine.Close();
  iCall.Close();

  //Unload the phone device driver
  error = iServer.UnloadPhoneModule(KTsyName);
  if (error != KErrNone)
    return error;

	//Close the connection to the tel server
  iServer.Close();
#endif /* __WINS__ */
  iCallState = ENotCalling;
  
  return error;
  }

TInt CPhoneCall::Dial()
  {
  TInt error = KErrNone;
  
  if (!iNumberSet)
    return ENumberNotSet;
    
  if (iCallState == ENotCalling)
    return ENotInitialised;

  if (IsActive())
    return EAlreadyCalling;
    
#ifndef __WINS__
  iCall.Dial(iStatus, iNumber);  
  SetActive();
#endif /* __WINS__ */  
  iCallState = ECalling;
  return error;
  }
  
TInt CPhoneCall::HangUp()
  {
  TInt error = KErrNone;
 
  if (iCallState == ECallInProgress || iCallState == ECalling) 
    {
#ifndef __WINS__
    error = iCall.HangUp(); //synchronous, should be changed to asynchronous
#endif /* __WINS__ */  
    iCallState = EInitialised;
    return error;
    }
    
  return ENotCallInProgress;
  }

/*void CPhoneCall::SetCallBack(TPyPhoneCallBack& aCb) 
  {
  iCallMe = aCb;
  iCallBackSet = ETrue;
  }*/

#else /* EKA2 */
void CPhoneCall::ConstructL()
  {
  iCallState = ENotCalling;
  iNumberSet = EFalse;
  }

CPhoneCall::~CPhoneCall()
  {
  Cancel();
  }

void CPhoneCall::RunL()
  {
  switch (iCallState) 
    {
    case ECalling:
      if(iStatus == KErrNone)
        iCallState = ECallInProgress;
      break;
    case EHangingUp:
      //if(iStatus == KErrNone)
        iCallState = EInitialised;
      break;
    default:
      break;
    }
  }
   
void CPhoneCall::DoCancel()
  {
  TStaticData* sd = NULL;
  sd = GetTelephony();
  if(sd==NULL){
    return;
  }
  // XXX CancelAsync return code handling
  if(iCallState == ECalling)
    sd->telephony->CancelAsync(CTelephony::EDialNewCallCancel);
  else if(iCallState == EHangingUp)
    sd->telephony->CancelAsync(CTelephony::EHangupCancel);
  iCallState = EInitialised;
  }
  
TInt CPhoneCall::Initialise()
  {
  TInt error = KErrNone;

  if (iCallState != ENotCalling)
    return EInitialiseCalledAlready;

  iCallState = EInitialised;
    
  return error;
  }
  
TInt CPhoneCall::UnInitialise()
  {
  TInt error = KErrNone;
  
  if (IsActive())
    return EAlreadyCalling;
    
  if (iCallState == ENotCalling)
    return ENotInitialised;

  iCallState = ENotCalling;
  
  return error;
  }

TInt CPhoneCall::Dial()
  {
  TInt error = KErrNone;
  
  TStaticData* sd = NULL;
  sd = GetTelephony();
  if(sd==NULL){
    return NULL;
  }
  
  if (!iNumberSet)
    return ENumberNotSet;
    
  if (iCallState == ENotCalling)
    return ENotInitialised;

  if (IsActive())
    return EAlreadyCalling;
    
#ifndef __WINS__
  CTelephony::TTelNumber telNumber(iNumber);
  CTelephony::TCallParamsV1 callParams;
  callParams.iIdRestrict = CTelephony::ESendMyId;
  CTelephony::TCallParamsV1Pckg callParamsPckg(callParams);
  sd->telephony->DialNewCall(iStatus, callParamsPckg, telNumber, iCallId);
  SetActive();
#endif /* __WINS__ */  
  iCallState = ECalling;
  return error;
  }
  
TInt CPhoneCall::HangUp()
  {
  TInt error = KErrNone;
  TStaticData* sd = NULL;
  sd = GetTelephony();
  if(sd==NULL){
    return NULL;
  }
  // Check the current status (if the other side has hang-up):
#ifndef __WINS__
  CTelephony::TCallStatusV1 callStatusV1;
  CTelephony::TCallStatusV1Pckg callStatusV1Pckg(callStatusV1);

  sd->telephony->GetCallStatus(iCallId, callStatusV1Pckg);
  CTelephony::TCallStatus callStatus = callStatusV1.iStatus;
  if(callStatus == CTelephony::EStatusIdle) 
    return ENotCallInProgress;

  if (iCallState == ECallInProgress) // The call was answered, calling hang up is fine 
    {
    sd->telephony->Hangup(iStatus, iCallId); //asynchronous
    SetActive();
    iCallState = EHangingUp;
    return error;
    }
  else if (iCallState == ECalling) // Waiting to be answered, calling hang up is not fine 
    {
    sd->telephony->CancelAsync(CTelephony::EDialNewCallCancel);
    iCallState = EInitialised;
    return error;
    }
#else
  if (iCallState == ECallInProgress || iCallState == ECalling) 
    {
    iCallState = EInitialised;
    return error;
    }
#endif
  return ENotCallInProgress;
  }

#endif /* EKA2 */
