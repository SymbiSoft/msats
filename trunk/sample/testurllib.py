import appuifw
import urllib
import httplib

#if this code not run,maybe the next open code can't run correctly! 
test1 = u"600151"
params = urllib.urlencode({'code': test1})
headers = {"Content-type": "application/x-www-form-urlencoded","Accept": "text/plain","Host":"orz8.appspot.com","X-Online-Host":"orz8.appspot.com"}
conn = httplib.HTTPConnection("10.0.0.172")
conn.request("POST", "/getstock", params, headers)
response = conn.getresponse()


url='http://orz8.appspot.com/getstock?code=600151' 
proxies={'http':'http://10.0.0.172:80'} 
print 'waiting!...'
data=urllib.FancyURLopener(proxies).open(url).read() 

try:
	udata=data.decode("utf8")
	usplitdata=[]
	usplitdata=udata.split(u"|")
	for i in usplitdata:
		print i
except:
	print "utf8 error!"