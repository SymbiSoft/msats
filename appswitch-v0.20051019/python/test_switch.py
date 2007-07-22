"""
module appswitch 

functions:
  tuple application_list(include_all)
    returns running applications (tuple of unicode strings)
    pararameters:
      include_all = iff true, hidden apps are listed

  bool switch_to_fg(app)
  bool switch_to_bg(app)
    switches given application to foreground/background.
    returns true iff app with that caption found.
    paramaters:
      app - unicode string (see application_list)
      
  bool end_app(app)
    request closing of given app
  bool kill_app(app)
    kills this app

  both return true if app found.
"""

import e32

import appswitch

apps = appswitch.application_list(True) # true = include all
                                       # false = no hidden apps 
print apps
for app in apps:
    print appswitch.switch_to_fg(app)    
    e32.ao_sleep(1)

