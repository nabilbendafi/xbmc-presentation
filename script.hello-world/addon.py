import xbmc
from xbmcgui import Dialog
from xbmcaddon import Addon

if __name__ == '__main__':
    #Rock'n'Roll
    # print on XBMC log file
    xbmc.log('Hello world!')
    
    # fetch add-on description
    addon = Addon()
    description = addon.getAddonInfo('description')

    # print on dialog box
    dialog = Dialog()
    dialog.ok('Hello world!', description)
