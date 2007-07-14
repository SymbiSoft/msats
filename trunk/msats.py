import time

import e32
import e32db
import appuifw

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
	
	def add(self, e):
		self.native_db.execute(e.sql_add())

	def delete(self, e):
		self.native_db.execute(e.sql_delete())
		
class StrategyEntry:
	sql_create = u"CREATE TABLE strategy (id integer,code varchar,type integer,startprice float,uprate float,downrate float)"
	StrategyType=[u"Sell after up start price",u"Buy after down start price",u"Sell after up previous day price",u"Buy after down previous day price"]
	
	def __init__(self, r=None):
		if r:			
			self.id  = r.col(1)
			self.code  = r.col(2)
			self.type  = r.col(3)
			self.startprice  = r.col(4)
			self.uprate  = r.col(5)
			self.downrate  = r.col(6)
		else:
			self.id  = 0
			self.code  =u''
			self.type  = 1
			self.startprice  = 0.0
			self.uprate  = 0.0
			self.downrate  = 0.0
			
	def sql_add(self):
		sql = "INSERT INTO strategy (id,code,type,startprice,uprate,downrate) VALUES (%d,%s,%d,%d,%d,%d)"%(
			self.id,self.code,self.type,self.startprice,self.uprate,sele.downrate)
		return unicode(sql)
	
	def sql_delete(self):
		sql = "DELETE FROM strategy WHERE id=%d"%\
			  (self.id)
		return unicode(sql)
		
	def get_id(self):
		return self.id	
	
	def get_code(self):
		return self.code
	
	def get_form(self):
		result = [(u"Id", 'number', int(self.id)),
				  (u"Code", 'Text', int(self.code))]
		if self.type==None:
			result.append((u"Type", 'combo', (self.StrategyType,0)))
		else:
			result.append((u"Type", 'combo', (self.StrategyType,self.type)))
		result.append((u"StartPrice", 'number', float(self.startprice)))
		result.append((u"UpRate", 'number', float(self.uprate)))
		result.append((u"DownRate", 'number', float(self.downrate)))
		return result
		
	def set_from_form(self, form):
		self.id  = int(form[0][2])
		self.code  = form[1][2]
		self.type	 = form[2][2][1]
		self.startprice   = float(form[3][2])
		self.uprate   = float(form[4][2])
		self.downrate   = float(form[5][2])
		
class MsatsApp:

	def __init__(self):
		self.lock = e32.Ao_lock()
		self.exit_flag = False
		appuifw.app.exit_key_handler = self.abort
		self.entry_list = []
		self.menu_stockmanage = (u"Stock Manage", self.handle_stockmanage)
		self.menu_strategy = (u"Strategy Manage", self.handle_strategymange)
		self.menu_run = (u"Run", self.handle_run)
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

	def update_entry_list(self):
		self.entry_list = self.Personsrelation.get_all_entries()

	def show_main_view(self):
		self.show_menu()  
	
	def show_menu(self):	
		appuifw.app.menu = [self.menu_stockmanage,
								self.menu_strategy,
								self.menu_persondie,
								self.menu_run]

			
	def handle_stockmanage(self):
		i=1
		
		
	def handle_strategymange(self):	
		i=2
	
	def handle_run(self):
		i=3
		
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