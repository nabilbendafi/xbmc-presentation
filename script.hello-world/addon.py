import xbmc
from xbmcgui import Dialog

if __name__ == '__main__':
    #Rock'n'Roll
    # print on XBMC log file
    xbmc.log('Hello world!')
    
    # print on dialog box
    dialog = Dialog()
    dialog.ok('Hello world!', 'Hello world!')
