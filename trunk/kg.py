# Copyright (c) 2007 jili8

import time

import e32
import e32db
import appuifw

class KillGameDb:
	def __init__(self, db_name):
		try:
			self.native_db = e32db.Dbms()
			self.native_db.open(db_name)
		except:
			self.native_db.create(db_name)
			self.native_db.open(db_name)
			self.native_db.execute(PersonsRelationEntry.sql_create)
			self.native_db.execute(PersonsNumberEntry.sql_create)
			self.native_db.execute(PersonsEntry.sql_create)

	def close(self):
		self.native_db.close()
		
class PersonsRelation:
	def __init__(self, db_name):
		try:
			self.native_db = e32db.Dbms()
			self.native_db.open(db_name)
		except:
			KillGameDb(db_name)
			self.native_db = e32db.Dbms()
			self.native_db.open(db_name)	
	
	def get_all_entries(self):
		dbv = e32db.Db_view()
		dbv.prepare(self.native_db,
					u"SELECT * from personsrelation ORDER BY gameno DESC")
		dbv.first_line()
		results = []
		for i in range(dbv.count_line()):
			dbv.get_line()
			e = PersonsRelationEntry(dbv)
			results.append(e)
			dbv.next_line()
		return results
	
	def add(self, e):
		self.native_db.execute(e.sql_add())

	def delete(self, e):
		self.native_db.execute(e.sql_delete())

	def addpersonrelation(self,gameno,gameturn,personno,types,person2no):
		sql=u"INSERT INTO personsrelation (gameno, gameturn, personno, types, person2no) VALUES (%d,%d,%d,%d,%d)"%(
			gameno,
			gameturn,
			personno,
			types,
			person2no)
		self.native_db.execute(sql)

	def get_votenumber(self,gameno,gameturn,person2no):
		dbv = e32db.Db_view()
		dbv.prepare(self.native_db,
					u"SELECT * from personsrelation where gameno=%d and gameturn=%d and types=999 and person2no=%d"%(gameno,gameturn,person2no))
		return dbv.count_line()
	
	def getbygameturn(self,gameno,gameturn):
		dbv = e32db.Db_view()
		dbv.prepare(self.native_db,
					u"SELECT * from personsrelation where gameno=%d and gameturn=%d"%(gameno,gameturn))
		dbv.first_line()
		results = []
		for i in range(dbv.count_line()):
			dbv.get_line()
			e = PersonsRelationEntry(dbv)
			results.append(e)
			dbv.next_line()
		return results
		
	def getbypersonsrelation(self,gameno,personno,types):
		dbv = e32db.Db_view()
		dbv.prepare(self.native_db,
					u"SELECT * from personsrelation where gameno=%d and personno=%d and types=%d"%(gameno,personno,types))
		dbv.first_line()
		results = []
		for i in range(dbv.count_line()):
			dbv.get_line()
			e = PersonsRelationEntry(dbv)
			results.append(e)
			dbv.next_line()
		return results
	
	def getbypersonsrelationnot(self,gameno,personno,types):
		dbv = e32db.Db_view()
		dbv.prepare(self.native_db,
					u"SELECT * from personsrelation where gameno=%d and personno=%d and types<>%d"%(gameno,personno,types))
		dbv.first_line()
		results = []
		for i in range(dbv.count_line()):
			dbv.get_line()
			e = PersonsRelationEntry(dbv)
			results.append(e)
			dbv.next_line()
		return results
	
	def getbypersonsrelation2(self,gameno,person2no,types):
		dbv = e32db.Db_view()
		dbv.prepare(self.native_db,
					u"SELECT * from personsrelation where gameno=%d and person2no=%d and types=%d"%(gameno,person2no,types))
		dbv.first_line()
		results = []
		for i in range(dbv.count_line()):
			dbv.get_line()
			e = PersonsRelationEntry(dbv)
			results.append(e)
			dbv.next_line()
		return results
	
	def getbypersonsrelationnot2(self,gameno,person2no,types):
		dbv = e32db.Db_view()
		dbv.prepare(self.native_db,
					u"SELECT * from personsrelation where gameno=%d and person2no=%d and types<>%d"%(gameno,person2no,types))
		dbv.first_line()
		results = []
		for i in range(dbv.count_line()):
			dbv.get_line()
			e = PersonsRelationEntry(dbv)
			results.append(e)
			dbv.next_line()
		return results
		
class PersonsRelationEntry:
	sql_create = u"CREATE TABLE personsrelation (gameno INTEGER,gameturn INTEGER,personno INTEGER, types INTEGER, person2no INTEGER)"
	SayType=[u"civilian",u"police",u"killer",u"not civilian",u"not police",u"not killer"]

	# Initialize with a row from Sport_diary_db
	def __init__(self, r=None):
		if r:			
			self.gameno  = r.col(1)
			self.gameturn   = r.col(2)
			self.personno   = r.col(3)
			self.types	  = r.col(4)
			self.person2no	= r.col(5)
		else:
			self.gameno  = 0
			self.gameturn   = 0
			self.personno   = 0
			self.types	  = 0
			self.person2no	= 0

	def sql_add(self):
		sql = "INSERT INTO personsrelation (gameno, gameturn, personno, types, person2no) VALUES (%d,%d,%d,%d,%d)"%(
			self.gameno,
			self.gameturn,
			self.personno,
			self.types,
			self.person2no)
		return unicode(sql)
	
	def sql_delete(self):
		sql = "DELETE FROM personsrelation WHERE gameno=%d"%\
			  (self.gameno,self.personno)
		return unicode(sql)
		
	def get_gameno(self):
		return self.gameno
	
	def get_gameturn(self):
		return self.gameturn

	def get_personno(self):
		return self.personno

	def get_types(self):
		return self.types

	def get_person2no(self):
		return self.person2no

	def get_form(self):
		result = [(u"GameTurn", 'number', int(self.gameturn)),
				  (u"PersonNo", 'number', int(self.personno))]
		if self.types==None:
			result.append((u"Types", 'combo', (self.SayType,0)))
		else:
			result.append((u"Types", 'combo', (self.SayType,self.types)))
		result.append((u"Person2No", 'number', int(self.person2no)))
		return result
		
	def set_from_form(self, form,gameno):
		self.gameno = gameno
		self.gameturn  = int(form[0][2])
		self.personno  = int(form[1][2])
		self.types	 = form[2][2][1]
		self.person2no   = int(form[3][2])

class PersonsNumber:
	def __init__(self, db_name):
		try:
			self.native_db = e32db.Dbms()
			self.native_db.open(db_name)
		except:
			KillGameDb(db_name)
			self.native_db = e32db.Dbms()
			self.native_db.open(db_name)

	def get_all_entries(self):
		dbv = e32db.Db_view()
		dbv.prepare(self.native_db,
					u"SELECT * from personsnumber ORDER BY gameno DESC")
		dbv.first_line()
		results = []
		for i in range(dbv.count_line()):
			dbv.get_line()
			e = PersonsNumberEntry(dbv)
			results.append(e)
			dbv.next_line()
		return results
	
	def get_max_gameno(self):
		dbv = e32db.Db_view()
		dbv.prepare(self.native_db,
					u"SELECT gameno from personsnumber ORDER BY gameno DESC")
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

			
class PersonsNumberEntry:
	sql_create = u"CREATE TABLE personsnumber (gameno INTEGER,personsnumber INTEGER,policesnumber INTEGER, killersnumber INTEGER)"
	
	def __init__(self, r=None):
		if r:			
			self.gameno =r.col(1)
			self.personsnumber  = r.col(2)
			self.policesnumber   = r.col(3)
			self.killersnumber   = r.col(4)
		else:
			self.gameno =0
			self.personsnumber  = 0
			self.policesnumber   = 0
			self.killersnumber   = 0

	def sql_add(self):
		sql = "INSERT INTO personsnumber (gameno, personsnumber, policesnumber, killersnumber) VALUES (%d,%d,%d,%d)"%(
			self.gameno,
			self.personsnumber,
			self.policesnumber,
			self.killersnumber)
		return unicode(sql)
	
	def sql_delete(self):
		sql = "DELETE FROM personsnumber WHERE gameno=%d"%\
			  self.gameno
		return unicode(sql)
		
	def get_gameno(self):
		return self.gameno
	
	def get_personsnumber(self):
		return self.personsnumber

	def get_policesnumber(self):
		return self.policesnumber

	def get_killersnumber(self):
		return self.killersnumber
			
	def get_form(self):
		result = [(u"Persons Number", 'number', int(self.personsnumber)),
				  (u"Polices Number", 'number', int(self.policesnumber)),
				  (u"Killers Number", 'number', int(self.killersnumber))]
	
		return result
		
	def set_from_form(self, form,gameno):
		self.gameno = gameno
		self.personsnumber = int(form[0][2])
		self.policesnumber  = int(form[1][2])
		self.killersnumber  = int(form[2][2])
		
	def personsnum_info(self,form):
		appuifw.note(u""+str(form[0][2])+u"Persons;"+str(form[1][2])+u"Polices;"+str(form[2][2])+u"killers", 'info')

class Persons:

	def __init__(self, db_name):
		try:
			self.native_db = e32db.Dbms()
			self.native_db.open(db_name)
		except:
			KillGameDb(db_name)
			self.native_db = e32db.Dbms()
			self.native_db.open(db_name)

	def get_all_entries(self):
		dbv = e32db.Db_view()
		dbv.prepare(self.native_db,
					u"SELECT * from persons ORDER BY gameno DESC")
		dbv.first_line()
		results = []
		for i in range(dbv.count_line()):
			dbv.get_line()
			e = PersonsEntry(dbv)
			results.append(e)
			dbv.next_line()
		return results
	
	def add(self, e):
		self.native_db.execute(e.sql_add())

	def delete(self, e):
		self.native_db.execute(e.sql_delete())
	
	def updatepersontype(self, e):
		self.native_db.execute(e.sql_updatepersontype())

	def updatepersondie(self, e):
		self.native_db.execute(e.sql_updatepersondie())
	
	def updateuserflagandtype(self, e):
		self.native_db.execute(e.sql_updateuserflagandtype())
		
	def getpersonbytype(self,gameno,persontype,sure):
		dbv = e32db.Db_view()
		dbv.prepare(self.native_db,
					u"SELECT personno from persons where gameno=%d and persontype=%d and sure=%d"%(gameno,persontype,sure))
		dbv.first_line()
		results = []
		for i in range(dbv.count_line()):
			dbv.get_line()
			results.append(dbv.col(1))
			dbv.next_line()
		return results
	
	def addallpersons(self,gameno,personsnumber):
		e=PersonsEntry()
		e.gameno=gameno
		e.persontype=0
		e.sure=0
		e.dieturn=0
		e.userflag=0
		for i in range(personsnumber):
			e.personno=i+1
			self.add(e)
	
	def setpersontype(self,gameno,personno,persontype,sure):
		sql=u"update persons set persontype=%d,sure=%d where gameno=%d and personno=%d"%(
			persontype,
			sure,
			gameno,
			personno)
		self.native_db.execute(sql)
	
	def setpersonuserflag(self,gameno,personno,userflag):
		sql=u"update persons set userflag=%d where gameno=%d and personno=%d"%(
			userflag,
			gameno,
			personno)
		self.native_db.execute(sql)
			  
	def setpersondie(self,gameno,personno,turn):
		sql=u"update persons set dieturn=%d where gameno=%d and personno=%d"%(
			turn,
			gameno,
			personno)
		self.native_db.execute(sql)
	
	def isuser(self,gameno,personno):
		sql=u"SELECT * from persons where gameno=%d and personno=%d"%(
			gameno,
			personno)
		sql=unicode(sql)
		dbv = e32db.Db_view()
		dbv.prepare(self.native_db,sql)
		if 0 == dbv.count_line():
			userflag=0
		else:
			dbv.first_line()
			dbv.get_line()
			userflag = int(dbv.col(6))	
		return userflag
			
	def isdiedperson(self,gameno,turn,personno):
		sql=u"SELECT * from persons where gameno=%d and personno=%d"%(
			gameno,
			personno)
		sql=unicode(sql)
		dbv = e32db.Db_view()
		dbv.prepare(self.native_db,sql)
		if 0 == dbv.count_line():
			dieturn=0
		else:
			dbv.first_line()
			dbv.get_line()
			dieturn = int(dbv.col(5))	
		
		if dieturn==0: 
			return 0
		if dieturn<=turn:
			return 1
		return 0

class PersonsEntry:
	PersonType = [u"civilian", u"police", u"killer"]
	sql_create = u"CREATE TABLE persons (gameno INTEGER,personno INTEGER,persontype INTEGER, sure INTEGER, dieturn INTEGER, userflag INTEGER)"
	
	# Initialize with a row from Sport_diary_db
	def __init__(self, r=None):
		if r:			
			self.gameno  = r.col(1)
			self.personno   = r.col(2)
			self.persontype   = r.col(3)
			self.sure	  = r.col(4)
			self.dieturn	= r.col(5)
			self.userflag	= r.col(6)
		else:
			self.gameno  =0 
			self.personno   =0 
			self.persontype   =0 
			self.sure	  =0 
			self.dieturn	=0
			self.userflag	= 0
	def sql_add(self):
		sql = "INSERT INTO persons (gameno,personno, persontype, sure, dieturn, userflag) VALUES (%d,%d,%d,%d,%d,%d)"%(
			self.gameno,
			self.personno,
			self.persontype,
			self.sure,
			self.dieturn,
			self.userflag)
		return unicode(sql)
	
	def sql_delete(self):
		sql = "DELETE FROM persons WHERE gameno=%d and personno=%d"%\
			  (self.gameno,self.personno)
		return unicode(sql)
	
	def sql_updatepersontype(self):
		sql = "update persons set persontype=%d,sure=%d WHERE gameno=%d and personno=%d"%\
			  (self.persontype,self.sure,self.gameno,self.personno)
		return unicode(sql)

	def sql_updatepersondie(self):
		sql = "update persons set dieturn=%d WHERE gameno=%d and personno=%d"%\
			  (self.dieturn,self.gameno,self.personno)
		return unicode(sql)
	
	def sql_updateuserflagandtype(self):
		sql = "update persons set persontype=%d,sure=%d,userflag=%d WHERE gameno=%d and personno=%d"%\
			  (self.persontype,self.sure,self.userflag,self.gameno,self.personno)
		return unicode(sql)
				
	def get_gameno(self):
		return self.gameno


	def get_personno(self):
		return self.personno
	
	def get_persontype(self):
		return self.persontype
	def get_sure(self):
		return self.sure

	def get_dieturn(self):
		return self.dieturn

	def get_form_persontype(self):
		result = [(u"PersonNo", 'number', int(self.personno))]
		if self.persontype==None:
			result.append((u"PersonType", 'combo',(self.PersonType,0)))
		else:		
			result.append((u"PersonType", 'combo',(self.PersonType,self.persontype)))  
		result.append((u"Sure", 'number', int(self.sure)))
		return result
		
	def set_from_form_persontype(self, form,gameno):
		self.gameno = gameno
		self.personno  = int(form[0][2])
		self.persontype  = form[1][2][1]
		self.sure	 = int(form[2][2])
		self.dieturn   = 0
		self.userflag   = 0

	def get_form_persondie(self):
		result = [(u"PersonNo", 'number', int(self.personno))]
		result.append((u"DieTurn", 'number', int(self.dieturn)))
		return result
		
	def set_from_form_persondie(self, form,gameno):
		self.gameno = gameno
		self.personno  = int(form[0][2])
		self.persontype  = 0
		self.sure	 = 0
		self.dieturn   = int(form[1][2])
		self.userflag   = 0
	
	def get_form_userflagandtype(self):
		result = [(u"Your Id No", 'number', int(self.personno))]
		if self.persontype==None:
			result.append((u"PersonType", 'combo',(self.PersonType,0)))
		else:		
			result.append((u"PersonType", 'combo',(self.PersonType,self.persontype)))  
		return result
		
	def set_from_form_userflagandtype(self, form,gameno):
		self.gameno = gameno
		self.personno  = int(form[0][2])
		self.persontype  = form[1][2][1]
		self.sure	 = 1
		self.dieturn   = 0
		self.userflag   = 1
		
class KillGameApp:
	ColorList=[0x0,0x004000,(255,0,0),0,255,(128,128,128)]
	PersonType = [u"civilian", u"police", u"killer"]
	SayType=[u"civilian",u"police",u"killer",u"not civilian",u"not police",u"not killer"]
	PersonNoList=[]
	
	gameno=0
	turn=1
	personsnumber=0
	policesnumber=0
	killersnumber=0
	yourno=0
	yourtype=0
	
	diedperson=0
	
	step=0
	
	LogText=appuifw.Text(u'')
	PoliceText=appuifw.Text(u'')
	KillerText=appuifw.Text(u'')
	TurnText=appuifw.Text(u'')
	PersonText=appuifw.Text(u'')
	
	def __init__(self):
		self.lock = e32.Ao_lock()
		self.exit_flag = False
		appuifw.app.exit_key_handler = self.abort
		self.entry_list = []
		self.menu_gamestart = (u"Start", self.handle_gamestart)
		self.menu_gamecontinue = (u"Continue", self.handle_gamecontinue)
		self.menu_persontype = (u"PersonType", self.handle_persontype)
		self.menu_persondie = (u"PersonDie", self.handle_persondie)
		self.menu_personrelation = (u"PersonRelation", self.handle_personrelation)
		self.menu_personvote = (u"PersonVote", self.handle_personvote)
		self.menu_gameend = (u"GameEnd", self.handle_gameend)
		appuifw.app.menu = []

	def initialize_db(self, db_name):
		self.kill_game = KillGameDb(db_name)
		self.PersonsNumber = PersonsNumber(db_name)
		self.PersonsRelation = PersonsRelation(db_name)
		self.Persons = Persons(db_name)
		
	def run(self):
		while not self.exit_flag:
			self.show_main_view()
			self.lock.wait()
		self.close()

	def close(self):
		appuifw.app.menu = []
		appuifw.app.body = None
		appuifw.app.exit_key_handler = None
		self.kill_game.close()

	def abort(self):
		if appuifw.query(u"Are you sure to quit?",'query'):
			self.exit_flag = True
			self.lock.signal()

	def update_entry_list(self):
		self.entry_list = self.Personsrelation.get_all_entries()

	def textinfo(self,textobj,color,info):
		textobj.color=color
		textobj.add(info+u'\n')
			
	def handle_tab(self,index):
		global lb
		if index == 0:
			self.log() 
		if index == 1:
			self.policerelated()
		if index == 2:
			self.killerrelated()
		if index == 3:
			self.turnrelated()
		if index == 4:
			self.personrelated()
		
	def log(self):
		appuifw.app.body=self.LogText

	def policerelated(self):
		self.PoliceText.clear()
		self.textinfo(self.PoliceText,self.ColorList[4],u"The polices are:")
		policelist=self.Persons.getpersonbytype(self.gameno,1,1)
		for i in policelist:
			self.textinfo(self.PoliceText,self.ColorList[5],unicode(i))
		self.textinfo(self.PoliceText,self.ColorList[4],u"The polices vote:")
		for i in policelist:
			self.textinfo(self.PoliceText,self.ColorList[5],u'police:#'+unicode(i))
			relationlist=self.PersonsRelation.getbypersonsrelation(self.gameno,int(i),999)
			for j in relationlist:
				self.textinfo(self.PoliceText,self.ColorList[2],u'has voted #'+unicode(j.person2no)+u' in turn: '+unicode(j.gameturn))
		self.textinfo(self.PoliceText,self.ColorList[4],u"The polices say:")
		for i in policelist:
			self.textinfo(self.PoliceText,self.ColorList[5],u'police:#'+unicode(i))
			relationlist=self.PersonsRelation.getbypersonsrelationnot(self.gameno,int(i),999)
			for j in relationlist:
				self.textinfo(self.PoliceText,self.ColorList[3],u'has said #'+unicode(j.person2no)+u' is '+self.SayType[j.types]+u' in turn: '+unicode(j.gameturn))
		self.textinfo(self.PoliceText,self.ColorList[4],u"Who votes the polices :")
		for i in policelist:
			self.textinfo(self.PoliceText,self.ColorList[5],u'police:#'+unicode(i))
			relationlist=self.PersonsRelation.getbypersonsrelation2(self.gameno,int(i),999)
			for j in relationlist:
				self.textinfo(self.PoliceText,self.ColorList[1],u'has voted by#'+unicode(j.personno)+u' in turn: '+unicode(j.gameturn))
		self.textinfo(self.PoliceText,self.ColorList[4],u"Who says the polices :")
		for i in policelist:
			self.textinfo(self.PoliceText,self.ColorList[5],u'police:#'+unicode(i))
			relationlist=self.PersonsRelation.getbypersonsrelationnot2(self.gameno,int(i),999)
			for j in relationlist:
				self.textinfo(self.PoliceText,self.ColorList[0],u'has beed said by #'+unicode(j.personno)+u' is '+self.SayType[j.types]+u' in turn: '+unicode(j.gameturn))
		appuifw.app.body=self.PoliceText
	
	def killerrelated(self):
		self.KillerText.clear()
		self.textinfo(self.KillerText,self.ColorList[4],u"The killers are:")
		killerlist=self.Persons.getpersonbytype(self.gameno,0,1)
		for i in killerlist:
			self.textinfo(self.KillerText,self.ColorList[5],u'killer: '+unicode(i))
		self.textinfo(self.KillerText,self.ColorList[4],u"The killers vote:")
		for i in killerlist:
			self.textinfo(self.KillerText,self.ColorList[5],u'killer:#'+unicode(i))
			relationlist=self.PersonsRelation.getbypersonsrelation(self.gameno,int(i),999)
			for j in relationlist:
				self.textinfo(self.KillerText,self.ColorList[2],u'has voted #'+unicode(j.person2no)+u' in turn: '+unicode(j.gameturn))
		self.textinfo(self.KillerText,self.ColorList[4],u"The killers say:")
		for i in killerlist:
			self.textinfo(self.KillerText,self.ColorList[5],u'killer:#'+unicode(i))
			relationlist=self.PersonsRelation.getbypersonsrelationnot(self.gameno,int(i),999)
			for j in relationlist:
				self.textinfo(self.KillerText,self.ColorList[3],u'has said #'+unicode(j.person2no)+u' is '+self.SayType[j.types]+u' in turn: '+unicode(j.gameturn))
		self.textinfo(self.KillerText,self.ColorList[4],u"Who votes the killers :")
		for i in killerlist:
			self.textinfo(self.KillerText,self.ColorList[5],u'killer:#'+unicode(i))
			relationlist=self.PersonsRelation.getbypersonsrelation2(self.gameno,int(i),999)
			for j in relationlist:
				self.textinfo(self.KillerText,self.ColorList[1],u'has been voted #'+unicode(j.personno)+u' in turn: '+unicode(j.gameturn))
		self.textinfo(self.KillerText,self.ColorList[4],u"Who says the killers :")
		for i in killerlist:
			self.textinfo(self.KillerText,self.ColorList[5],u'killer:#'+unicode(i))
			relationlist=self.PersonsRelation.getbypersonsrelationnot2(self.gameno,int(i),999)
			for j in relationlist:
				self.textinfo(self.KillerText,self.ColorList[0],u'has been said by #'+unicode(j.personno)+u' is '+self.SayType[j.types]+u' in turn: '+unicode(j.gameturn))
		appuifw.app.body=self.KillerText

	def turnrelated(self):
		turnno=appuifw.query(u"Turn no",'number')
		if turnno==None:
			return
		
		self.TurnText.clear()
		relationlist=self.PersonsRelation.getbygameturn(self.gameno,turnno)
		for j in relationlist:
			if j.types==999:
				self.textinfo(self.TurnText,self.ColorList[0],u'#'+unicode(j.personno)+u' has voted #'+unicode(j.person2no)+u' in turn: '+unicode(j.gameturn))
			else:
				self.textinfo(self.TurnText,self.ColorList[0],u'#'+unicode(j.personno)+u' has said #'+unicode(j.person2no)+u' is '+self.SayType[j.types]+u' in turn: '+unicode(j.gameturn))
		appuifw.app.body=self.TurnText
			
	def personrelated(self):
		personno=appuifw.query(u"Person no",'number')
		if personno==None:
			return
			
		self.PersonText.clear()
		self.textinfo(self.PersonText,self.ColorList[4],u"The #"+str(personno)+u" vote:")
		relationlist=self.PersonsRelation.getbypersonsrelation(self.gameno,personno,999)
		for j in relationlist:
			self.textinfo(self.PersonText,self.ColorList[2],u' has voted #'+unicode(j.person2no)+u' in turn: '+unicode(j.gameturn))
		self.textinfo(self.KillerText,self.ColorList[4],u"The #"+str(personno)+u" say:")
		relationlist=self.PersonsRelation.getbypersonsrelationnot(self.gameno,personno,999)
		for j in relationlist:
			self.textinfo(self.PersonText,self.ColorList[3],u' has said #'+unicode(j.person2no)+u' is '+self.SayType[j.types]+u' in turn: '+unicode(j.gameturn))
		self.textinfo(self.PersonText,self.ColorList[4],u"Who votes the #"+str(personno))
		relationlist=self.PersonsRelation.getbypersonsrelation2(self.gameno,personno,999)
		for j in relationlist:
			self.textinfo(self.PersonText,self.ColorList[1],u' has been voted #'+unicode(j.personno)+u' in turn: '+unicode(j.gameturn))
		self.textinfo(self.PersonText,self.ColorList[4],u"Who says the #"+str(personno))
		relationlist=self.PersonsRelation.getbypersonsrelationnot2(self.gameno,personno,999)
		for j in relationlist:
			self.textinfo(self.PersonText,self.ColorList[0],u' has been said by #'+unicode(j.personno)+u' is '+self.SayType[j.types]+u' in turn: '+unicode(j.gameturn))
		appuifw.app.body=self.PersonText

	def show_main_view(self):
		appuifw.app.set_tabs([u"Log",u"Police Related",u"Killer Related",u"Turn Related",u"Person Related"],self.handle_tab)
		appuifw.app.body=self.LogText
		self.show_menu(0)  
	
	def show_menu(self,flag):	
		if flag==0:
			appuifw.app.menu = [self.menu_gamestart]
		else:	
			appuifw.app.menu = [self.menu_gamecontinue,
								self.menu_persontype,
								self.menu_persondie,
								self.menu_personrelation,
								self.menu_personvote,
								self.menu_gameend]

	def newgameno(self):
		gameno=self.PersonsNumber.get_max_gameno()
		return gameno+1
		
	def get_form_partener(self,length):
		result = []
		for i in range(length):	
			result.append((u"partener "+str(i+1), 'number',0))
		return result
  
	def get_form_inspect(self):
		result = [(u"PersonNo", 'number', 0)]
		result.append((u"PersonType", 'combo',(self.PersonType,0)))
		return result
		
	def personkill(self,gameno,turn):
		if self.yourtype!=2:
			return
		if turn==1:
			appuifw.app.title = u"select your partener"
			length=self.killersnumber-1
			data=self.get_form_partener(length)
			flags = appuifw.FFormEditModeOnly+appuifw.FFormDoubleSpaced
			f = appuifw.Form(data, flags)
			f.execute()
			for i in range(length):	
				personno=int(f[i][2])
				if personno!=0:
					self.Persons.setpersontype(gameno,personno,2,1)
					
   
	def personinspect(self,gameno,turn):
		if self.yourtype!=1:
			return
		if turn==1:
			appuifw.app.title = u"select your partener"
			length=self.policesnumber-1
			data=self.get_form_partener(length)
			flags = appuifw.FFormEditModeOnly+appuifw.FFormDoubleSpaced
			f = appuifw.Form(data, flags)
			f.execute()
			for i in range(length):	
				personno=int(f[i][2])
				if personno!=0:
					self.Persons.setpersontype(gameno,personno,1,1)
					
		appuifw.app.title = u"who was inspected"	
		data=self.get_form_inspect()
		flags = appuifw.FFormEditModeOnly+appuifw.FFormDoubleSpaced
		f = appuifw.Form(data, flags)
		f.execute()
		personinspected=int(f[0][2])
		persontype=f[1][2][1]	
		self.Persons.setpersontype(gameno,personinspected,persontype,1)
		
	def get_form_personvote(self,length):
		result = []
		for i in range(length):	
			result.append((u"vote person "+str(i), 'number',0))
		return result

	def personvote(self,gameno,turn,person2no,length):   
		if self.Persons.isdiedperson(self.gameno,self.turn,person2no)==1:
			return
			
		appuifw.app.title = u'Who vote #'+str(person2no)+u' person?'
		data=self.get_form_personvote(length)
		flags = appuifw.FFormEditModeOnly+appuifw.FFormDoubleSpaced
		f = appuifw.Form(data, flags)
		f.execute()
		
		for i in range(length):	
			personno=int(f[i][2])
			if personno!=0:
				self.PersonsRelation.addpersonrelation(gameno,turn,personno,999,person2no)
				self.textinfo(self.LogText,self.ColorList[2],u'#'+str(person2no)+u' was voted by #'+str(personno))
	  
	def voteresult(self,gameno,turn,personlist):
		maxvotepersonlist=[]
	  
		maxcount=0
		
		for i in personlist:
			count=self.PersonsRelation.get_votenumber(gameno,turn,int(i))  
			
			if count==maxcount:
				maxvotepersonlist.append(unicode(i))
			if count>maxcount:
				maxvotepersonlist=[]
				maxvotepersonlist.append(unicode(i))
				maxcount=count	
			
		length=len(maxvotepersonlist)
		if length==1:
			outperson=int(maxvotepersonlist[0])
			if appuifw.query(u'please confirm '+unicode(maxvotepersonlist[0])+u' was out?','query')!=True:
				outperson=appuifw.query(u'out person','number')
			if outperson:
				self.Persons.setpersondie(gameno,outperson,turn)
				self.textinfo(self.LogText,self.ColorList[3],u'#'+unicode(outperson)+u' out!')
			
		if length>1:	
			if appuifw.query(u'more than one person has the same max vote,continue vote?','query'):
				self.makepersonnolist(self.gameno,self.turn)
				length=len(self.PersonNoList)
				for i in maxvotepersonlist:
					self.personvote(gameno,turn,int(i),length)
				self.voteresult(gameno,turn,maxvotepersonlist)
			else:
				outperson=appuifw.query(u'out person','number')
				if outperson!=None:
					self.Persons.setpersondie(gameno,outperson,turn)
					self.textinfo(self.LogText,self.ColorList[3],u'#'+unicode(outperson)+u' out!')
			
	def makepersonnolist(self,gameno,turn):
		self.PersonNoList=[]
		for i in range(self.personsnumber):
			if self.Persons.isdiedperson(gameno,turn,i+1)==0:
				self.PersonNoList.append(unicode(str(i+1)))
				
	def get_form_personsay(self):
		result = []
			
		result.append((u"PersonType", 'combo',(self.PersonType,0)))
		for i in range(3):
			result.append((u"Action"+str(i), 'combo', (self.SayType,0)))
			for j in range(3):
				result.append((u"Person2No"+ str(j), 'number', 0))
		return result

	def personsay(self,gameno,turn,personno):
		if self.Persons.isdiedperson(self.gameno,self.turn,personno)==1:
			return;
			
		appuifw.app.title = u"#"+str(personno)+u" say"
		data=self.get_form_personsay()
		flags = appuifw.FFormEditModeOnly+appuifw.FFormDoubleSpaced
		f = appuifw.Form(data, flags)
		f.execute()
		
		persontype=f[0][2][1]
		if persontype!=None:
			self.PersonsRelation.addpersonrelation(gameno,turn,personno,persontype,personno)
			self.textinfo(self.LogText,self.ColorList[0],u'#'+str(personno)+u' says he is '+ self.PersonType[persontype])
		for i in range(3):
			saytype=f[1+i*4][2][1]
			for j in range(3):
				person2no=int(f[2+i*4+j][2])
				
				if person2no!=0:
					self.PersonsRelation.addpersonrelation(gameno,turn,personno,saytype,person2no)
					self.textinfo(self.LogText,self.ColorList[1],u'#'+str(personno)+u' says #'+str(person2no)+u' is ' +self.SayType[saytype])
  
	def personvote2(self,diedflag):	
		result = [(u"Person2no",'number',0)]
		
		self.makepersonnolist(self.gameno,self.turn)
		length=len(self.PersonNoList)
		
		for i in range(length):	
			result.append((u"vote person "+str(i), 'number',0))
			
		appuifw.app.title = u'Person vote'
		flags = appuifw.FFormEditModeOnly+appuifw.FFormDoubleSpaced
		f = appuifw.Form(result, flags)
		f.execute()
		person2no=int(f[0][2])
		
		if self.Persons.isdiedperson(self.gameno,self.turn,person2no)==1:
			return
			
		for i in range(length):	
			personno=int(f[i+1][2])
			if personno!=0:
				self.PersonsRelation.addpersonrelation(self.gameno,self.turn,personno,999,person2no)
				self.textinfo(self.LogText,self.ColorList[2],u'#'+str(person2no)+u' was voted by #'+str(personno))
	
		if diedflag==1:
			self.Persons.setpersondie(self.gameno,person2no,self.turn)
  		
	def handle_gamestart(self):
		self.LogText.clear()
		self.gameno=self.newgameno()
		new_entry = PersonsNumberEntry()
		data = new_entry.get_form()
		flags = appuifw.FFormEditModeOnly+appuifw.FFormDoubleSpaced
		f = appuifw.Form(data, flags)
		f.execute()
		self.personsnumber = int(f[0][2])
		self.policesnumber  = int(f[1][2])
		self.killersnumber  = int(f[2][2])
		new_entry.set_from_form(f,self.gameno)
		self.PersonsNumber.add(new_entry)
		
		self.textinfo(self.LogText,self.ColorList[4],u'gameno='+str(self.gameno)+u' '+str(self.personsnumber)+u' persons '+str(self.policesnumber)+u' poilces '+str(self.killersnumber)+u' killers')
		
		self.Persons.addallpersons(self.gameno,self.personsnumber)
    
		new_entry = PersonsEntry()
		data = new_entry.get_form_userflagandtype()
		flags = appuifw.FFormEditModeOnly+appuifw.FFormDoubleSpaced
		f = appuifw.Form(data, flags)
		f.execute()
		self.yourno = int(f[0][2])
		self.yourtype  = f[1][2][1]
		new_entry.set_from_form_userflagandtype(f,self.gameno)
		self.Persons.updateuserflagandtype(new_entry)
		
		self.turn=1
		self.step=0
		self.show_menu(1)	
		
	def handle_gamecontinue(self):	
		self.step=self.step+1	
		if self.step==1:
			self.textinfo(self.LogText,self.ColorList[4],u' turn'+str(self.turn))
			self.personkill(self.gameno,self.turn)
			self.personinspect(self.gameno,self.turn)
			
			self.diedperson=appuifw.query(u'Who was killed on this turn?','number')
			if self.diedperson!=None:
				self.textinfo(self.LogText,self.ColorList[4],u'#'+str(self.diedperson)+u' was killed on this turn')
				self.personsay(self.gameno,self.turn,self.diedperson,)	
				self.Persons.setpersondie(self.gameno,self.diedperson,self.turn)
			else:
				self.step=self.step-1
		
		if self.step==2:	
			for i in range(self.personsnumber):
				personno=(i+self.diedperson)%self.personsnumber+1
				self.personsay(self.gameno,self.turn,personno)	
				
		if self.step==3:
			if appuifw.query(u"Directly input outed person and the person voted him",'query'):
				self.personvote2(1)
			else:
				self.makepersonnolist(self.gameno,self.turn)
				length=len(self.PersonNoList)
				for i in range(self.personsnumber):
					personno=(i+self.diedperson)%self.personsnumber+1
					self.personvote(self.gameno,self.turn,personno,length)
						
				self.makepersonnolist(self.gameno,self.turn)
				self.voteresult(self.gameno,self.turn,self.PersonNoList)
			self.turn=self.turn+1
			self.step=0
	
	def handle_persontype(self):
		new_entry = PersonsEntry()
		data = new_entry.get_form_persontype()
		flags = appuifw.FFormEditModeOnly+appuifw.FFormDoubleSpaced
		f = appuifw.Form(data, flags)
		f.execute()
		new_entry.set_from_form_persontype(f,self.gameno)
		self.Persons.updatepersontype(new_entry)
		
	def handle_persondie(self):
		new_entry = PersonsEntry()
		data = new_entry.get_form_persondie()
		flags = appuifw.FFormEditModeOnly+appuifw.FFormDoubleSpaced
		f = appuifw.Form(data, flags)
		f.execute()
		new_entry.set_from_form_persondie(f,self.gameno)
		self.Persons.updatepersondie(new_entry)
		
	def handle_personrelation(self):
		new_entry = PersonsRelationEntry()
		data = new_entry.get_form()
		flags = appuifw.FFormEditModeOnly+appuifw.FFormDoubleSpaced
		f = appuifw.Form(data, flags)
		f.execute()
		new_entry.set_from_form(f,self.gameno)
		self.PersonsRelation.add(new_entry)
	
	def handle_personvote(self):
		self.personvote2(0)
				
	def handle_gameend(self):
		self.show_menu(0)
						
	
def main():
	app = KillGameApp()
	app.initialize_db(u"e:\\KillGame.db")
	app.run()

if __name__ == '__main__':
	old_title = appuifw.app.title
	try:
		appuifw.app.title = u"Kill Game Assistant"
		e32.ao_yield()
		main()
	finally:
		appuifw.app.title = old_title
