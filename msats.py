from key_modifiers import *
from key_codes import *
import sys
import time
import random
import e32
import e32db
import appuifw
import urllib
import httplib
import audio
import keypress 
import telephone
import appswitch

def float2str(i):
		i='%s'%(float(i))
		if i[-1]=='0':
			i=i[:-2]
		return i

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
		e32.ao_sleep(sleep)
		for i in range(len(splitdata)-1):
			e32.ao_sleep(sleep)
			if splitdata[i+1]=="":
				e32.ao_sleep(sleep)
			else:
				self.pressstr(splitdata[i+1])
		e32.ao_sleep(15)
		telephone.hang_up()

class MsatsDb:
	def __init__(self, db_name):
		try:
			self.native_db = e32db.Dbms()
			self.native_db.open(db_name)
		except:
			self.native_db.create(db_name)
			self.native_db.open(db_name)
			self.native_db.execute(SettingEntry.sql_create)
			self.native_db.execute(MoneyEntry.sql_create)
			self.native_db.execute(TradeEntry.sql_create)
			self.native_db.execute(StockEntry.sql_create)
			self.native_db.execute(StrategyEntry.sql_create)

	def close(self):
		self.native_db.close()

class Setting:
	def __init__(self, db_name):
		try:
			self.native_db = e32db.Dbms()
			self.native_db.open(db_name)
		except:
			MsatsDb(db_name)
			self.native_db = e32db.Dbms()
			self.native_db.open(db_name)	
	
	def get_all_entries(self):
		dbv = e32db.Db_view()
		dbv.prepare(self.native_db,
					u"SELECT * from setting ORDER BY account DESC")
		dbv.first_line()
		results = []
		for i in range(dbv.count_line()):
			dbv.get_line()
			e = SettingEntry(dbv)
			results.append(e)
			dbv.next_line()
		return results

	def get_number(self):
		dbv = e32db.Db_view()
		dbv.prepare(self.native_db,
					u"SELECT * from setting ORDER BY account DESC")
		return dbv.count_line()
	
	def add(self, e):
		self.native_db.execute(e.sql_add())
		
	def update(self, e):
		self.native_db.execute(e.sql_update())
		
	def delete(self, e):
		self.native_db.execute(e.sql_delete())
		
	def deleteall(self):
		self.native_db.execute((u"DELETE FROM setting"))
		
class SettingEntry:
	sql_create = u"CREATE TABLE setting (account varchar,password varchar)"
	
	def __init__(self, r=None):
		if r:			
			self.account  = r.col(1)
			self.password  = r.col(2)
		else:
			self.account  = u""
			self.password  =u""

	def sql_add(self):
		sql = "INSERT INTO setting (account,password) VALUES ('%s','%s')"%(self.account,self.password)
		return unicode(sql)

	def sql_update(self):
		sql = "update setting set password='%s' where account='%s'"%(self.password,self.account)
		return unicode(sql)
	
	def sql_delete(self):
		sql = "DELETE FROM setting WHERE account='%s'"%\
			  (self.account)
		return unicode(sql)
	
	def get_account(self):
		return self.account	
	
	def get_password(self):
		return self.password

	def get_form(self):
		result = [(u"Account", 'text', self.account),(u"Password", 'text', self.password)]
		return result
		
	def set_from_form(self, form):
		self.account = form[0][2]
		self.password = form[1][2]

class Money:
	def __init__(self, db_name):
		try:
			self.native_db = e32db.Dbms()
			self.native_db.open(db_name)
		except:
			MsatsDb(db_name)
			self.native_db = e32db.Dbms()
			self.native_db.open(db_name)	
	
	def get_all_entries(self):
		dbv = e32db.Db_view()
		dbv.prepare(self.native_db,
					u"SELECT * from money ORDER BY id DESC")
		dbv.first_line()
		results = []
		for i in range(dbv.count_line()):
			dbv.get_line()
			e = MoneyEntry(dbv)
			results.append(e)
			dbv.next_line()
		return results

	def get_max_id(self):
		dbv = e32db.Db_view()
		dbv.prepare(self.native_db,
					u"SELECT id from money ORDER BY id DESC")
		if 0 == dbv.count_line():
			results=0
		else:
			dbv.first_line()
			dbv.get_line()
			results = dbv.col(1)	
		return results

	def get_total(self):
		dbv = e32db.Db_view()
		total=0.0
		dbv.prepare(self.native_db,u"SELECT money from money where type=0")
		if 0 == dbv.count_line():
				total=0.0
		else:
			dbv.first_line()
			for i in range(dbv.count_line()):
				dbv.get_line()
				total=total+float(dbv.col(1))

		dbv.prepare(self.native_db,u"SELECT money from money where type=1")
		if 0 != dbv.count_line():
			dbv.first_line()
			for i in range(dbv.count_line()):
				dbv.get_line()
				total=total-float(dbv.col(1))
		return total
	
	def add(self, e):
		self.native_db.execute(e.sql_add())
		
	def update(self, e):
		self.native_db.execute(e.sql_update())
		
	def delete(self, e):
		self.native_db.execute(e.sql_delete())
		
class MoneyEntry:
	sql_create = u"CREATE TABLE money (id integer,date timestamp,type integer,money float)"
	MoneyType=[u"In",u"Out"]
	
	def __init__(self, r=None):
		if r:			
			self.id  = int(r.col(1))
			self.date  = r.col(2)
			self.type  = int(r.col(3))
			self.money  = float(r.col(4))
		else:
			self.id  = 0
			self.date  =time.time()
			self.type  = 0
			self.money  = 0.0
	
	def sql_add(self):
		sql = "INSERT INTO money (id,date,type,money) VALUES (%d,#%s#,%d,%s)"%(self.id,e32db.format_time(self.date),self.type,float2str(self.money))
		return unicode(sql)

	def sql_update(self):
		sql = "update money set date=#%s#,type=%d,money=%s where id=%d"%(
			e32db.format_time(self.date),self.type,float2str(self.money),self.id)
		return unicode(sql)
	
	def sql_delete(self):
		sql = "DELETE FROM money WHERE id=%d"%\
			  (self.id)
		return unicode(sql)
	
	def get_id(self):
		return self.id	
	
	def get_date(self):
		return self.date
	
	def get_form(self):
		 # Convert Unix timestamp into the form the form accepts.
		(yr, mo, da, h, m, s, wd, jd, ds) =time.localtime(self.date)
		m += 60*h # 60 minutes per hour
		s += 60*m # 60 seconds per minute
		result = [(u"Date", 'date', float(self.date-s))]
		if self.type==None:
			result.append((u"Type", 'combo', (self.MoneyType,0)))
		else:
			result.append((u"Type", 'combo', (self.MoneyType,self.type)))
		result.append((u"Money", 'text', unicode(str(self.money))))
		return result
		
	def set_from_form(self, form):
		self.date  = float(form[0][2])+1
		self.type	 = int(form[1][2][1])
		self.money   = float(form[2][2])

class Trade:
	def __init__(self, db_name):
		try:
			self.native_db = e32db.Dbms()
			self.native_db.open(db_name)
		except:
			MsatsDb(db_name)
			self.native_db = e32db.Dbms()
			self.native_db.open(db_name)	
	
	def get_all_entries(self):
		dbv = e32db.Db_view()
		dbv.prepare(self.native_db,
					u"SELECT * from trade ORDER BY id DESC")
		dbv.first_line()
		results = []
		for i in range(dbv.count_line()):
			dbv.get_line()
			e = TradeEntry(dbv)
			results.append(e)
			dbv.next_line()
		return results

	def get_max_id(self):
		dbv = e32db.Db_view()
		dbv.prepare(self.native_db,
					u"SELECT id from trade ORDER BY id DESC")
		if 0 == dbv.count_line():
			results=0
		else:
			dbv.first_line()
			dbv.get_line()
			results = dbv.col(1)	
		return results

	def get_total(self):
		dbv = e32db.Db_view()
		total=0.0
		dbv.prepare(self.native_db,u"SELECT price,num from trade where type=0")
		if 0 == dbv.count_line():
				total=0.0
		else:
			dbv.first_line()
			for i in range(dbv.count_line()):
				dbv.get_line()
				total=total+float(dbv.col(1))*float(dbv.col(2))

		dbv.prepare(self.native_db,u"SELECT price,num from trade where type=1")
		if 0 != dbv.count_line():
			dbv.first_line()
			for i in range(dbv.count_line()):
				dbv.get_line()
				total=total-float(dbv.col(1))*float(dbv.col(2))
		return total

	def get_numbycode(self,code):
		dbv = e32db.Db_view()
		num=0
		dbv.prepare(self.native_db,u"SELECT num from trade where type=0 and code='%s'"%(code))
		if 0 == dbv.count_line():
				num=0
		else:
			dbv.first_line()
			for i in range(dbv.count_line()):
				dbv.get_line()
				num=num-int(dbv.col(1))

		dbv.prepare(self.native_db,u"SELECT num from trade where type=1 and code='%s'"%(code))
		if 0 != dbv.count_line():
			dbv.first_line()
			for i in range(dbv.count_line()):
				dbv.get_line()
				num=num+int(dbv.col(1))
		return num
	
	def add(self, e):
		self.native_db.execute(e.sql_add())
		
	def update(self, e):
		self.native_db.execute(e.sql_update())
		
	def delete(self, e):
		self.native_db.execute(e.sql_delete())
		
class TradeEntry:
	sql_create = u"CREATE TABLE trade (id integer,date timestamp,type integer,code varchar,price float,num integer)"
	TradeType=[u"Sell",u"Buy"]
	
	def __init__(self, r=None):
		if r:			
			self.id  = int(r.col(1))
			self.date  = r.col(2)
			self.type  = int(r.col(3))
			self.code=r.col(4)
			self.price  = float(r.col(5))
			self.num  = int(r.col(6))
		else:
			self.id  = 0
			self.date  =time.time()
			self.type  = 0
			self.code=u''
			self.price  = 0.0
			self.num  = 0
			
	def sql_add(self):
		sql = "INSERT INTO trade (id,date,type,code,price,num) VALUES (%d,#%s#,%d,'%s',%s,%d)"%(
			self.id,e32db.format_time(self.date),self.type,self.code,float2str(self.price),self.num)
		return unicode(sql)

	def sql_update(self):
		sql = "update trade set date=#%s#,type=%d,code='%s',price=%s,num=%d where id=%d"%(
			e32db.format_time(self.date),self.type,self.code,float2str(self.price),self.num,self.id)
		return unicode(sql)
	
	def sql_delete(self):
		sql = "DELETE FROM trade WHERE id=%d"%\
			  (self.id)
		return unicode(sql)
	
	def get_id(self):
		return self.id	
	
	def get_date(self):
		return self.date
	
	def get_form(self):
		 # Convert Unix timestamp into the form the form accepts.
		(yr, mo, da, h, m, s, wd, jd, ds) =time.localtime(self.date)
		m += 60*h # 60 minutes per hour
		s += 60*m # 60 seconds per minute
		result = [(u"Date", 'date', float(self.date-s))]
		if self.type==None:
			result.append((u"Type", 'combo', (self.TradeType,0)))
		else:
			result.append((u"Type", 'combo', (self.TradeType,self.type)))
		result.append((u"Code", 'text', self.code))
		result.append((u"Price", 'text', unicode(str(self.price))))
		result.append((u"Num", 'number', self.num))
		return result
		
	def set_from_form(self, form):
		self.date  = float(form[0][2])+1
		self.type	 = int(form[1][2][1])
		self.code    =form[2][2]
		self.price   = float(form[3][2])
		self.num    =int(form[4][2])
		
class Stock:
	def __init__(self, db_name):
		try:
			self.native_db = e32db.Dbms()
			self.native_db.open(db_name)
		except:
			MsatsDb(db_name)
			self.native_db = e32db.Dbms()
			self.native_db.open(db_name)	
	
	def get_all_entries(self):
		dbv = e32db.Db_view()
		dbv.prepare(self.native_db,
					u"SELECT * from stock ORDER BY code DESC")
		dbv.first_line()
		results = []
		for i in range(dbv.count_line()):
			dbv.get_line()
			e = StockEntry(dbv)
			results.append(e)
			dbv.next_line()
		return results
	
	def add(self, e):
		self.native_db.execute(e.sql_add())
		
	def update(self, e):
		self.native_db.execute(e.sql_update())
		
	def delete(self, e):
		self.native_db.execute(e.sql_delete())
		
class StockEntry:
	sql_create = u"CREATE TABLE stock (code varchar)"
	
	# Initialize with a row from Sport_diary_db
	def __init__(self, r=None):
		if r:			
			self.code  = r.col(1)
		else:
			self.code  = u""
			
	def sql_add(self):
		sql = "INSERT INTO stock (code) VALUES ('%s')"%(
			self.code)
		return unicode(sql)

	def sql_update(self):
		sql = "update stock set code='%s' where code='%s' "%(
			self.code,self.code)
		return unicode(sql)
	
	
	def sql_delete(self):
		sql = "DELETE FROM stock WHERE code='%s'"%\
			  (self.code)
		return unicode(sql)
		
	def get_code(self):
		return self.code
	
	def get_form(self):
		result = [(u'Code', 'text', self.code)]
		return result
		
	def set_from_form(self, form):
		self.code = form[0][2]

class Strategy:
	def __init__(self, db_name):
		try:
			self.native_db = e32db.Dbms()
			self.native_db.open(db_name)
		except:
			MsatsDb(db_name)
			self.native_db = e32db.Dbms()
			self.native_db.open(db_name)	
	
	def get_all_entries(self):
		dbv = e32db.Db_view()
		dbv.prepare(self.native_db,u"SELECT * from strategy ORDER BY id DESC")
		dbv.first_line()
		results = []
		for i in range(dbv.count_line()):
			dbv.get_line()
			e = StrategyEntry(dbv)
			results.append(e)
			dbv.next_line()
		return results

	def get_all_codes(self):
		dbv = e32db.Db_view()
		dbv.prepare(self.native_db,u"SELECT * from strategy ORDER BY id DESC")
		dbv.first_line()
		results = []
		for i in range(dbv.count_line()):
			distinct=0
			dbv.get_line()
			e = StrategyEntry(dbv)
			for code in results:
				if code==e.code:
					distinct=1
					break
			if distinct==0:
				results.append(e.code)
			dbv.next_line()
		return results

	def get_all_enabledentriesbycode(self,code):
		dbv = e32db.Db_view()
		dbv.prepare(self.native_db,u"SELECT * from strategy where code='%s' and enableflag=1 ORDER BY id DESC"%(code))
		dbv.first_line()
		results = []
		for i in range(dbv.count_line()):
			dbv.get_line()
			e = StrategyEntry(dbv)
			results.append(e)
			dbv.next_line()
		return results

	def get_all_enabledentries(self):
		dbv = e32db.Db_view()
		dbv.prepare(self.native_db,u"SELECT * from strategy where enableflag=1")
		dbv.first_line()
		results = []
		for i in range(dbv.count_line()):
			dbv.get_line()
			e = StrategyEntry(dbv)
			results.append(e)
			dbv.next_line()
		return results	
		
	def get_max_id(self):
		dbv = e32db.Db_view()
		dbv.prepare(self.native_db,
					u"SELECT id from strategy ORDER BY id DESC")
		if 0 == dbv.count_line():
			results=0
		else:
			dbv.first_line()
			dbv.get_line()
			results = dbv.col(1)	
		return results
		
	def add(self, e):
		self.native_db.execute(e.sql_add())

	def update(self, e):
		self.native_db.execute(e.sql_update())	

	def delete(self, e):
		self.native_db.execute(e.sql_delete())
	
	def disable(self, e):
		self.native_db.execute(e.sql_disable())
		
class StrategyEntry:
	sql_create = u"CREATE TABLE strategy (id integer,code varchar,type integer,startprice float,uprate float,downrate float,enableflag integer)"
	StrategyType=[u"Sell after up start price",u"Buy after down start price",u"Sell after up previous day price",u"Buy after down previous day price"]
	
	def __init__(self, r=None):
		if r:			
			self.id  = r.col(1)
			self.code  = r.col(2)
			self.type  = int(r.col(3))
			self.startprice  = float(r.col(4))
			self.uprate  = float(r.col(5))
			self.downrate  = float(r.col(6))
			self.enableflag  = int(r.col(7))
		else:
			self.id  = 0
			self.code  =u''
			self.type  = 1
			self.startprice  = 0.0
			self.uprate  = 0.0
			self.downrate  = 0.0
			self.enableflag  = 0
			
	def sql_add(self):
		sql = "INSERT INTO strategy (id,code,type,startprice,uprate,downrate,enableflag) VALUES (%d,'%s',%d,%s,%s,%s,%d)"%(
			self.id,self.code,self.type,float2str(self.startprice),float2str(self.uprate),float2str(self.downrate),self.enableflag)
		return unicode(sql)

	def sql_update(self):
		sql = "update strategy set code='%s',type=%d,startprice=%s,uprate=%s,downrate=%s,enableflag=%d where id=%d"%(
			self.code,self.type,float2str(self.startprice),float2str(self.uprate),float2str(self.downrate),self.enableflag,self.id)
		return unicode(sql)
	
	def sql_delete(self):
		sql = "DELETE FROM strategy WHERE id=%d"%\
			  (self.id)
		return unicode(sql)
	
	def sql_disable(self):
		sql = "update strategy set enableflag=0 WHERE id=%d"%\
			  (self.id)
		return unicode(sql)
		
	def get_id(self):
		return self.id	
	
	def get_code(self):
		return self.code
	
	def get_form(self):
		result = [(u"Code", 'text', self.code)]
		if self.type==None:
			result.append((u"Type", 'combo', (self.StrategyType,0)))
		else:
			result.append((u"Type", 'combo', (self.StrategyType,self.type)))
		result.append((u"StartPrice", 'text', unicode(str(self.startprice))))
		result.append((u"UpRate", 'text', unicode(str(self.uprate))))
		result.append((u"DownRate", 'text', unicode(str(self.downrate))))
		result.append((u"EnableFlag", 'number', self.enableflag))
		return result
		
	def set_from_form(self, form):
		self.code  = form[0][2]
		self.type	 = form[1][2][1]
		self.startprice   = float(form[2][2])
		self.uprate   = float(form[3][2])
		self.downrate   = float(form[4][2])
		self.enableflag   = int(form[5][2])
		
class MsatsApp:
	LogText=appuifw.Text(u'')
	AdviceText=appuifw.Text(u'')
	MoneyText=appuifw.Text(u'')
	timer = e32.Ao_timer() 
	
	def __init__(self):
		self.lock = e32.Ao_lock()
		self.app_lock = e32.Ao_lock()
		self.exit_flag = False
		appuifw.app.exit_key_handler = self.abort
		self.entry_list = []

		self.menu_money = (u"Money", self.handle_moneyoverview)
		self.menu_moneyadd=(u"Add",self.handle_moneyadd)
		self.menu_moneyedit=(u"Edit",self.handle_moneyedit)
		self.menu_moneydelete=(u"Delete",self.handle_moneydelete)
		self.menu_moneydetail=(u"Detail",self.handle_view_entry)
		self.menu_moneyreturn=(u"Return",self.locksignal)
		
		self.menu_trade = (u"Trade", self.handle_tradeoverview)
		self.menu_tradeadd=(u"Add",self.handle_tradeadd)
		self.menu_tradeedit=(u"Edit",self.handle_tradeedit)
		self.menu_tradedelete=(u"Delete",self.handle_tradedelete)
		self.menu_tradedetail=(u"Detail",self.handle_view_entry)
		self.menu_tradereturn=(u"Return",self.locksignal)
		
		self.menu_stock = (u"Stock", self.handle_stockoverview)
		self.menu_stockadd=(u"Add",self.handle_stockadd)
		self.menu_stockedit=(u"Edit",self.handle_stockedit)
		self.menu_stockdelete=(u"Delete",self.handle_stockdelete)
		self.menu_stockdetail=(u"Detail",self.handle_view_entry)
		self.menu_stockreturn=(u"Return",self.locksignal)
		
		self.menu_strategy = (u"Strategy", self.handle_strategyoverview)
		self.menu_strategyadd=(u"Add",self.handle_strategyadd)
		self.menu_strategyedit=(u"Edit",self.handle_strategyedit)
		self.menu_strategydelete=(u"Delete",self.handle_strategydelete)
		self.menu_strategydetail=(u"Detail",self.handle_view_entry)
		self.menu_strategyreturn=(u"Return",self.locksignal)
		
		self.menu_run = (u"Run", ((u"Start",self.handle_runstart),(u"Stop",self.handle_runstop)))
		self.menu_setting = (u"Setting",self.handle_setting)
		self.AutoTradeByPhone=AutoTradeByPhone()
		appuifw.app.menu = []

	def initialize_db(self, db_name):
		self.msats = MsatsDb(db_name)
		self.Setting = Setting(db_name)
		self.Money = Money(db_name)
		self.Trade = Trade(db_name)
		self.Stock = Stock(db_name)
		self.Strategy = Strategy(db_name)
		
	def run(self):
		while not self.exit_flag:
			self.show_main_view()
			self.lock.wait()
		self.close()

	def close(self):
		appuifw.app.menu = []
		appuifw.app.body = None
		appuifw.app.exit_key_handler = None
		self.msats.close()

	def abort(self):
		if appuifw.query(u"Are you sure to quit?",'query'):
			self.exit_flag = True
			self.lock.signal()
			self.app_lock.signal()
			
	def handle_tab(self,index):
		global lb
		if index == 0:
			self.log() 
		if index == 1:
			self.advice()
		if index == 2:
			self.money()

	def log(self):
		appuifw.app.body=self.LogText

	def advice(self):
		appuifw.app.body=self.AdviceText

	def money(self):
		appuifw.app.body=self.MoneyText
		
	def show_main_view(self):
		appuifw.app.set_tabs([u"Log",u"Advice",u"Money"],self.handle_tab)
		appuifw.app.body=self.LogText
		self.show_menu()  
		self.app_lock.wait()


	def show_menu(self):	
		appuifw.app.menu = [self.menu_money,self.menu_trade,self.menu_stock,self.menu_strategy,self.menu_run,self.menu_setting]

	def show_moneymenu(self):	
		appuifw.app.menu = [self.menu_moneyadd,self.menu_moneyedit,self.menu_moneydelete,self.menu_moneydetail,self.menu_moneyreturn]
		
	def show_trademenu(self):	
		appuifw.app.menu = [self.menu_tradeadd,self.menu_tradeedit,self.menu_tradedelete,self.menu_tradedetail,self.menu_tradereturn]

	def show_stockmenu(self):	
		appuifw.app.menu = [self.menu_stockadd,self.menu_stockedit,self.menu_stockdelete,self.menu_stockdetail,self.menu_stockreturn]
		
	def show_strategymenu(self):	
		appuifw.app.menu = [self.menu_strategyadd,self.menu_strategyedit,self.menu_strategydelete,self.menu_strategydetail,self.menu_strategyreturn]

	def textinfo(self,textobj,color,info):
		textobj.color=color
		textobj.add(info+u'\n')	
	
	def handle_view_entry(self):
		if self.entry_list:
			index = self.main_view.current()
			self.show_entry(self.entry_list[index])
		
	def show_entry(self, entry):
		data = entry.get_form()
		flags = appuifw.FFormViewModeOnly
		f = appuifw.Form(data, flags)
		f.execute()

	def locksignal(self):
		self.lock.signal()
		
	def handle_moneyadd(self):
		new_entry = MoneyEntry()
		data = new_entry.get_form()
		flags = appuifw.FFormEditModeOnly+appuifw.FFormDoubleSpaced
		f = appuifw.Form(data, flags)
		f.execute()
		new_entry.set_from_form(f)
		new_entry.id=self.newmoneyid()
		self.Money.add(new_entry)
		self.handle_moneyoverview()
		
	def handle_moneyedit(self):
		if self.entry_list:
			index = self.main_view.current()
			data = self.entry_list[index].get_form()
		
			flags = appuifw.FFormEditModeOnly+appuifw.FFormDoubleSpaced
			f = appuifw.Form(data, flags)
			f.execute()
			new_entry = MoneyEntry()
			new_entry.id=int(self.entry_list[index].id)
			new_entry.set_from_form(f)
			self.Money.update(new_entry)
			self.handle_moneyoverview()			
		
	def handle_moneydelete(self):
		if self.entry_list:
			index = self.main_view.current()
		if appuifw.query(u"Delete entry?", 'query'):
			self.Money.delete(self.entry_list[index])
			self.handle_moneyoverview()	
		
	def handle_moneyoverview(self):
		self.main_view = appuifw.Listbox([(u"Loading...", u"")],self.handle_view_entry)
		appuifw.app.body = self.main_view
		self.entry_list = self.Money.get_all_entries()
		if not self.entry_list:
			content = [(u"(Empty)", u"")]
		else:
			content = [(unicode(str(item.id)),unicode(str(item.money))) for item in self.entry_list]
		self.main_view.set_list(content)
		self.show_moneymenu()

	def handle_tradeadd(self):
		new_entry = TradeEntry()
		data = new_entry.get_form()
		flags = appuifw.FFormEditModeOnly+appuifw.FFormDoubleSpaced
		f = appuifw.Form(data, flags)
		f.execute()
		new_entry.set_from_form(f)
		new_entry.id=self.newtradeid()
		self.Trade.add(new_entry)
		self.handle_tradeoverview()
		
	def handle_tradeedit(self):
		if self.entry_list:
			index = self.main_view.current()
			data = self.entry_list[index].get_form()
		
			flags = appuifw.FFormEditModeOnly+appuifw.FFormDoubleSpaced
			f = appuifw.Form(data, flags)
			f.execute()
			new_entry = TradeEntry()
			new_entry.id=self.entry_list[index].id
			new_entry.set_from_form(f)
			self.Trade.update(new_entry)
			self.handle_tradeoverview()			
		
	def handle_tradedelete(self):
		if self.entry_list:
			index = self.main_view.current()
		if appuifw.query(u"Delete entry?", 'query'):
			self.Trade.delete(self.entry_list[index])
			self.handle_tradeoverview()	
		
	def handle_tradeoverview(self):
		self.main_view = appuifw.Listbox([(u"Loading...", u"")],self.handle_view_entry)
		appuifw.app.body = self.main_view
		self.entry_list = self.Trade.get_all_entries()
		if not self.entry_list:
			content = [(u"(Empty)", u"")]
		else:
			content = [(unicode(str(item.id)),item.code) for item in self.entry_list]
		self.main_view.set_list(content)
		self.show_trademenu()
					   
	def handle_stockadd(self):
		new_entry = StockEntry()
		data = new_entry.get_form()
		flags = appuifw.FFormEditModeOnly+appuifw.FFormDoubleSpaced
		f = appuifw.Form(data, flags)
		f.execute()
		new_entry.set_from_form(f)
		self.Stock.add(new_entry)
		self.handle_stockoverview()
		
	def handle_stockedit(self):
		if self.entry_list:
			index = self.main_view.current()
			data = self.entry_list[index].get_form()
		
			flags = appuifw.FFormEditModeOnly+appuifw.FFormDoubleSpaced
			f = appuifw.Form(data, flags)
			f.execute()
			new_entry = StockEntry()
			new_entry.set_from_form(f)
			self.Stock.update(new_entry)
			self.handle_stockoverview()
			
	def handle_stockdelete(self):
		if self.entry_list:
			index = self.main_view.current()
		if appuifw.query(u"Delete entry?", 'query'):
			self.Stock.delete(self.entry_list[index])
			self.handle_stockoverview()
				
	def handle_stockoverview(self):
		self.main_view = appuifw.Listbox([(u"Loading...", u"")], self.handle_view_entry)
		appuifw.app.body = self.main_view
		self.entry_list = self.Stock.get_all_entries()
		if not self.entry_list:
			content = [(u"(Empty)", u"")]
		else:
			content = [(u'',item.code) for item in self.entry_list]
		self.main_view.set_list(content)
		self.show_stockmenu()
	
	def handle_strategyadd(self):
		new_entry = StrategyEntry()
		data = new_entry.get_form()
		flags = appuifw.FFormEditModeOnly+appuifw.FFormDoubleSpaced
		f = appuifw.Form(data, flags)
		f.execute()
		new_entry.set_from_form(f)
		new_entry.id=self.newstrategyid()
		self.Strategy.add(new_entry)
		self.handle_strategyoverview()
		
	def handle_strategyedit(self):
		if self.entry_list:
			index = self.main_view.current()
			data = self.entry_list[index].get_form()
		
			flags = appuifw.FFormEditModeOnly+appuifw.FFormDoubleSpaced
			f = appuifw.Form(data, flags)
			f.execute()
			new_entry = StrategyEntry()
			new_entry.id=self.entry_list[index].id
			new_entry.set_from_form(f)
			self.Strategy.update(new_entry)
			self.handle_strategyoverview()			
		
	def handle_strategydelete(self):
		if self.entry_list:
			index = self.main_view.current()
		if appuifw.query(u"Delete entry?", 'query'):
			self.Strategy.delete(self.entry_list[index])
			self.handle_strategyoverview()	
		
	def handle_strategyoverview(self):
		self.main_view = appuifw.Listbox([(u"Loading...", u"")],self.handle_view_entry)
		appuifw.app.body = self.main_view
		self.entry_list = self.Strategy.get_all_entries()
		if not self.entry_list:
			content = [(u"(Empty)", u"")]
		else:
			content = [(unicode(str(item.id)),item.code) for item in self.entry_list]
		self.main_view.set_list(content)
		self.show_strategymenu()

	def gettotalmoneycanuse(self):
		return self.Money.get_total()+self.Trade.get_total()
	
	def mynowtime(self):
		return time.ctime()

	def maketrade(self,flag,code,nowprice):

		newentry=SettingEntry()
		if self.Setting.get_number()==0:
			self.textinfo(self.LogText,0x004000,"account and password not defined")
			return
		else:
			entrylist=self.Setting.get_all_entries()
			newentry=entrylist[0]
			account=newentry.account
			password=newentry.password
			
		if flag==0:
			num=int(self.Trade.get_numbycode(code)/100)
			if num>0:
				randnum=random.randint(1,num)
				self.textinfo(self.AdviceText,0x004000,"    you can sell %d max,randnum=%d"%(num,randnum))
				tradestr="2620888p1p1p1p%s#p%s#p2p2p%s#p%.2f#p%d00#p8"%(account,password,code,nowprice,randnum)
				tradestr=tradestr.replace(".","*")
				self.textinfo(self.AdviceText,0x004000,"    the tradestr is %s"%(tradestr))
			else:
				self.textinfo(self.AdviceText,0x004000,"    you have no stock to sell!")
				return	
		if flag==1:
			totalmoneycanuse=self.gettotalmoneycanuse()
			if totalmoneycanuse>100*nowprice:
				num=int(totalmoneycanuse/(100*nowprice))
				randnum=random.randint(1,num)
				self.textinfo(self.AdviceText,0x004000,"    you can buy %d max,randnum=%d"%(num,randnum))
				tradestr="2620888p1p1p1p%s#p%s#p2p1p%s#p%.2f#p%d00#p8"%(account,password,code,nowprice,randnum)
				tradestr=tradestr.replace(".","*")
				self.textinfo(self.AdviceText,0x004000,"    the tradestr is %s"%(tradestr))
			else:
				self.textinfo(self.AdviceText,0x004000,"    you have no money to buy!")
				return
		self.AutoTradeByPhone.dialandsenddtmf(tradestr)

	def process(self,strategy,nowprice,yesterdayprice):
		#yesterday price
		startprice=float(strategy.startprice)
		uprate=float(strategy.uprate)
		downrate=float(strategy.downrate)
		self.textinfo(self.LogText,0x004000,"    now price:%s;yesterday price:%s"%(float2str(nowprice),float2str(yesterdayprice)))
		if int(strategy.type)>1:
			baseprice=yesterdayprice
		#start price	
		else:
			baseprice=startprice
		#sell	
		if int(strategy.type)%2==0:
			tradeprice=baseprice*(1+uprate)
			if nowprice>=tradeprice:
				self.textinfo(self.AdviceText,0x004000,self.mynowtime())
				self.textinfo(self.AdviceText,0x004000,"    you can sell %s in price %s"%(strategy.code,float2str(nowprice)))
				self.maketrade(0,strategy.code,nowprice)
				self.playsound()
				self.Strategy.disable(strategy)
		#buy	
		else:
			tradeprice=baseprice*(1-downrate)
			if nowprice<=tradeprice:
				self.textinfo(self.AdviceText,0x004000,self.mynowtime())
				self.textinfo(self.AdviceText,0x004000,"    you can buy %s in price %s"%(strategy.code,float2str(nowprice)))
				self.maketrade(1,strategy.code,nowprice)
				self.playsound()
				self.Strategy.disable(strategy)

	def do_onetime(self):
		codelist=self.Strategy.get_all_codes()
		for code in codelist:
			self.textinfo(self.LogText,0x004000,code)
			self.textinfo(self.LogText,0x004000,"Getting")
			if self.stopflag==1:
				return
			try:
				data=self.getstock(code)
			except:
				self.textinfo(self.LogText,0x004000,"get the info error!")
				continue

			self.textinfo(self.LogText,0x004000,data)
			if data!="error":
				try:
					yesterdayprice=float(self.getdataindex(data,1))
					nowprice=float(self.getdataindex(data,0))
				except:
					self.textinfo(self.LogText,0x004000,"the info is not complete")
					continue

				stragelist=self.Strategy.get_all_enabledentriesbycode(code)
				for j in stragelist:		
					self.process(j,nowprice,yesterdayprice)

	def handle_runstart(self):
		self.textinfo(self.LogText,0x004000,"start...")
		
		self.stopflag=0

		trademode=1
		if not appuifw.query(u"Only get trade data on trade time?",'query'):
			trademode=0
		
		while self.stopflag!=1:
			self.textinfo(self.LogText,0x004000,self.mynowtime())
			if trademode==1:
				timepurple=time.localtime()
				if (timepurple.tm_hour==9 and timepurple.tm_min>=30) or (timepurple.tm_hour==10) or (timepurple.tm_hour==11 and timepurple.tm_min<=30) or (timepurple.tm_hour==13) or (timepurple.tm_hour==14):
					self.do_onetime()
				else:
					self.textinfo(self.LogText,0x004000,"now is not trade time,do nothing")
			else:
				self.do_onetime()
				
			for j in range(30):
				if self.stopflag==1:
					break
				else:
					self.LogText.color=0x004000
					self.LogText.add(u'.')
					self.timer.after(1)  # sleep 30 sec
			self.LogText.add(u'\n')
			
			if self.stopflag==1:
				break
		self.textinfo(self.LogText,0x004000,"stopped")

	def handle_runstop(self):
		self.stopflag=1

	def handle_setting(self):
		newentry=SettingEntry()
		if self.Setting.get_number()==0:
			newentry.account=u""
			newentry.password=u""
		else:
			entrylist=self.Setting.get_all_entries()
			newentry=entrylist[0]
			
		data = newentry.get_form()
		
		flags = appuifw.FFormEditModeOnly+appuifw.FFormDoubleSpaced
		f = appuifw.Form(data, flags)
		f.execute()
		new_entry = SettingEntry()
		new_entry.set_from_form(f)
		self.Setting.deleteall()
		self.Setting.add(new_entry)			
		
	def newmoneyid(self):
		id=self.Money.get_max_id()
		return id+1

	def newtradeid(self):
		id=self.Trade.get_max_id()
		return id+1
	
	def newstrategyid(self):
		id=self.Strategy.get_max_id()
		return id+1
	
	def newstrategyid(self):
		id=self.Strategy.get_max_id()
		return id+1
		
	def playsound(self):
		audio.say("New message!")
		
	def getstock(self,code):
		#if this code not run,maybe the next open code can't run correctly! 
		test1 = "000001"
		params = urllib.urlencode({'code': test1})
		headers = {"Content-type": "application/x-www-form-urlencoded","Accept": "text/plain","Host":"www.jili8.com","X-Online-Host":"www.jili8.com"}
		conn = httplib.HTTPConnection("10.0.0.172")
		conn.request("POST", "/php/getstock.php", params, headers)
		response = conn.getresponse()

		url='http://www.jili8.com/php/getstock.php?code='+code

		proxies={'http':'http://10.0.0.172:80'} 
		data=urllib.FancyURLopener(proxies).open(url).read() 
		try:
			udata=data.decode("utf8")
			return udata
		except:
			return u"error"

	def getdataindex(self,udata,index):
		usplitdata=[]
		usplitdata=udata.split(u"|")
		return usplitdata[index]
		
def main():
	app = MsatsApp()
	app.initialize_db(u"e:\\msats.db")
	app.run()

if __name__ == '__main__':
	old_title = appuifw.app.title
	try:
		appuifw.app.title = u"Mobile Stock Auto Trade System"
		e32.ao_yield()
		main()
	finally:
		appuifw.app.title = old_title