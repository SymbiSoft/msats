#
# test_calendar.py
#
# Copyright (c) 2006-2007 Nokia Corporation
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

#
# PLEASE TRY THIS WITH A MOBILE DEDICATED TO TESTING PURPOSES ONLY.
#


import calendar
import time
import e32


# script1, show default db.

def script1():
    db=calendar.open()
        
    for entry_id in db:
        ent=db[entry_id]

        print 'id:%i'%ent.id    
        print 'content:%s'%ent.content
        print 'originating:%d'%ent.originating
        print 'location:%s'%ent.location
        print 'start_time:%s'%time.ctime(ent.start_time)
        print 'end_time:%s'%time.ctime(ent.end_time)   
        print 'repeat:' 
        print ent.get_repeat()       
        print '--------'
       
        
    print 'number of entries:%i'%len(db)
    

# script2, create new database and entry etc.

def script2():   
    # open (create if does not exist) the database.
    db=calendar.open('c:cal_test_db.cdb','c')
    
    week=7*24*60*60
    hour=60*60
    minute=60
    now=time.time()
    
    print 'entries in db:%i'%len(db)
    print 'add an appointment..'
    new_entry=db.add_appointment() # new appointment.
   
    new_entry.set_time(now+week,now+week+hour)
    new_entry.alarm=now+week-5*minute
    new_entry.content='the meeting'
    new_entry.location='conference room 01'
    new_entry.replication='private'
    if e32.s60_version_info[0]>=2:
        new_entry.priority=1 # high priority.          
    new_entry.commit()
    
    print 'entries in db now:%i'%len(db)
    print '**entry\'s data**'
    print 'id:%i'%new_entry.id
    print 'content:%s'%new_entry.content
    print 'location:%s'%new_entry.location
    print 'start_time:%s'%time.ctime(new_entry.start_time)
    print 'end_time:%s'%time.ctime(new_entry.end_time)
    print 'last modified:%s'%time.ctime(new_entry.last_modified)
    print 'alarm datetime:%s'%time.ctime(new_entry.alarm)
    print 'replication:%s'%new_entry.replication
    if e32.s60_version_info[0]>=2:
        print 'priority:%d'%new_entry.priority
    #print 'crossed out:%s'%new_entry.crossed_out
    print '--------'

    print 'now we\'ll delete the entry..'
    del db[new_entry.id]
    print 'entries in db now:%i'%len(db)
    print ''
    
    # add todo entry.
    print 'add a todo..'
    new_entry=db.add_todo() # new todo.
    new_entry.set_time(now+week)
    new_entry.alarm=now+week-5*minute
    new_entry.content='the things todo'
    new_entry.location='work'
    new_entry.replication='private'
    new_entry.priority=3 # low priority.
    new_entry.commit()
       
    print 'entries in db now:%i'%len(db)
    print '**entry\'s data**'
    print 'id:%i'%new_entry.id
    print 'content:%s'%new_entry.content
    print 'location:%s'%new_entry.location
    print 'start_time:%s'%time.ctime(new_entry.start_time)
    print 'end_time:%s'%time.ctime(new_entry.end_time)
    print 'last modified:%s'%time.ctime(new_entry.last_modified)
    print 'alarm datetime:%s'%time.ctime(new_entry.alarm)
    print 'replication:%s'%new_entry.replication
    print 'priority:%d'%new_entry.priority
    print 'crossed out:%s'%new_entry.crossed_out
    print '--------'
    
    # cross out the entry.
    new_entry.cross_out_time=time.time()
    print 'after crossing out:'
    
    print new_entry.crossed_out
    print 'crossed out:%s'%new_entry.crossed_out
    print 'cross out time:%s'%time.ctime(new_entry.cross_out_time)
    print 'alarm:%s'%str(new_entry.alarm)
    print ''
    
    print 'now we\'ll delete the entry..'
    del db[new_entry.id]
    print 'entries in db now:%i'%len(db)

    
# script3, open db (not the default db) and create an entry.

def script3():

    week=7*24*60*60
    hour=60*60
    minute=60
    day=24*60*60
    now=time.time()

    # create and open new database.
    db=calendar.open('d:cal_test_db.cdb','n')
    
    print 'entries in db:%i'%len(db)
    print 'add a todo..'
    new_entry=db.add_todo() # new todo.
    new_entry.set_time(now+week,now+week+hour)
    new_entry.content='things to do'
    new_entry.location='--'
    new_entry.commit()
    
    print 'entries in db now:%i'%len(db)
    print 'entry\'s data'
    print 'id:%i'%new_entry.id
    print 'content:%s'%new_entry.content
    print 'location:%s'%new_entry.location
    print 'start_time:%s'%time.ctime(new_entry.start_time)
    print 'end_time:%s'%time.ctime(new_entry.end_time)
    print 'last modified:%s'%time.ctime(new_entry.last_modified)
    print '--------'

    print 'now we\'ll delete the entry..'
    del db[new_entry.id]
    print 'entries in db now:%i'%len(db)
   

# script4, simple repeat test.

def script4():
    week=7*24*60*60
    day=24*60*60
    hour=60*60
    minute=60
    now=time.time()
    
    db=calendar.open() 

    # create an appointment.
    new_entry=db.add_appointment() # new appointment.
    new_entry.set_time(now+2*week,now+2*week+hour)
    new_entry.alarm=now+week-5*minute
    new_entry.content='repeat test'
    new_entry.location='somewhere'
   
        
    # make it repeat weekly for 4 weeks.
    repeat={'type':'weekly',
            "days":[0,1], #which days in a week (monday,tuesday)
            'start':new_entry.start_time,
            'end':new_entry.start_time+4*week-day}
     
    new_entry.set_repeat(repeat)
     
    new_entry.commit()
    
    # print the repeat information.
    print new_entry.get_repeat()
    

# script5, another repeat example.

def script5():
   
    week=7*24*60*60
    day=24*60*60
    hour=60*60
    minute=60
    now=time.time()
    
    db=calendar.open()

        
    # create an appointment.
    new_entry=db.add_appointment()
    new_entry.set_time(now+week,now+week+hour)
    new_entry.alarm=now+week-5*minute
    new_entry.content='rep debug test'
    new_entry.location='somewhere'

    
    
    # repeat on tuesdays and thursdays every second week except on the exception dates ('exceptions').
    repeat={'type':'weekly',
            'start':new_entry.start_time,
            'end':new_entry.start_time+10*week,
            'days':[1,3], # repeat on tuesday and thursday.
            'exceptions':list([new_entry.start_time+week+i*day for i in range(7)]), # no repeats on these days.
            'interval':2 # repeat every second week.
            }
     
    new_entry.set_repeat(repeat)
   
    new_entry.commit()

    # print the repeat information.
    print new_entry.get_repeat()


# script6, various repeat types.

def script6():
    
    week=7*24*60*60
    day=24*60*60
    hour=60*60
    minute=60
    now=time.time()
    
    db=calendar.open()
   
    # create an appointment.
    new_entry=db.add_appointment()
    new_entry.set_time(now+week,now+week+hour)
    new_entry.alarm=now+week-5*minute
    new_entry.content='daily rep'
    new_entry.location='somewhere'

    repeat={'type':'daily',
            'start':new_entry.start_time,
            'end':new_entry.start_time+week-day,
            'interval':2} # on every second day.

    new_entry.set_repeat(repeat)
    new_entry.commit()

    
    # create an another appointment.
    new_entry_2=db.add_appointment()
    new_entry_2.set_time(now+week,now+week+hour)
    new_entry_2.alarm=now+week-5*minute
    new_entry_2.content='monthly rep by dates'
    new_entry_2.location='somewhere'

    # set monthly repeat (by dates) for 90 days.
    repeat={'type':'monthly_by_dates',
            'start':new_entry_2.start_time,
            'end':new_entry_2.start_time+90*day-day,
            'days':[9,19] # set the repeat occur 10th and 20th day of the month.
            }

    new_entry_2.set_repeat(repeat)
    new_entry_2.commit()
    

    # create third appointment.
    new_entry_3=db.add_appointment()
    new_entry_3.set_time(now+week,now+week+hour)
    new_entry_3.alarm=now+week-5*minute
    new_entry_3.content='monthly rep by days'
    new_entry_3.location='somewhere'

    # set monthly repeat (by days) for 90 days.
    repeat={'type':'monthly_by_days',
            'start':new_entry_3.start_time,
            'end':new_entry_3.start_time+90*day-day,
            'days':[{'week':1,'day':1},{'week':4,'day':4}], # second tuesday and last friday of the month.
            } 
    new_entry_3.set_repeat(repeat)
    new_entry_3.commit()
    
    # create fourth appointment.
    new_entry_4=db.add_appointment()
    new_entry_4.set_time(now+week,now+week+hour)
    new_entry_4.alarm=now+week-5*minute
    new_entry_4.content='yearly rep by date'
    new_entry_4.location='somewhere'

    # set yearly repeat (by date) for 3 years.
    repeat={'type':'yearly_by_date',
            'start':new_entry_4.start_time,
            'end':new_entry_4.start_time+3*365*day-day}
    new_entry_4.set_repeat(repeat)
    new_entry_4.commit()


    # create fifth appointment.
    new_entry_5=db.add_appointment()
    new_entry_5.set_time(now+week,now+week+hour)
    new_entry_5.alarm=now+week-5*minute
    new_entry_5.content='yearly rep by day'
    new_entry_5.location='somewhere'

    # set yearly repeat (by day) on third thursday of june
    # during time interval new_entry.start_time -- new_entry.start_time+3*365*day-day.
    repeat={'type':'yearly_by_day',
            'start':new_entry_5.start_time,
            'end':new_entry_5.start_time+3*365*day-day,
            'days':{'day':3,'week':2,'month':5}}
    new_entry_5.set_repeat(repeat)
    new_entry_5.commit()
    
    
    print new_entry.get_repeat()
    print new_entry_2.get_repeat()
    print new_entry_3.get_repeat()
    print new_entry_4.get_repeat()
    print new_entry_5.get_repeat()    

# script7, vcalendar export.

def script7():
    db=calendar.open()
    if len(db)==0:
        print 'no entries in db'
        return
    id_list=list()
    for id in db:
        id_list.append(id)
        break # export only one entry.
    print db.export_vcalendars(tuple(id_list))


# script8, vcalendar import.

def script8():

    db=calendar.open()
    if len(db)==0:
        print 'no entries in db'
        return
    id_list=list()
    for id in db:
        id_list.append(id)
        break # export only one entry.
    vcals=db.export_vcalendars(tuple(id_list))
    print 'imported following vcals (id:s shown) %s'%str(db.import_vcalendars(vcals))


# script9, searching.

def script9():
    
    week=7*24*60*60
    day=24*60*60
    
    # open the 'default' database.
    db=calendar.open()

  
    # print entry instances occurring this month
    # (instance is a pair of entry id and datetime value).
    print 'monthly instances:'
    print db.monthly_instances(time.time())

    # get only todos and events.
    print 'monthly todo and event instances:'
    print db.monthly_instances(time.time(),events=1,todos=1)

    # print instances occurring today.
    print 'daily instances:'
    print db.daily_instances(time.time())
    
    # print todo and event instances occurring today.
    print 'daily todo and event instances:'
    print db.daily_instances(time.time(),events=1,todos=1)

    # print todo and event instances that have string 'e' in their
    # content (as a substring). note that only the instances occurring
    # one day are printed (the first day in the given time interval
    # that has a matching instance).
    print 'instances found by string search:'
    print db.find_instances(time.time(),time.time()+4*week-day,u'e')
    
    
# script10, cancel alarms.

def script10():
    db=calendar.open()

    for id in db: 
        db[id].alarm=None # note that autocommit is on.


# script11, autocommit test.

def script11():
    db=calendar.open()
  
    if not len(db):
        print 'no entries in db.'
        return

    for id in db:
        entry=db[id]


    entry.content='TEXT I' # autocommit is now on..
    print 'content:%s'%db[entry.id].content # ..since the content has changed in the database.
    entry.begin() # autocommit is now off..
    entry.content='TEXT II'
    print 'content now:%s'%db[entry.id].content # ..since the content has not changed in the database.
    entry.commit() # now the changes are saved..
    print 'content at last:%s'%db[entry.id].content # ..since the content has changed in the database.


    entry.content='TEXT III' # autocommit is now on..
    print 'content:%s'%db[entry.id].content # ..since the content has changed in the database.
    entry.begin() # autocommit is now off..
    entry.content='TEXT IV'
    print 'content now:%s'%db[entry.id].content # ..since the content has not changed in the database.
    entry.commit() # now the changes are saved (and autocommit is set on again)..
    print 'content at last:%s'%db[entry.id].content
 

# script12, delete entries.

def script12():
    db=calendar.open()
   
    for id in db:
        del db[id]
    

import appuifw
import e32
lock=e32.Ao_lock()
appuifw.app.menu=[
    (u'show default db',script1),
    (u'new database and entry',script2),
    (u'open test db etc.',script3),
    (u'simple repeat test',script4),
    (u'another repeat test',script5),
    (u'various repeat types',script6),
    (u'vcalendar export',script7),
    (u'vcalendar import',script8),
    (u'searching',script9),
    (u'cancel alarms',script10),
    (u'autocommit',script11),
    (u'delete entries',script12),
    (u'Exit',lock.signal)]
old_exit_handler=appuifw.app.exit_key_handler
def exit_handler():
    appuifw.app.exit_key_handler=old_exit_handler
    lock.signal()

appuifw.app.exit_key_handler=exit_handler
lock.wait()




