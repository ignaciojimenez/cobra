# -*- coding: latin-1 -*-

import os,time,json,urllib,ConfigParser

def checkPlaying():
	xbmc_host = 'localhost'
	xbmc_port = 80
	xbmc_json_rpc_url = "http://" + xbmc_host + ":" + str(xbmc_port) + "/jsonrpc"
	payload = {"jsonrpc": "2.0", "method": "Player.GetActivePlayers", "id": 1}
	url_param = urllib.urlencode({'request': json.dumps(payload)})
	
	result = json.load(urllib.urlopen(xbmc_json_rpc_url + '?' + url_param))
	#print result
	if result['result']:
		return True
	else:
		return False


def tail(f, n, offset=None):
	"""Reads a n lines from f with an offset of offset lines.  The return
	value is a tuple in the form ``(lines, has_more)`` where `has_more` is
	an indicator that is `True` if there are more lines in the file.
	"""
	avg_line_length = 150
	to_read = n + (offset or 0)
	while 1:
		try:
			f.seek(-(avg_line_length * to_read), 2)
		except IOError:
			# woops.  apparently file is smaller than what we want
			# to step back, go to the beginning instead
			f.seek(0)
		pos = f.tell()
		lines = f.read().splitlines()
		if len(lines) >= to_read or pos == 0:
			return lines[-to_read:offset and -offset or None],len(lines) > to_read or pos > 0
		avg_line_length *= 1.3

#MAIN                                                                                                                                                 
if __name__ == '__main__': 

	config = ConfigParser.ConfigParser()
	config.readfp(open('/home/osmc/.cobra/conf.ini'))
	logfile = config.get('RSS','cobraBase')+config.get('RSS','logfile')

	#print time.ctime() + " - Errorss.py started"

	fo = open(logfile, "r")
	#print tail(fo,1)[0][0]

	if "bozo" in tail(fo,1)[0][0]:
		if checkPlaying():
			print "["+ time.ctime() + "] Bozofound but Playing"
		else:
			print "["+ time.ctime() + "] Bozofound REBOOTING..."
			os.system('/sbin/shutdown -r now "Bozofound reboot"')
	else:
		print "["+ time.ctime() + "] No bozo"
