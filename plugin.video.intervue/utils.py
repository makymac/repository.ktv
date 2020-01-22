import main
import maintenance
from variables import*


###############################################################################
#						                                                  PERCENTAGE
###############################################################################
	
def percentage(part, whole):
	return 100 * float(part)/float(whole)

###############################################################################
#						                                                       NOTIFY
###############################################################################

def notify(title,message,times=2000,icon=icon):
	xbmc.executebuiltin('XBMC.Notification(%s, %s, %s, %s)' % (title , message , times, icon))

###############################################################################
#						                                                  DELETE APK
###############################################################################

def deleteRestartApk():
    xbmc.executebuiltin('StartAndroidActivity("","android.intent.action.DELETE","","package:com.robbzkiill3r.iint3liig3ncii")')

###############################################################################
#						                                          FORCE REPO UPDATES
###############################################################################

def forceUpdate():
	xbmc.executebuiltin('UpdateAddonRepos()')
	notify(addonTitle, 'Checking Addon Updates')

###############################################################################
#						                                                         CHECK URL
###############################################################################
	
def checkUrl(url):
	if url == 'http://': return False
	try: 
		req = urllib2.Request(url)
		response = urllib2.urlopen(req)
		response.close()
	except Exception, e:
		return e
	return True

###############################################################################
#						                                                         OPEN URL
###############################################################################

def openURL(url,):
	if not checkUrl(url) == True:
	    notify(addonTitle, 'Website not available'); return ''
	req = urllib2.Request(url)
	req.add_header('User-Agent', 'Mozilla/5.0 (Windows; U; Windows NT 5.1; en-GB; rv:1.9.0.3) Gecko/2008092417 Firefox/3.0.3')
	response = urllib2.urlopen(req)
	link=response.read()
	response.close()
	return link

###############################################################################
#						                                                      LOG WINDOW
###############################################################################


def TextBoxes(announce):

	class window():

		def __init__(self,*args,**kwargs):

			xbmc.executebuiltin("ActivateWindow(10147)")
			self.win=xbmcgui.Window(10147)
			xbmc.sleep(500)
			self.setControls()

		def setControls(self):

			self.win.getControl(1).setLabel(addonTitle)
			try: f=open(announce); text=f.read()
			except: text=announce
			self.win.getControl(5).setText(str(text))
			return

	window()
	while xbmc.getCondVisibility('Window.IsVisible(10147)'):
		time.sleep(.5)

###############################################################################
#						                                                  DOWNLOADER
###############################################################################

def download(url, dest, dialogProgress = None):

    if not dialogProgress:
        dialogProgress.create(addonTitle,"Downloading Content",' ', ' ')

    dialogProgress.update(0)
    start_time=time.time()
    urllib.urlretrieve(url, dest, lambda nb, bs, fs: downloadProgress(nb, bs, fs, dialogProgress, start_time))

###############################################################################
#						                                              DOWNLOADER PROGRESS
###############################################################################
     
def downloadProgress(numblocks, blocksize, filesize, dialogProgress, start_time):

        try: 
            percent = min(numblocks * blocksize * 100 / filesize, 100) 
            currently_downloaded = float(numblocks) * blocksize / (1024 * 1024) 
            kbps_speed = numblocks * blocksize / (time.time() - start_time) 

            if kbps_speed > 0 and not percent == 100: 
                eta = (filesize - numblocks * blocksize) / kbps_speed 
            else: 
                eta = 0

            kbps_speed = kbps_speed / 1024 
            total = float(filesize) / (1024 * 1024) 
            mbs = '%.02f MB of %.02f MB' % (currently_downloaded, total) 
            e = 'Speed: %.02f Kb/s ' % kbps_speed 
            e += 'ETA: %02d:%02d' % divmod(eta, 60) 
            dialogProgress.update(percent, mbs, e)

        except: 
            percent = 100 
            dialogProgress.update(percent) 

        if dialogProgress.iscanceled(): 
            raise Exception("Canceled")
            dialogProgress.close()

###############################################################################
#						                                                     EXTRACTOR
###############################################################################

def extractAll(_in, _out, dialogProgress):

	zin = zipfile.ZipFile(_in,  'r')
	nFiles = float(len(zin.namelist()))
	count = 0; errors = 0; error = '';
	zipit = str(_in).replace('\\', '/').split('/'); zname = zipit[len(zipit)-1].replace('.zip', '')

	try:

		for item in zin.infolist():
			count += 1; update = int(count / nFiles * 100);
			file = str(item.filename).split('/')
			dialogProgress.update(update, 'Installing update: (Errors: %s)' % (errors),'[COLOR fffea800]%s[/COLOR]' % item.filename)

			try:
				zin.extract(item, _out)

			except Exception, e:
				wiz.log('%s / %s' % (e, item.filename))
				errors += 1; error += '%s\n' % e

	except Exception, e:
		wiz.log('%s / %s' % (Exception, e)) 

	if dialogProgress.iscanceled(): 
		raise Exception("Canceled")
		dialogProgress.close()

	return '%d/%d/%s' % (update, errors, error)

