import feedparser,re,time,subprocess,ConfigParser,os,sys

config = ConfigParser.ConfigParser()
config.readfp(open('/home/pi/.cobra/conf.ini'))
auth = config.get('RSS','auth')

try:
	subprocess.check_call('transmission-remote --auth '+re.escape(auth)+' -l',shell = True, stdout=open(os.devnull, 'w'))
	print "["+ time.ctime() + "] Transmission OK"
except:
	try:
		print "["+ time.ctime() + "] ERROR: Reiniciando transmission"
		subprocess.check_call('service transmission-daemon restart', shell = True)
		time.sleep(1)
		print "["+ time.ctime() + "] Transmission REINICIADO OK"
	except:
		print "["+ time.ctime() + "] ERROR: No se pudo reiniciar transmission"
#checkagain
