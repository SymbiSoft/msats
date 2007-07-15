import appuifw
import urllib
import httplib

def getstock(code):
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
	
code="000001"
udata=getstock(code)
print udata
ucode=u"000001"
udata=getstock(ucode)
print udata
