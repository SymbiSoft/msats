#
# positioning.py
#
# python interface for Location Acquisition API
#
# Copyright (c) 2007 Nokia Corporation
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
#

import e32

if e32.s60_version_info>=(3,0):
    import imp
    _locationacq=imp.load_dynamic('_locationacq', 'c:\\sys\\bin\\_locationacq.pyd')
else:
    import _locationacq
    
from locationacq import *

_pos_serv=_locationacq.position_server()
_positioner=_pos_serv.positioner()


def revdict(d):
    return dict([(d[k],k) for k in d.keys()])

_requestor_types={"service":_locationacq.req_type_service,
                  "contact":_locationacq.req_type_contact}                  
_reverse_requestor_types=revdict(_requestor_types)
                  
_requestor_formats={"application":_locationacq.req_format_app,
                    "telephone":_locationacq.req_format_tel,
                    "url":_locationacq.req_format_url,
                    "email":_locationacq.req_format_mail}
_reverse_requestor_formats=revdict(_requestor_formats)




# get information about available positioning modules
def modules():
  return _pos_serv.modules()

# get default module id
def default_module():
  return _pos_serv.default_module()

# get detailed information about the specified module  
def module_info(module_id):
  return _pos_serv.module_info(module_id)

# select a module
def select_module(module_id):
  _positioner=_pos_serv.positioner(module_id)
  
# set requestors of the service (at least one must be set)
def set_requestors(requestors):
  for item in requestors:
    item["type"]=_requestor_types[item["type"]]
    item["format"]=_requestor_formats[item["format"]]
    item["data"]=unicode(item["data"])    
  _positioner.set_requestors(requestors)

# get the position information
def position(course=0,satellites=0):
  flags=0
  if(course):
    flags|=_locationacq.info_course
  if(satellites):
    flags|=_locationacq.info_satellites
  return _positioner.position(flags)
