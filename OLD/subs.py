# -*- coding: latin-1 -*-

import os,time,re,string,shutil,subprocess,sys,difflib,ConfigParser,json,urllib
from urllib import quote

def detectarIdioma(fichero):
	key = 'e38bcce17e1afea70f5c4539f8e5f47c'
	if "spanish" in fichero.lower():
		#print ("ES: " + fichero)
		return 'es'
	elif "espaᯬ" in fichero.lower():
		#print ("ES: " + fichero)
		return 'es'
	else:
		cadenaArchivo = os.path.splitext(fichero)[0].lower().replace(u".",u" ").replace(u"dvdrip",u"").replace(u"xvid",u"").replace(u"ac3",u"").replace(u"cd1",u"").replace(u"cd2",u"").replace(u"720p",u"").replace(u"aac",u"").replace(u"x264",u"").replace(u"brrip",u"").replace(u"5.1",u"").replace(u"spanish",u"").replace(u"(",u"").replace(u")",u"").replace(u"[",u"").replace(u"]",u"").replace(u"star wars",u"la guerra de las galaxias")
		respuesta = urllib.urlopen(u"http://ws.detectlanguage.com/0.2/detect?q="+quote(cadenaArchivo, safe=u'')+u"&key="+key)
		str_response = respuesta.read().decode(u'utf-8')
		obj = json.loads(str_response)

		for item in obj[u"data"][u"detections"]:
			if item[u"language"] == u'es':
				#print("ESDETECTADO: "+ cadenaArchivo)
				return u'es'
		#print("NO_DETECTADO: " + cadenaArchivo)
		return u'otros'		

def removeEmptyFolders(path):
	if not os.path.isdir(path):
		return

	# remove empty subfolders
	files = os.listdir(path)
	if len(files):
		for f in files:
			fullpath = os.path.join(path, f)
			if os.path.isdir(fullpath):
				removeEmptyFolders(fullpath)
	
	# if folder empty, delete it
	files = os.listdir(path)
	if len(files) == 0 and not any(path in s for s in rutas):
		print "["+ time.ctime() + "] Removing empty folder:"+ path
		os.rmdir(path)
		
		
def borrarDirsVacios():
	for path in rutas:
		removeEmptyFolders(path)


def comprobarRuta(directorio):
	if not os.path.exists(directorio):
		os.makedirs(directorio)
		
def obtenerSerie (archivo,ruta):	
	if re.search(ur"([sS])(\d+)([eE]|EP|ep)(\d+)",archivo) != None :
		m = re.search(ur"(.*)([sS])(\d+)([eE]|EP|ep)(\d+)",archivo)
	elif re.search(ur"(\d+)x(\d+)",archivo) != None :
		m = re.search(ur"(.*)(\d+)x(\d+)", archivo)
		
	if len(os.listdir(ruta)) > 0 and len(difflib.get_close_matches(m.group(1)[:-1].lower().replace(u".",u"-"), os.listdir(ruta), 1))> 0:
		return difflib.get_close_matches(m.group(1)[:-1].lower().replace(u".",u"-"), os.listdir(ruta), 1)[0]
	else:
		return m.group(1)[:-1].lower().replace(u".",u"-")

def descargarSubdownloader (fichero,root,rutaDestino,idioma):
	try:
		subprocess.check_call(u'subdownloader --cli -q --video='+ re.escape(os.path.join(root,fichero)) +u' -l '+idioma+u' --rename-subs --sol', shell = True)
		#subdownloader baja el subtitulo con todo en minusculas, por lo que hay que convertirlo al nombre de archivo.
		#si no se ha bajado nada no se ejecutan los siguientes comandos de mover fichero porque el renombrado dara error
		
		try:
			os.rename(os.path.join(root,os.path.splitext(fichero)[0].lower()+u".srt"), os.path.join(root,os.path.splitext(fichero)[0]+u".srt"))
		except:
			#print("Subdownloader: Subtitulo no encontrado para renombrar")
			return False
		
		#si es una serie
		if re.search(ur"([sS])(\d+)([eE]|EP|ep)(\d+)",fichero) != None or re.search(ur"(\d+)x(\d+)",fichero) != None:
			if not os.path.isdir(rutaDestino +u"/"+obtenerSerie(fichero,rutaDestino)):
				os.mkdir(rutaDestino +u"/"+obtenerSerie(fichero,rutaDestino))
			rutaFinal = rutaDestino +u"/"+obtenerSerie(fichero,rutaDestino)
		#si es una pelicula
		else:
			if not os.path.isdir(rutaDestino +u"/"+os.path.splitext(fichero)[0]):
				#creamos el directorio destino en caso de que no exista
				os.mkdir(rutaDestino +u"/"+os.path.splitext(fichero)[0])
			rutaFinal = rutaDestino +u"/"+os.path.splitext(fichero)[0]
		
		#print("el crear carpeta pelicula no casca")
		#print("\tSUBTITULO DESCARGADO = " + os.path.splitext(fichero)[0]+".srt")
		#movemos la pelicula
		
		shutil.move(os.path.join(root,fichero),os.path.join(rutaFinal,fichero))
		#print("\tdescargarSubdownloader: MOVIDA A = " + rutaFinal+"/"+fichero)
		#movemos el subtitulo
		shutil.move(root+u"/"+os.path.splitext(fichero)[0]+u".srt",rutaFinal+u"/"+os.path.splitext(fichero)[0]+u".srt")
		#print ('\tdescargarSubdownloader: EXITO: ARCHIVO y SUB DESCARGADOS EN= ' + rutaFinal+"/")
		return True
	except:
		#print(e.message())
		print "["+ time.ctime() + '] ERROR:descargarSubdownloader: SUBDOWNLOADER o NO EXISTE SUBTITULO'
		return False

###INICIO MAIN
if __name__ == u'__main__':

	print "["+ time.ctime() + "] subs.py started"
	config = ConfigParser.ConfigParser()
	config.readfp(open('/home/osmc/.cobra/conf.ini'))
	
	rutaOriginal = config.get('SUBS','downloadBase')+config.get('SUBS','rutaOriginal')
	rutaSeries = config.get('SUBS','downloadBase')+config.get('SUBS','rutaSeries')
	rutaPeliculas = config.get('SUBS','downloadBase')+config.get('SUBS','rutaPeliculas')
	idioma = config.get('SUBS','idioma')

	#TODO: recorrer todas las rutas que se carguen, no declararlas "a pelo"
	global rutas 
	rutas = [ rutaOriginal, rutaSeries, rutaPeliculas ]
		
	extensiones = [u"avi", u"mp4" , u"mkv",u"vob",u"mpg",u"iso"]

	comprobarRuta(rutaOriginal)
	comprobarRuta(rutaSeries)
	comprobarRuta(rutaPeliculas)
	
	#nos desplazamos a la ruta de descargas
	os.chdir(rutaOriginal)
	
	#exploramos recursivamente
	for root, dirs, files in os.walk(rutaOriginal):
		#print (os.path.join(root,fichero).strip(path))
		#print("Numero de ficheros leidos ="+str(len(files)))
		for fichero in files:
			#Comprobamos que sea un fichero grande
			if (os.path.getsize(os.path.join(root,fichero)))/(1024*1024.0) > 60 :
				#si es un fichero de las extensiones definidas previamente
				if any(fichero[-3:].lower() in s for s in extensiones):
					#print ("FICHERO VIDEO LEIDO: " + fichero)
					#comprobamos si es una serie (SXXEXX o XXxXX)
					if re.search(ur"([sS])(\d+)([eE]|EP|ep)(\d+)",fichero) != None or re.search(ur"(\d+)x(\d+)",fichero) != None:
						try:
							if descargarSubdownloader(fichero,root,rutaSeries,idioma) is False:
								print "["+ time.ctime() + "] NO-SUBS SERIE= "+fichero
							else:
								print "["+ time.ctime() + "] SUB DESCARGADO SERIE= " + os.path.join(root,fichero)

						except:
							print "["+ time.ctime() + "] ERROR: SUBDOWNLOADER; Fichero= "+fichero
				
					#si es una pelicula
					else:
						if detectarIdioma(fichero) != u'es':
							if descargarSubdownloader(fichero,root,rutaPeliculas,idioma) is False:
								print "["+ time.ctime() + "] NO-SUBS PELICULA EN= "+fichero
							else:
								print "["+ time.ctime() + "] SUB DESCARGADO PELICULA EN= " + os.path.join(root,fichero)
						else:
							shutil.move(os.path.join(root,fichero),os.path.join(rutaPeliculas,fichero))
							print "["+ time.ctime() + "] Pelicula ES Movida= "+os.path.join(root,fichero)
				else:
					#fichero no video grande
					print "["+ time.ctime() + "] Archivo grande no video . Dejado en carpeta =" + re.escape(os.path.join(root,fichero))
			else:
				#fichero pequeño comprobar srt
				if (os.path.splitext(fichero)[1] == '.srt'):
					shutil.move(root+"/"+os.path.splitext(fichero)[0]+".srt",root+"/"+os.path.splitext(fichero)[0]+".srt.downloaded")
					print "["+ time.ctime() + "] Archivo de subs presente. Dejado en origen y cambiada extension =" + re.escape(fichero)
				elif (os.path.splitext(fichero)[1] == '.downloaded'):
					print "["+ time.ctime() + "] Archivo de subs presente. Dejado en origen= " + re.escape(fichero)
				else:
					subprocess.check_call('rm '+ re.escape(os.path.join(root,fichero)), shell = True)
					print "["+ time.ctime() + "] Archivo DESCARTADO y borrado= " + re.escape(fichero)

	#print("Terminado el bucle de ficheros")		
	borrarDirsVacios() #ojo esta llamada depende de la variable global rutas
	sys.exit()
