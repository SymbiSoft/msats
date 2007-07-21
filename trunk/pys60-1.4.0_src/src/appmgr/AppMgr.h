//
// AppMgr.h
//
/* Copyright (c) 2005 Nokia Corporation
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
 */

#ifndef __APPMGR_H
#define __APPMGR_H

#include <aknapp.h>
#include <AknDoc.h>

class CAppMgrDocument : public CAknDocument
{
 public:
  CAppMgrDocument(CEikApplication& aApp):CAknDocument(aApp) {;}
  CFileStore* OpenFileL(TBool aDoOpen,const TDesC& aFilename,RFs& aFs);
 private: // from CEikDocument
  CEikAppUi* CreateAppUiL();
};

class CAppMgrApplication : public CAknApplication 
{
 private: // from CApaApplication
  CApaDocument* CreateDocumentL();
  TUid AppDllUid() const;
};

#endif // __APPMGR_H






