import xbmc, xbmcaddon, xbmcgui, xbmcplugin, os, sys, xbmcvfs, glob, zipfile
import shutil
import urllib2,urllib
import re
import time
import datetime
from datetime import date, datetime, timedelta
from sqlite3 import dbapi2 as database



###############################################################################
#						                                                  XBMC ARGUMENTS
###############################################################################

dialog = xbmcgui.Dialog()
dialogProgress  = xbmcgui.DialogProgress()
space = '[COLOR ffa8a8a8][B]-------------------------------------------------[/B][/COLOR]'

###############################################################################
#						                                                  GLOBAL PATHS
###############################################################################
addonID = 'script.ivueguide'
addon_name = xbmcaddon.Addon(addonID)
linkaddon = addon_name.getSetting('userurl')
addon_ID       = 'plugin.video.intervue'
addonTitle     = 'InterVUE'
addon          = xbmcaddon.Addon(addon_ID)
home           = xbmc.translatePath('special://home/')
profile       = xbmc.translatePath('special://profile/')
addons       = os.path.join(home, 'addons')
userData       = os.path.join(home, 'userdata')
addonData      = os.path.join(userData, 'addon_data', addon_ID)
inipath = xbmc.translatePath(os.path.join('special://profile', 'addon_data', addon_ID, 'resources', 'ini'))
subpath = xbmc.translatePath(os.path.join('special://profile', 'addon_data', addon_ID, 'resources', 'subs'))
ivuepath = xbmc.translatePath(os.path.join('special://profile', 'addon_data', addonID))
subData = xbmc.translatePath('special://profile/addon_data/script.ivueguide/resources/config/Data.txt')
subLogos = xbmc.translatePath('special://profile/addon_data/script.ivueguide/resources/config/Logo.txt')
catData = xbmc.translatePath('special://profile/addon_data/script.ivueguide/resources/categories/')	
packagesdir    =  xbmc.translatePath(os.path.join('special://home/addons/packages',''))
thumbnails    =  xbmc.translatePath('special://home/userdata/Thumbnails')
cachePath = os.path.join(home, 'cache')
tempPath = xbmc.translatePath('special://temp')
textures  = xbmc.translatePath('special://home/userdata/Database/Textures13.db')
kodilog = xbmc.translatePath('special://logpath/kodi.log')
kodiold = xbmc.translatePath('special://logpath/kodi.old.log')
icon = xbmc.translatePath(os.path.join('special://home/addons/', addon_ID, 'icon.png'))

if not os.path.exists(subpath):
    os.makedirs(subpath)
if not os.path.exists(inipath):
    os.makedirs(inipath)


