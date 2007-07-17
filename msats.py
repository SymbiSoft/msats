import time

import e32
import e32db
import appuifw
import urllib
import httplib
import audio

class MsatsDb:
	def __init__(self, db_name):
		try:
			self.native_db = e32db.Dbms()
			self.native_db.open(db_name)
		except:
			self.native_db.create(db_name)
			self.native_db.open(db_name)
			self.native_db.execute(StockEntry.sql_create)
			self.native_db.execute(StrategyEntry.sql_create)

	def close(self):
		self.native_db.close()

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
		sql = "INSERT INTO strategy (id,code,type,startprice,uprate,downrate,enableflag) VALUES (%d,'%s',%d,%f,%f,%f,%d)"%(
			self.id,self.code,self.type,self.startprice,self.uprate,self.downrate,self.enableflag)
		return unicode(sql)

	def sql_update(self):
		sql = "update strategy set code='%s',type=%d,startprice=%f,uprate=%f,downrate=%f,enableflag=%d where id=%d "%(
			self.code,self.type,self.startprice,self.uprate,self.downrate,self.enableflag,self.id)
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
	AlertText=appuifw.Text(u'')
	MoneyText=appuifw.Text(u'')
	timer = e32.Ao_timer() 
	
	def __init__(self):
		self.lock = e32.Ao_lock()
		self.exit_flag = False
		appuifw.app.exit_key_handler = self.abort
		self.entry_list = []
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
		appuifw.app.menu = []

	def initialize_db(self, db_name):
		self.msats = MsatsDb(db_name)
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

	def handle_tab(self,index):
		global lb
		if index == 0:
			self.log() 
		if index == 1:
			self.alert()
		if index == 2:
			self.money()

	def log(self):
		appuifw.app.body=self.LogText

	def alert(self):
		appuifw.app.body=self.AlertText

	def money(self):
		appuifw.app.body=self.MoneyText
		
	def show_main_view(self):
		appuifw.app.set_tabs([u"Log",u"Alert",u"Money"],self.handle_tab)
		appuifw.app.body=self.LogText
		self.show_menu()  
	
	def show_menu(self):	
		appuifw.app.menu = [self.menu_stock,self.menu_strategy,self.menu_run]

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

	
	def handle_runstart(self):
		self.textinfo(self.LogText,0x004000,"start...")
		self.stopflag=0
		while not self.stopflag:
			stragelist=self.Strategy.get_all_enabledentries()
			self.textinfo(self.LogText,0x004000,time.ctime())
			for j in stragelist:
				self.textinfo(self.LogText,0x004000,j.code)
				
				try:
					data=self.getstock(j.code)
				except:
					self.textinfo(self.LogText,0x004000,"get the info error!")
					continue

				self.textinfo(self.LogText,0x004000,data)
				if data!="error":
					try:
						yesterdayprice=float(self.getdataindex(data,3))
						nowprice=float(self.getdataindex(data,6))
					except:
						self.textinfo(self.LogText,0x004000,"the info is not complete")
						continue
						
					startprice=float(j.startprice)
					uprate=float(j.uprate)
					downrate=float(j.uprate)	
					self.textinfo(self.LogText,0x004000,"    now price:%f;yesterday price:%f"%(nowprice,yesterdayprice))
					if int(j.type)==0:
						sellprice=startprice*(1+uprate)
						self.textinfo(self.LogText,0x004000,"    you want to sell it after the start price:%f*(1+%f)=%f"%(startprice,uprate,sellprice))
						if nowprice>=sellprice:
							self.textinfo(self.LogText,0x004000,"    you can sell it now")
							self.textinfo(self.AlertText,0x004000,time.ctime())
							self.textinfo(self.AlertText,0x004000,"    you can sell %s in price %f"%(j.code,nowprice))
							self.playsound()
							self.Strategy.disable(j)
					if int(j.type)==1:
						buyprice=startprice*(1-downrate)
						self.textinfo(self.LogText,0x004000,"    you want to buy it after the start price:%f*(1-%f)=%f"%(startprice,downrate,buyprice))
						if nowprice<=buyprice:
							self.textinfo(self.LogText,0x004000,"    you can buy it now")
							self.textinfo(self.AlertText,0x004000,time.ctime())
							self.textinfo(self.AlertText,0x004000,"    you can buy %s in price %f"%(j.code,nowprice))
							self.playsound()
							self.Strategy.disable(j)	
					if int(j.type)==2:
						sellprice=yesterdayprice*(1+uprate)
						self.textinfo(self.LogText,0x004000,"    you want to sell it after the yesterday price:%f*(1+%f)=%f"%(yesterdayprice,uprate,sellprice))
						if nowprice>=sellprice:
							self.textinfo(self.LogText,0x004000,"    you can sell it now")
							self.textinfo(self.AlertText,0x004000,time.ctime())
							self.textinfo(self.AlertText,0x004000,"    you can sell %s in price %f"%(j.code,nowprice))
							self.playsound()
							self.Strategy.disable(j)	
					if int(j.type)==3:
						buyprice=yesterdayprice*(1-downrate)
						self.textinfo(self.LogText,0x004000,"    you want to buy it after the yesterday price:%f*(1-%f)=%f"%(yesterdayprice,downrate,buyprice))
						if nowprice<=buyprice:
							self.textinfo(self.LogText,0x004000,"    you can buy it now")
							self.textinfo(self.AlertText,0x004000,time.ctime())
							self.textinfo(self.AlertText,0x004000,"    you can buy %s in price %f"%(j.code,nowprice))
							self.playsound()	
							self.Strategy.disable(j)				
			self.timer.after(30)  # sleep 30 sec

	def handle_runstop(self):
		self.timer.cancel()
		self.stopflag=1
				
	def newstrategyid(self):
		id=self.Strategy.get_max_id()
		return id+1
		
	def playsound(self):
		audio.say("Liberty, love!These two I need. For my love I will sacrifice life, for liberty I will sacrifice my love")
		
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