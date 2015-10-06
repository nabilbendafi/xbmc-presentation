import xbmc
from xbmcaddon import Addon
import pyxbmct.addonwindow as pyxbmct


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


class XRSWindow(pyxbmct.AddonFullWindow):

    """Main application window."""

    def __init__(self, title=''):
        """Constructor."""
        super(XRSWindow, self).__init__(title)
        self.width = 850
        """window width"""
        self.height = 600
        """window width"""
        self.rows = 12
        """grid rows"""
        self.columns = 8
        """grid columns"""
        self.close_button = pyxbmct.Button('Close')
        """close button"""

        self.setGeometry(self.width, self.height, self.rows, self.columns)
        self.draw_layout()
        self.connect_controls()

    def draw_layout(self):
        """Draw elements on the grid."""
        # place the close button on the grid.
        self.placeControl(self.close_button, 11, 3, columnspan=2)

    def connect_controls(self):
        """Register actions."""

        # Connect close button and BACK to close() function.
        self.connect(self.close_button, self.close)
        self.connect(pyxbmct.ACTION_NAV_BACK, self.close)


if __name__ == '__main__':
    # Rock'n'Roll
    window = XRSWindow(title='XBMC RSS Stalker')
    window.show()
    # display window until close() is called
    window.doModal()
    # xbmcgui classes are not grabage-collected, delete manually
    del window
