/* KeyPress (simulation of key press) developed by group 451 spring 2006 at Aalborg University from the Pys60 sysinfo template. 
We use the module to simulate hang up on nokia 6600 in silent mode.


Copyright 2006 group 451 spring 2006 at Aalborg University and Cyke64 (cyke64@gmail.com)
Licensed under the Apache License, Version 2.0 (the "License");
    you may not use this file except in compliance with the License.
    You may obtain a copy of the License at
    
     http://www.apache.org/licenses/LICENSE-2.0
     
    Unless required by applicable law or agreed to in writing, software
    distributed under the License is distributed on an "AS IS" BASIS,
    WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
    See the License for the specific language governing permissions and
    limitations under the License. 

version history
===============
 1.00 : group 451 spring 2006 at Aalborg University
          simulate key press on right menu key
 1.01 : 05-02-2006 by Cyke64
         simulate any key press from key_codes.py  
 1.02 : 05-10-2006 by Cyke64
         add Modifiers
         add key_modifiers.py


*/

/*TODO: iRepeats
*/

#include "Python.h"
#include "symbian_python_ext_util.h"
#include <e32keys.h>
#include <w32std.h>


extern "C" PyObject *
keypress_simulate_keymenu(PyObject* /*self*/)
{
                   
RWsSession ws;
   TKeyEvent key;
   ws.Connect();
   
   key.iCode = EKeyDevice1;
   key.iScanCode = EStdKeyDevice1;
   ws.SimulateKeyEvent(key);
   ws.Close();
//Simulates key press on right menu key, for other keys see e32keys.h 

  return Py_BuildValue("i", 1);
  
}

	/** 
  State of modifier keys and pointing device. Modifier keys are defined in TEventModifier. 
	TUint iModifiers;
	 
  Count of auto repeats generated.
	0 means an event without repeats. 1 or more means "this many auto repeat events". 
	It is normal to ignore this value and treat it as a single event. 
	TInt iRepeats;
	*/

extern "C" PyObject *
keypress_simulate_key(PyObject* /*self*/, PyObject *args)
{
  TInt error;
  int key_code;
  int scan_code;

  RWsSession ws;
  TKeyEvent key;

  if (!PyArg_ParseTuple(args, "ii", &key_code, &scan_code))
    return NULL;
                       
  ws.Connect();
   
   key.iCode = key_code;
   key.iScanCode = scan_code;
   
   Py_BEGIN_ALLOW_THREADS;
	 TRAP(error,ws.SimulateKeyEvent(key);ws.Close(););
	 Py_END_ALLOW_THREADS;
   ws.Close();
    
	 if (error)
	 {
		 return SPyErr_SetFromSymbianOSErr(error);
	 }
   
  return Py_BuildValue("i", 1);
  
}

extern "C" PyObject *
keypress_simulate_key3(PyObject* /*self*/, PyObject *args)
{
  TInt error;
  int key_code;
  int scan_code;
  int modifiers;

  RWsSession ws;
  TKeyEvent key;

  if (!PyArg_ParseTuple(args, "iii", &key_code, &scan_code,&modifiers))
    return NULL;
                       
  ws.Connect();
   
   key.iCode = key_code;
   key.iScanCode = scan_code;
   key.iModifiers = modifiers;
   
   Py_BEGIN_ALLOW_THREADS;
	 TRAP(error,ws.SimulateKeyEvent(key);ws.Close(););
	 Py_END_ALLOW_THREADS;
    
	 if (error)
	 {
		 return SPyErr_SetFromSymbianOSErr(error);
	 }
   
  return Py_BuildValue("i", 1);
  
}

extern "C" {

  static const PyMethodDef keypress_methods[] = {
    {"simulate_keyMenu", (PyCFunction)keypress_simulate_keymenu, METH_NOARGS, NULL},
    {"simulate_key",  (PyCFunction)keypress_simulate_key, METH_VARARGS, NULL },
    {"simulate_key_mod",  (PyCFunction)keypress_simulate_key3, METH_VARARGS, NULL },

    {NULL,              NULL}           /* sentinel */
  };

  DL_EXPORT(void) initkeypress(void)
  {
    PyObject *m;

    m = Py_InitModule("keypress", (PyMethodDef*)keypress_methods);
  }
} /* extern "C" */

GLDEF_C TInt E32Dll(TDllReason)
{
  return KErrNone;
}
