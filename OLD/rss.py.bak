# -*- coding: latin-1 -*-

import os,feedparser,time,re,subprocess,sys,ConfigParser

#print "["+ time.ctime() + "] rss.py started"


config = ConfigParser.ConfigParser()
config.readfp(open('/home/pi/.cobra/conf_rss.ini'))
updateConf = config.get('RSS','cobraBase')+config.get('RSS','updateConf')
urlfeed = config.get('RSS','urlfeed')

configAuth = ConfigParser.ConfigParser()
configAuth.readfp(open('/home/pi/conf_auth.ini'))
auth = configAuth.get('AUT','auth')

with open(updateConf, "r") as f:
	lastUpdate = float(f.read())

feed = feedparser.parse(urlfeed)

if feed.bozo:
	print "["+ time.ctime() + "] ERROR: " + str(feed)
elif len(feed["items"]) == 0:
	print "["+ time.ctime() + "] No updated links - No links at all"
elif lastUpdate < time.mktime(feed["items"][0]["published_parsed"]):
	#se recorre el feed de 0 hasta arriba hasta que la coincide feed["items"][n]["published_parsed"] con lastUpdate
	n = 0
	i = 0
	#print "tamanio: " + str(len(feed['entries']))
	while n < len(feed['entries']):
		if lastUpdate < time.mktime(feed["items"][n]["published_parsed"]):
			#add to transmission
			try:
				subprocess.check_call('transmission-remote --auth '+ re.escape(auth)+ ' -a '+ feed["items"][n]["link"], shell = True,stdout=open(os.devnull, 'w'))
				i+=1
				okString = "["+ time.ctime() + "] - ["+ str(i) +"] "+"Added: " + feed["items"][n]["title"] + " - " +feed["items"][n]["link"]
				print okString.encode("latin-1","ignore")
			except:
				#print "["+ str(n+1) +"] "+"ERROR:Torrent no agregado= " + feed["items"][n]["title"]
				nokString = "["+ time.ctime() + "] - ["+ str(n+1) +"] "+"ERROR:Torrent no agregado= " + feed["items"][n]["title"]
				print nokString.encode("latin-1","ignore")
		n+=1

	lastUpdate = time.mktime(feed["items"][0]["published_parsed"])
	print "["+ time.ctime() + "] - ["+ str(i) +"] Torrents added"

	with open(updateConf, "w") as f:
		f.write(str(lastUpdate))
else:
	print "["+ time.ctime() + "] No updated links"
	sys.exit()
