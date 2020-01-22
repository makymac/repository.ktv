import maintenance
import utils
from variables import*
import sys

###############################################################################
#						                                                  MAIN MENU
############################################################################### 
 
def menu():
    integrate = '[COLOR ff9f9f9f]Link Subs:[/COLOR] Choose your sub'
    remove = '[COLOR ff9f9f9f]Unlink Subs:[/COLOR] Remove your sub'	
    maint = '[COLOR ff9f9f9f]Maintenance:[/COLOR] Maintain device'
    devicelog = '[COLOR ff9f9f9f]System Logs:[/COLOR] Check device logs'
    internet = '[COLOR ff9f9f9f]Speed Test:[/COLOR] ookla Speed Checker'

    option = dialog.select(addonTitle+' Main Menu', [integrate, space, remove, space, maint, space, devicelog, space, internet])

    if option == 0:
	    Integration()
    if option == [1,3,5,7]:
	    menu()
    if option == 2:
	    Remove()	
    if option == 4:
	    Maintain()
    if option == 6:
	    maintenance.logs()
    if option == 8:
	    xbmc.executebuiltin ( 'Runscript("special://home/addons/plugin.video.intervue/ookla.py")' )  


###############################################################################
#						                                                  	INTEGRATE MENU
###############################################################################

def Integration():
    folder = linkaddon+'/sub/'
    view = utils.openURL(folder)
    match=re.compile('<a href="(.*?)">').findall(view)
    notneeded = ['/ivueguide//', 'OFFLINEindex.html']
    files = [] 
    for name in match:
        if not name in notneeded:
            name = re.sub(r'%20', ' ', name)
            name = re.sub(r'.py', '', name)
            files.append(name)
    sub = dialog.select("Subscriptions", files)
    if sub == -1:
        menu()
    else:

        data=[]
        selected = files[sub]
        pathSub = os.path.join(subpath,"%s.py" % selected) 
        if os.path.exists(pathSub):
            os.remove(pathSub)
        zipurl = linkaddon+'/sub/%s.py' % (selected).replace(' ', '%20')
	checkurl = urllib2.urlopen(zipurl).read().splitlines()
	for check in checkurl:
            if check.startswith('addontag'):
                foundStr = check.split('addontag = [')[1].split(']')[0]
		tag = foundStr.replace("'", "")
		data.append(tag)
        found = data[0]
        path = os.path.join(xbmc.translatePath('special://home/addons'), found) 
        if os.path.exists(path):
            dialogProgress.create("SubVue","Starting %s integration" % selected,'Please wait')
            utils.download(zipurl, pathSub, dialogProgress)
            time.sleep(1)
            dialogProgress.close()
            if os.path.exists(subpath + "/%s.py" % selected):
                xbmc.executebuiltin ( 'Runscript("special://profile/addon_data/%s/resources/subs/%s.py")' % (addon_ID,selected))
        else:
            dialog.ok(addonTitle, 'Integration is not available right now', '')
			
###############################################################################
#						                                                  REMOVE MENU
###############################################################################  	
		
def Remove():
    streams = '[COLOR ff9f9f9f]Streams:[/COLOR] Remove subbed streams files'
    xmls = '[COLOR ff9f9f9f]Xmls:[/COLOR] Remove subbed xmls files'	
    logos = '[COLOR ff9f9f9f]Logos:[/COLOR] Remove subbed logo packs'
    categories = '[COLOR ff9f9f9f]Categories:[/COLOR] Remove subbed category files'

    option = dialog.select(addonTitle+ ' Remove Section', [streams, space, xmls, space, logos, space, categories])
    if option == -1:
        menu()
    if option == 0:
	    playlist()
    if option == [1,3,5,]:
	    Remove()
    if option == 2:
	    xml()
    if option == 4:
	    logo()
    if option == 6:
	    cat()

###############################################################################
#						                                                  REMOVE XMLS
###############################################################################  

def xml():
    data = []
    newdata = []
    if os.path.exists(subData):
	xml = open(subData).read()
        matches = re.compile('name="(.*?)".+?url="(.*?)"').findall(xml)
        subbedaddons = {}
            
	for name, value in matches:
            subbedaddons[name] = value
			
        names = sorted(subbedaddons)
        if len(names) > 0: 
            selections = dialog.multiselect(addonTitle+ ' Xmls', names)
            if selections < 0:
                Remove()
            else:
                for selection in selections:
                    sub_name = names[selection]
                    link = subbedaddons[sub_name]
                    if addon_name.getSetting('sub.xmltv') == sub_name:
                        addon_name.setSetting('sub.xmltv', '')
			if addon_name.getSetting('xmltv.type') == '15':
			    addon_name.setSetting('xmltv.type', '')
			    addon_name.setSetting('xmltv.type_select', '')
                    if addon_name.getSetting('sub.xmltv.url') == link:
                        addon_name.setSetting('sub.xmltv.url', '')
                    if os.path.exists(os.path.join(ivuepath,"%s.xml" % sub_name)):
                        os.remove(os.path.join(ivuepath,"%s.xml" % sub_name))
                    data.append(sub_name)
                if os.path.exists(subData):
                    o = open(subData).read().splitlines()
                    for line in o:
                        if not line == '':
                            if not line.split('name="')[1].split('" url')[0] in data:
                                newdata.append(line)
							
                foundxml = sorted(newdata)
                f = open(subData, 'w+')
                for item in foundxml:
                    f.write('%s\n' % item)
                f.close()
                dialog.ok(addonTitle, 'Selected xmls have been removed', '')
                Remove()
        else:
            dialog.ok(addonTitle, 'No xmls were found', '')
            Remove()
			
###############################################################################
#						                                                  REMOVE LOGOS
###############################################################################  
			
def logo():
    data = []
    newdata = []
    if os.path.exists(subLogos):
	xml = open(subLogos).read()
        matches = re.compile('name="(.*?)".+?logo="(.*?)"').findall(xml)
        subbedaddons = {}
            
	for name, value in matches:
            subbedaddons[name] = value
			
        names = sorted(subbedaddons)
        if len(names) > 0: 
            selections = dialog.multiselect(addonTitle+ ' Logos', names)
            if selections < 0:
                Remove()
            else:
                for selection in selections:
                    sub_name = names[selection]
                    if addon_name.getSetting('sub.logos') == sub_name:
                        addon_name.setSetting('logos.source', '0')
                        addon_name.setSetting('sub.logos', '')						
                        addon_name.setSetting('sub.logos.url', '')
                    data.append(sub_name)
                if os.path.exists(subLogos):
                    o = open(subLogos).read().splitlines()
                    for line in o:
                        if not line == '':
                            if not line.split('name="')[1].split('" logo')[0] in data:
                                newdata.append(line)
							
                foundxml = sorted(newdata)
                f = open(subLogos, 'w+')
                for item in foundxml:
                    f.write('%s\n' % item)
                f.close()
                dialog.ok(addonTitle, 'Selected logos have been removed', '')
                Remove()
        else:
            dialog.ok(addonTitle, 'No logos were found', '')
            Remove()
			
###############################################################################
#						                                                  REMOVE CATS
###############################################################################  
			
def cat():	
    data = []		
    ignoreFiles = ["custom.ini", "iVue.ini"]
    for file in os.listdir(catData):
        if not file in ignoreFiles:
            data.append(file.replace('.ini',''))
    names = sorted(data)
	
    if len(names) > 0: 
        selections = dialog.multiselect(addonTitle+ ' Categories', names)
        if selections < 0:
            Remove()
        else:
            for selection in selections:
                sub_name = names[selection]
                if addon_name.getSetting('categories.path') == sub_name:
	            addon_name.setSetting('categories.path', 'iVue')
                try:
                    os.remove(os.path.join(catData,sub_name+'.ini'))
		except:
		    dialog.ok(addonTitle, 'Error Removing ' + sub_name,'','')
	            pass

            dialog.ok(addonTitle, 'Selected category files were removed','')
    else:
        dialog.ok(addonTitle, 'No Categories were found', '')
        Remove()

###############################################################################
#						                                                  REMOVE SUBS
###############################################################################  
		
def playlist():	
    data = []		
    for file in os.listdir(inipath):
        data.append(file.replace('.ini',''))
    names = sorted(data)
	
    if len(names) > 0: 
        selections = dialog.multiselect(addonTitle+ ' Streams', names)
        if selections < 0:
            Remove()
        else:
            for selection in selections:
                sub_name = names[selection]
                try:
                    os.remove(os.path.join(inipath,sub_name+'.ini'))
		except:
		    dialog.ok(addonTitle, 'Error Removing ' + sub_name,'','')
	            pass

            dialog.ok(addonTitle, 'Selected Subscriptions were removed','')
    else:
        dialog.ok(addonTitle, 'No Subscriptions were found', '')
        Remove()
###############################################################################
#						                                                  MAINTENANCE MENU
###############################################################################   

def Maintain():

	if not os.path.exists(packagesdir):
		os.makedirs(packagesdir)

	try:
	        if os.path.exists(cachePath):
		    cacheSize = maintenance.get_size(cachePath)
                else:
		    cacheSize = maintenance.get_size(tempPath)
		packageSize = maintenance.get_size(packagesdir)
		thumbSize    = maintenance.get_size(thumbnails)
	except: pass
	
	try:
		convertCache    = maintenance.convertSize(cacheSize)
		convertPackages = maintenance.convertSize(packageSize)
		convertThumbs    = maintenance.convertSize(thumbSize)
	except: pass

	cache = '[COLOR ff9f9f9f]Clear Cache = [/COLOR]' + str(convertCache)
	packages = '[COLOR ff9f9f9f]Clear Packages = [/COLOR]' + str(convertPackages)
	thumbs = '[COLOR ff9f9f9f]Delete Thumbnails = [/COLOR]' + str(convertThumbs) 

	option = dialog.select(addonTitle+' Maintenace', [cache, space, packages, space, thumbs]) 

	if option < 0:
	    menu() 
	if option == 0:
	    maintenance.clearCache()
	if option == 2:
	    maintenance.clearPackages()
	if option == 4:
	    maintenance.removeThumbs()
	if option == [1,3]:
	    Maintain()



if __name__ == '__main__' :
    menu()
