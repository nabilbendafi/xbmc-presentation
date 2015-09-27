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

    # fetch username setting
    username = addon.getSetting('username')

    # fetch 'hello' localized string
    hello = addon.getLocalizedString(32000)

    # print on dialog box
    dialog = Dialog()
    dialog.ok('%s %s!' % (hello, username), description)

    # fetch timeout setting
    timeout = float(addon.getSetting('timeout'))

    # print on notification box
    dialog.notification('%s %s!' % (hello, username),
                        description, time=int(timeout))
