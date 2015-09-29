import xbmc
from xbmcgui import Dialog
from xbmcaddon import Addon


addon = Addon()
debug = addon.getSetting('debug') == 'true'
debug_host = addon.getSetting('debug_host')
debug_port = int(addon.getSetting('debug_port'))
# Remote debugger using Eclipse and Pydev
if debug:
    try:
        import pydevd
        pydevd.settrace(host=debug_host, port=debug_port,
                        stdoutToServer=True, stderrToServer=True)
        xbmc.log('Pydev started!')
    except ImportError:
        xbmc.log('Pydev not found!', xbmc.LOGERROR)
    except:
        xbmc.log('Couldn\'t attach Pydev!', xbmc.LOGERROR)


if __name__ == '__main__':
    #Rock'n'Roll
    pass
