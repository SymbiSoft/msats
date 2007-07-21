/*
 * ====================================================================
 *  Python_appui.cpp
 *  
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

#include <utf.h>
#include "Python_appui.h"
#include "Container.h"

void initappuifw();
void finalizeappuifw();

_LIT(KDefaultScript, "default.py");
#ifdef EKA2
#if defined(__WINS__)
_LIT(KPrivate, "c:\\private\\");
#else
_LIT(KPrivate, "\\private\\");
#endif
_LIT(KSeparator, "\\");
#endif

//
// class CAmarettoCallback
//

void CAmarettoCallback::Call(void* aArg) {
  TInt error = CallImpl(aArg);     // Enter (potentially) interpreter!
  iAppUi->ReturnFromInterpreter(error);
  User::LeaveIfError(error);
}


//
// class CAmarettoAppUi
//

TInt CAmarettoAppUi::EnableTabs(const CDesCArray* aTabTexts,
                                CAmarettoCallback* aFunc)
{
  TRAPD(error, ((CAmarettoContainer*)iContainer)->
        EnableTabsL(aTabTexts, aFunc));
  return error;
}

void CAmarettoAppUi::SetActiveTab(TInt aIndex)
{
  ((CAmarettoContainer*)iContainer)->SetActiveTab(aIndex);
}

TInt CAmarettoAppUi::SetHostedControl(CCoeControl* aControl,
                                      CAmarettoCallback* aFunc)
{
  TInt rval = KErrNone;
  TRAPD(error, (rval = ((CAmarettoContainer*)iContainer)->
                SetComponentL(aControl, aFunc)));
  return ((rval != KErrNone) ? rval : error);
}

void CAmarettoAppUi::RefreshHostedControl()
{
  ((CAmarettoContainer*)iContainer)->Refresh();
}

void CAmarettoAppUi::ConstructL() 
{
#if SERIES60_VERSION>=20
  BaseConstructL(EAknEnableSkin);
#else
  BaseConstructL();
#endif /* SERIES60_VERSION */

  iContainer = CAmarettoContainer::NewL(ClientRect());
  AddToStackL(iContainer);

  iInterpreter = CSPyInterpreter::NewInterpreterL();
  iInterpreterExitPending = EFalse;
  
  SetKeyBlockMode(ENoKeyBlock);
#if SERIES60_VERSION>=28
  SetOrientationL(EAppUiOrientationAutomatic);
#endif

  initappuifw();
}

CAmarettoAppUi::~CAmarettoAppUi() 
{
  RemoveFromStack(iContainer);
  delete iContainer;
  if (iDoorObserver)
    iDoorObserver->NotifyExit(MApaEmbeddedDocObserver::EEmpty);

  if (aSubPane) {
    /* no deletion since the pointer doesn't referes to any new allocated object */
    aSubPane = NULL;
  }
}

void CAmarettoAppUi::HandleCommandL(TInt aCommand) 
{
  switch (aCommand) {
  case EAknSoftkeyExit:
    if (iExitFunc) {
      iExitFunc->Call();
      break;
    }
  case EAknSoftkeyBack:
  case EAknCmdExit:
  case EEikCmdExit: 
    DoExit();
    break;
  default:
    if (iMenuCommandFunc && (aCommand >= EPythonMenuExtensionBase) &&
    	(aCommand < (EPythonMenuExtensionBase+KMaxPythonMenuExtensions)))
      iMenuCommandFunc->Call((void*)aCommand);
    break;
  }
}

void CAmarettoAppUi::HandleForegroundEventL(TBool aForeground)
{
  if (iFocusFunc) {
    iFocusFunc->Call((void*)aForeground);
  }

  CAknAppUi::HandleForegroundEventL(aForeground);
}

void CAmarettoAppUi::ReturnFromInterpreter(TInt aError)
{
  if (aError != KErrNone)
    iInterpreter->PrintError();
  
  if (iInterpreterExitPending) {
    if (iDoorObserver)
      ProcessCommandL(EAknCmdExit);
    else
      DoExit();
  }
}

void CAmarettoAppUi::HandleResourceChangeL(TInt aType)
{
  CAknAppUi::HandleResourceChangeL(aType);
  if ( aType == KEikDynamicLayoutVariantSwitch ) {		
      SetScreenmode(iScreenMode);
  }

}

void CAmarettoAppUi::DoRunScriptL()
{
  char *argv[] = {NULL, NULL};
  int argc = 0;
  TBuf8<KMaxFileName> namebuf;

  CnvUtfConverter::ConvertFromUnicodeToUtf8(namebuf, iScriptName);
  argv[0] = (char*)namebuf.PtrZ();
  argc++;

  if (iEmbFileName.Length() > 0) {
    argv[argc] = (char*)iEmbFileName.PtrZ();
    argc++;
  }

  // Enter interpreter!
  TInt error = iInterpreter->RunScript(argc, argv);
  ReturnFromInterpreter(error);
  User::LeaveIfError(error);
}

void CAmarettoAppUi::DoExit()
{
  iInterpreterExitPending = EFalse;
  finalizeappuifw();
  delete iInterpreter;
  Exit();
}

void CAmarettoAppUi::DynInitMenuPaneL(TInt aMenuId, CEikMenuPane* aMenuPane)
{
  TAmarettoMenuDynInitParams params;

  params.iMenuId=aMenuId;
  params.iMenuPane=aMenuPane;

  if ( ((aMenuId == iExtensionMenuId) && iMenuDynInitFunc)
       || (aMenuId >= R_PYTHON_SUB_MENU_00) )
    iMenuDynInitFunc->Call((void*)&params);
}

void CAmarettoAppUi::CleanSubMenuArray() 
{
  for (int i=0; i<KMaxPythonMenuExtensions; i++)
    subMenuIndex[i] = 0;
}

void CAmarettoAppUi::SetScreenmode(TInt aMode)
{
  if (aMode == EFull) {
    iScreenMode = EFull;
    iContainer->SetRect( ApplicationRect() );
  }
  else if (aMode == ELarge) {
    CEikStatusPane* statusPane = (CEikonEnv::Static())->AppUiFactory()->StatusPane();
    TRAPD(error, (statusPane->SwitchLayoutL(R_AVKON_STATUS_PANE_LAYOUT_EMPTY) ));
    if (error != KErrNone) {
      SPyErr_SetFromSymbianOSErr(error);
	         }
    iScreenMode = ELarge;
    iContainer->SetRect( ClientRect() );
  }
  else {
    CEikStatusPane* statusPane = (CEikonEnv::Static())->AppUiFactory()->StatusPane();
	  TRAPD(error, (statusPane->SwitchLayoutL(R_AVKON_STATUS_PANE_LAYOUT_USUAL) ));
    if (error != KErrNone) {
	     SPyErr_SetFromSymbianOSErr(error);
    }  
  
    iScreenMode = ENormal;
    iContainer->SetRect( ClientRect() );
  }  
}

TInt AsyncRunCallbackL(TAny* aArg)
{
  CAmarettoAppUi* appui = (CAmarettoAppUi*)aArg;
  delete appui->iAsyncCallback;
  appui->iAsyncCallback = NULL;
  
  appui->DoRunScriptL();
  
  return KErrNone;
}

TBool CAmarettoAppUi::ProcessCommandParametersL(TApaCommand aCommand,
                                             TFileName& /*aDocumentName*/,
                                             const TDesC8& /*aTail*/) 
{
  if (aCommand == EApaCommandRun) {
#ifdef EKA2
    TUid uid = Application()->AppDllUid();
    TBuf<KMaxUidName> uidName(uid.Name());
    uidName.Delete(KMaxUidName-1,1);
    uidName.Delete(0,1);

#if defined(__WINS__)    
    TBuf<KMaxFileName> script(KPrivate);
#else
    _LIT(KFile, "default.py");
    TFileName filename(KFile());
    CompleteWithAppPath(filename);
    filename.Delete(2, 256);

    TBuf<KMaxFileName> script(filename);
    script.Append(KPrivate);

#endif
    
    script.Append(uidName);
    script.Append(KSeparator);
    script.Append(KDefaultScript);
    
    iScriptName.Copy(script);
#else
    TFileName appName = Application()->AppFullName();
    TParse p;
    p.Set(KDefaultScript, &appName, NULL);
    iScriptName.Copy(p.FullName());
#endif /*EKA2*/

    //    TCallBack cb(&AsyncRunCallbackL);
    //    iAsyncCallback = new (ELeave) CAsyncCallBack(cb, CActive::EPriorityHigh);
    //    iAsyncCallback->CallBack();
    
    DoRunScriptL();

    return EFalse;
  }
  else
    return ETrue;
}

EXPORT_C void CAmarettoAppUi::RunScriptL(const TDesC& aFileName, const TDesC* aArg)
{
  iScriptName.Copy(aFileName);
  if (aArg)
    CnvUtfConverter::ConvertFromUnicodeToUtf8(iEmbFileName, *aArg);

  TCallBack cb(&AsyncRunCallbackL, this);
  iAsyncCallback = new (ELeave) CAsyncCallBack(cb, CActive::EPriorityHigh);
  iAsyncCallback->CallBack();
}

EXPORT_C CEikAppUi* CreateAmarettoAppUi(TInt aExtensionMenuId) 
{
  return new CAmarettoAppUi(aExtensionMenuId);
}

#ifndef EKA2
GLDEF_C TInt E32Dll(TDllReason /*aReason*/)
{
  return (KErrNone);
}
#endif /*EKA2*/
