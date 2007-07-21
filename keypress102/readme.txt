keypress v1.02
==============
(simulation of key press) originaly developed by group 451 spring 2006 
at Aalborg University and cyke64 from the Pys60 sysinfo template. 
We use the module to simulate hang up on nokia 6600 in silent mode.

License : Apache License 2

Installation :
 - send KEYPRESS.PYD to phone and install as lib
 - send key_modifiers.py to phone and install as lib

Use in python :

from key_modifiers import * 
from key_codes import * 
import keypress 
# Display "a" 
keypress.simulate_key(EKey1,EKey1)  
# Display "1" 
keypress.simulate_key_mod(EKey1,EKey1,EModifierKeypad) 