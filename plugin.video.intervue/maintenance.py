import utils
from variables import*

def removeThumbs():

    if os.path.exists(thumbnails)==True:  

        try:
            shutil.rmtree(thumbnails)
        except:
            dialog.ok(addonTitle, 'Error removing thumbnails folder','')
        try:
            os.remove(textures)
        except:
            dialog.ok(addonTitle, 'Error removing textures.db file','')

        if not os.path.exists(thumbnails):
            dialog.ok(addonTitle, 'Thumbnails were successfully removed','Please restart kodi')

    else:
        dialog.ok(addonTitle, 'Thumbnails folder not found','')

def clearPackages(over=None):

	if os.path.exists(packagesdir):

		try:	
			shutil.rmtree(packagesdir)
		except: 
			utils.notify(addonTitle,'Clear Packages: [COLOR red]Error[/COLOR]!')

		if not os.path.exists(packagesdir):
			utils.notify(addonTitle,'Clear Packages: [COLOR green]Success[/COLOR]!')

	else: 
		utils.notify(addonTitle,'Clear Packages: [COLOR red]None Found![/COLOR]')
 


 
def clearCache():
	cachelist = [
		(addonData),
		(os.path.join(home,'cache')),
		(os.path.join(home,'temp')),
		(os.path.join(addonData,'plugin.video.itv','Images'))]
		
	delfiles = 0

	for item in cachelist:

		if os.path.exists(item) and not item in [addonData]:
			for root, dirs, files in os.walk(item):

				file_count = 0
				file_count += len(files)

				if file_count > 0:
					for f in files:
						if not f in ['kodi.log', 'xbmc.log']:
							try:
								os.unlink(os.path.join(root, f))
							except:
								pass

					for d in dirs:
						try:
							shutil.rmtree(os.path.join(root, d))
							delfiles += 1
						except:
							pass

		else:
			for root, dirs, files in os.walk(item):
				for d in dirs:
					if 'cache' in d.lower():

						try:
							shutil.rmtree(os.path.join(root, d))
							delfiles += 1
                                                except:
						        pass


	utils.notify(addonTitle,'Clear Cache: Removed %s Files' % delfiles)


def viewLogFile():
			
	if os.path.exists(kodilog):
		if os.path.exists(kodilog) and os.path.exists(kodiold):
			option = dialog.yesno(addonTitle,"Which log would you like to view?","","Current or Old", yeslabel='[B]OLD[/B]',nolabel='[B]CURRENT[/B]')
			if option == 0:
				f = open(kodilog,mode='r'); msg = f.read(); f.close()
				utils.TextBoxes("%s - kodi.log" % msg)
			else:
				f = open(kodiold,mode='r'); msg = f.read(); f.close()
				utils.TextBoxes("%s - kodi.old.log" % msg)
		else:
			f = open(kodilog,mode='r'); msg = f.read(); f.close()
			utils.TextBoxes("%s - kodi.log" % msg)		
			
	if os.path.isfile(kodilog):
		return True
	else:
		dialog.ok(addonTitle,'No log file was found.','','[COLOR ff9f9f9f]Thank you for using iVue Wizard[/COLOR]')
		logs()

def view_LastError():

	found = 0

	if os.path.exists(xbmc.translatePath('special://logpath/')):
		openlog=open(kodilog).read()	
		scanlog=openlog.replace('\n','NEW_L').replace('\r','NEW_R')
		match = re.compile('EXCEPTION Thrown(.+?)End of Python script error report').findall(scanlog)
		for checker in match:
			found = 1
			founderror = "[B][COLOR red]THE LAST ERROR IN YOUR LOG WAS:[/B][/COLOR]\n\n" + checker + '\n'
		if found == 0:
			dialog.ok(addonTitle,'No errors were found in your log.')
		else:
			c=founderror.replace('NEW_L','\n').replace('NEW_R','\r')
			utils.TextBoxes("%s" % c)

	else:
		dialog.ok(addonTitle,'No log file was found on your system','','[COLOR ff9f9f9f]Thank you for using iVue Wizard[/COLOR]')
		logs()

def logs():
	founderrors = 0

	if os.path.exists(xbmc.translatePath('special://logpath/')):
		openlog=open(kodilog).read()	
		scanlog=openlog.replace('\n','NEW_L').replace('\r','NEW_R')
		match = re.compile('EXCEPTION Thrown(.+?)End of Python script error report').findall(scanlog)
		for checker in match:
			founderrors = founderrors + 1
	
	if founderrors == 0:
		errorslogged = "[COLOR ff9f9f9f]View Errors Only:[/COLOR] Errors found: [COLOR ffffffff]0[/COLOR]"
	else:
		errorslogged = "[COLOR ff9f9f9f]View Errors Only:[/COLOR] Errors found: [COLOR ff9f9f9f]" + str(founderrors) + "[/COLOR]"


	resp = dialog.select(addonTitle+' [COLOR ff9f9f9f]XBMC Logs[/COLOR]', [errorslogged, space, '[COLOR ff9f9f9f]View Full logs:[/COLOR] Current or old logs']) 
	if resp < 0:
	    return
	if resp == 0:
	    view_LastError()
	if resp == 1:
	    logs()
	if resp == 2:
	    viewLogFile()

def get_size(start_path):
	total_size = 0
	for dirpath, dirnames, filenames in os.walk(start_path):
		for f in filenames:
			fp = os.path.join(dirpath, f)
			total_size += os.path.getsize(fp)
	return total_size

def convertSize(size):
   import math
   if (size == 0):
	   return '0 MB'
   size_name = ("B", "KB", "MB", "GB", "TB", "PB", "EB", "ZB", "YB")
   i = int(math.floor(math.log(size,1024)))
   p = math.pow(1024,i)
   s = round(size/p,2)
   if size_name[i] == "B":
		return '[COLOR lime]%s %s' % (s,size_name[i]) + '[/COLOR]'
   if size_name[i] == "KB":
		return '%s %s' % (s,size_name[i])
   if size_name[i] == "GB":
		return '[COLOR red]%s %s' % (s,size_name[i]) + '[/COLOR]'
   if size_name[i] == "TB":
		return '[COLOR red]%s %s' % (s,size_name[i]) + '[/COLOR]'
   if s < 50:
		return '%s %s' % (s,size_name[i])
   if s >= 50:
		if s < 100:
			return '[COLOR yellow]%s %s' % (s,size_name[i]) + '[/COLOR]'
   if s >= 100:
		return '[COLOR red]%s %s' % (s,size_name[i]) + '[/COLOR]'


