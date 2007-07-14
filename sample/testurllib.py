import appuifw
import urllib
import httplib

#if this code not run,maybe the next open code can't run correctly! 
test1 = u"000001"
params = urllib.urlencode({'code': test1})
headers = {"Content-type": "application/x-www-form-urlencoded","Accept": "text/plain","Host":"www.jili8.com","X-Online-Host":"www.jili8.com"}
conn = httplib.HTTPConnection("10.0.0.172")
conn.request("POST", "/php/getstock.php", params, headers)
response = conn.getresponse()


url='http://www.jili8.com/php/getstock2.php?code=000001' 
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