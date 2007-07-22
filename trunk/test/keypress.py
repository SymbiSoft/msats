from key_modifiers import *
from key_codes import *  
import keypress 
import e32
import telephone
import appswitch

class AutoTradeByPhone:
	def presschar(self,char):
		if char=="0":
			keypress.simulate_key(EKey0,EKey0)
		if char=="1":
			keypress.simulate_key(EKey1,EKey1)
		if char=="2":
			keypress.simulate_key(EKey2,EKey2)
		if char=="3":
			keypress.simulate_key(EKey3,EKey3)
		if char=="4":
			keypress.simulate_key(EKey4,EKey4)
		if char=="5":
			keypress.simulate_key(EKey5,EKey5)
		if char=="6":
			keypress.simulate_key(EKey6,EKey6)
		if char=="7":
			keypress.simulate_key(EKey7,EKey7)
		if char=="8":
			keypress.simulate_key(EKey8,EKey8)
		if char=="9":
			keypress.simulate_key(EKey9,EKey9)
		if char=="#":
			keypress.simulate_key(EKeyHash,EKeyHash)
		if char=="*":
			keypress.simulate_key(EKeyStar,EKeyStar)
			
	def switch(self):
		appswitch.switch_to_fg(u"Menu")
		appswitch.switch_to_fg(u"Telephone")

	def pressstr(self,str):
		for i in range(len(str)):
			self.switch()
			self.presschar(str[i])
	
	def dialandsenddtmf(self,str):		
		splitdata=[]
		splitdata=str.split("p")
		sleep = 5
		
		telephone.dial(splitdata[0])
		for i in range(len(splitdata)-1):
			e32.ao_sleep(sleep)
			if splitdata[i+1]=="":
				e32.ao_sleep(sleep)
			else:
				self.pressstr(splitdata[i+1])
		e32.ao_sleep(30)
		telephone.hang_up()
a=AutoTradeByPhone()
a.dialandsenddtmf("2620888p1p1p1")
 
 