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
		sql = "INSERT INTO stock (code) VALUES (%s)"%(
			self.code)
		return unicode(sql)
	
	def sql_delete(self):
		sql = "DELETE FROM stock WHERE code=%s"%\
			  (self.code)
		return unicode(sql)
		
	def get_code(self):
		return self.code
	
	def get_form(self):
		result = [(u"Code", 'text', self.code))
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
		dbv.prepare(self.native_db,
					u"SELECT * from strategy ORDER BY id DESC")
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
		dbv.prepare(self.native_db,
					u"SELECT * from strategy ORDER BY id DESC where enableflag=1")
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
			self.type  = r.col(3)
			self.startprice  = r.col(4)
			self.uprate  = r.col(5)
			self.downrate  = r.col(6)
			self.enableflag  = r.col(7)
		else:
			self.id  = 0
			self.code  =u''
			self.type  = 1
			self.startprice  = 0.0
			self.uprate  = 0.0
			self.downrate  = 0.0
			self.enableflag  = 0
			
	def sql_add(self):
		sql = "INSERT INTO strategy (id,code,type,startprice,uprate,downrate,enableflag) VALUES (%d,%s,%d,%d,%d,%d,%d)"%(
			self.id,self.code,self.type,self.startprice,self.uprate,sele.downrate)
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
		result = [(u"Code", 'Text', int(self.code))]
		if self.type==None:
			result.append((u"Type", 'combo', (self.StrategyType,0)))
		else:
			result.append((u"Type", 'combo', (self.StrategyType,self.type)))
		result.append((u"StartPrice", 'number', float(self.startprice)))
		result.append((u"UpRate", 'number', float(self.uprate)))
		result.append((u"DownRate", 'number', float(self.downrate)))
		result.append((u"EnableFlag", 'number', integer(self.enableflag)))
		return result
		
	def set_from_form(self, form):
		self.code  = form[0][2]
		self.type	 = form[1][2][1]
		self.startprice   = float(form[2][2])
		self.uprate   = float(form[3][2])
		self.downrate   = float(form[4][2])
		
class MsatsApp:
	LogText=appuifw.Text(u'')
	
	def __init__(self):
		self.lock = e32.Ao_lock()
		self.exit_flag = False
		appuifw.app.exit_key_handler = self.abort
		self.entry_list = []
		self.menu_stockmanage = (u"Stock", ((u"Add",handle_stockadd),(u"Delete",handle_stockdelete),(u"Overview",handle_stockoverview)))
		self.menu_strategy = (u"Strategy", ((u"Add",handle_strategyadd),(u"Delete",handle_strategydelete),(u"Overview",handle_strategyoverview)))
		self.menu_run = (u"Run", ((u"Start",handle_runstart),(u"Stop",handle_runstop)))
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

	def show_main_view(self):
		appuifw.app.body=self.LogText
		self.show_menu()  
	
	def show_menu(self):	
		appuifw.app.menu = [self.menu_stockmanage,
								self.menu_strategy,
								self.menu_persondie,
								self.menu_run]

	def textinfo(self,textobj,color,info):
		textobj.color=color
		textobj.add(info+u'\n')	
	
	def handle_view_entry(self):
		if self.entry_list:
			index = self.main_view.current()
			self.show_entry(self.entry_list[index])
		self.lock.signal()
   
	def show_entry(self, entry):
  	data = entry.get_form()
    flags = appuifw.FFormViewModeOnly
    f = appuifw.Form(data, flags)
		f.execute()
	
	def handle_stockadd(self):
		new_entry = StockEntry()
		data = new_entry.get_form()
		flags = appuifw.FFormEditModeOnly+appuifw.FFormDoubleSpaced
		f = appuifw.Form(data, flags)
		f.execute()
		new_entry.set_from_form(f)
		self.Stock.add(new_entry)
		
	def handle_stockdelete(self):
		code=appuifw.query(u"Stock code",'text')
		if code==None:
			return
		new_entry = StokckEntry()
		new_entry.code=code
		this.Stock.delete(new_entry)	
				
	def handle_stockoverview(self):
		self.main_view = appuifw.Listbox([(u"Loading...", u"")], 
                                         self.handle_view_entry)
    appuifw.app.body = self.main_view
    self.entry_list = self.Stock.get_all_entries()
		if not self.entry_list:
			content = [(u"(Empty)", u"")]
		else:
			content = [u'',item.code) for item in self.entry_list]
		self.main_view.set_list(content)
	
	def handle_strategyadd(self):
		new_entry = StrategyEntry()
		data = new_entry.get_form()
		flags = appuifw.FFormEditModeOnly+appuifw.FFormDoubleSpaced
		f = appuifw.Form(data, flags)
		f.execute()
		new_entry.set_from_form(f)
		new_entry.id=self.newstrategyid()
		self.Strategy.add(new_entry)
		
	def handle_strategydelete(self):
		id=appuifw.query(u"Strategy id",'number')
		if id==None:
			return
		new_entry = Strategy()
		new_entry.id=id
		this.Strategy.delete(new_entry)
	
	def handle_strategyoverview(self):
		self.main_view = appuifw.Listbox([(u"Loading...", u"")], 
                                         self.handle_view_entry)
    appuifw.app.body = self.main_view
    self.entry_list = self.Strategy.get_all_entries()
		if not self.entry_list:
			content = [(u"(Empty)", u"")]
		else:
			content = [item.id,item.code) for item in self.entry_list]
		self.main_view.set_list(content)

	
	def handle_runstart(self):
		self.textinfo(self.TextLog,0x004000,"start...")
		self.stopflag=0
		while not self.stopflag:
			stragelist=self.Strategy.get_all_enabledentries()
			for j in stragelist:
				self.textinfo(self.TextLog,0x004000,j.code)
				data=getstock(j.code)
				if data!="error":
					yesterdayprice=float(getdataindex(data,3))
					nowprice=float(getdataindex(data,6))
					startprice=float(j.startprice)
					uprate=float(j.uprate)
					downrate=float(j.uprate)	
					self.textinfo(self.TextLog,0x004000,"    now price:%d;yesterday price:%d"%(nowprice,yesterdayprice))
					if integer(j.type)==1:
						sellprice=startprice*(1+uprate)
						self.textinfo(self.TextLog,0x004000,"    you want to sell it after the start price:%d*(1+%d)=%d"%(startprice,uprate,sellprice))
						if nowprice>=sellprice:
							self.textinfo(self.TextLog,0x004000,"    you can sell it now")
							self.playsound("E:\\sound1.mid")
							self.Strategy.disable(j)
					if integer(j.type)==2:
						buyprice=startprice*(1-downrate)
						self.textinfo(self.TextLog,0x004000,"    you want to buy it after the start price:%d*(1-%d)=%d"%(startprice,downrate,buyprice))
						if nowprice<=buyprice:
							self.textinfo(self.TextLog,0x004000,"    you can buy it now")
							self.playsound("E:\\sound1.mid")
							self.Strategy.disable(j)	
					if integer(j.type)==3:
						sellprice=yesterdayprice*(1+uprate)
						self.textinfo(self.TextLog,0x004000,"    you want to sell it after the yesterday price:%d*(1+%d)=%d"%(yesterdayprice,uprate,sellprice))
						if nowprice>=sellprice:
							self.textinfo(self.TextLog,0x004000,"    you can sell it now")
							self.playsound("E:\\sound1.mid")
							self.Strategy.disable(j)	
					if integer(j.type)==4:
						buyprice=yesterdayprice*(1-downrate)
						self.textinfo(self.TextLog,0x004000,"    you want to buy it after the yesterday price:%d*(1-%d)=%d"%(yesterdayprice,downrate,buyprice))
						if nowprice<=buyprice:
							self.textinfo(self.TextLog,0x004000,"    you can buy it now")
							self.playsound("E:\\sound1.mid")	
							self.Strategy.disable(j)
							
			e32.ao_sleep(120)  # sleep 120 sec

	def handle_runstop(self):
		self.stopflag=1
				
	def newstrategyid(self):
		id=self.Strategy.get_max_id()
		return id+1
		
	def playsound(self,sound)
		S = audio.Sound.open(sound)
		S.play()

		
	def getstock(self,code)
		#if this code not run,maybe the next open code can't run correctly! 
	
		params = urllib.urlencode({'code': unicode(code)})
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
			return "error"
  	
	def getdataindex(sele,udata,index)
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