import appswitch

# please start to-do before this test

print appswitch.switch_to_fg(u"TODO")
e32.ao_sleep(1)    
print appswitch.switch_to_bg(u"TODO")
e32.ao_sleep(1)
print appswitch.end_app(u"TODO")
e32.ao_sleep(1)
print appswitch.switch_to_fg(u"TODO")

print appswitch.switch_to_fg(u"PYTHON")
