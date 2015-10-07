import re
import urllib
import webbrowser
from xml.etree import ElementTree

import xbmc
from xbmcaddon import Addon
import xbmcgui
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


class Article(xbmcgui.ListItem):

    """Abstracts a feed article."""

    def __new__(cls, feed, tag, *args, **kwargs):
        """Constructor."""
        article = xbmcgui.ListItem.__new__(cls, *args, **kwargs)

        article.feed = feed
        """article's parent feed"""
        article.title = ''
        """article's title"""
        article.link = ''
        """article's link"""
        article.description = ''
        """article's description"""
        article.guid = ''
        """article's guid"""
        article.tag = tag
        """article's tag"""

        # title
        title = tag.find(article.feed.namespace + 'title').text
        article.title = '[B]' + title.strip() + '[/B]' if title else ''
        # label is needed by lower level xbmcgui.ListItem
        article.setLabel(article.title)

        # link
        link_tag = tag.find(article.feed.namespace + 'link')
        article.link = link_tag.attrib.get('href') or link_tag.text

        # description
        for name in ('description', 'summary', 'content'):
            desc_tag = tag.find(article.feed.namespace + name)
            if desc_tag is not None and (desc_tag.text or len(desc_tag)):
                article.description = (desc_tag.text or ElementTree.tostring(
                    desc_tag[0], encoding='unicode'))

        # guid
        for name in ('id', 'guid', 'link'):
            guid_tag = tag.find(article.feed.namespace + name)
            if guid_tag is not None and guid_tag.text:
                article.guid = guid_tag.text
                break

        return article

    def update_status(self, read=True):
        """Update article status
        Toggle bold font

        :param: read Status of the article
        """
        if read:
            self.title = self.title.replace('[B]', '').replace('[/B]', '')
        else:
            self.title = '[B]' + self.title + '[/B]'
        self.setLabel(self.title)

    @property
    def read(self):
        return re.match('^\[B\]', self.title)


class Feed(pyxbmct.List):

    """Abstracts a RSS feed."""

    def __init__(self, name='Sam & Max', url='http://sametmax.com/feed/'):
        """Constructor."""
        super(Feed, self).__init__()
        self.name = name
        """feed's name"""
        self.namespace = ''
        """feed's namespace"""
        self.url = url
        """feed's url"""
        self.articles = []
        """feed's articles"""
        self.raw = ''
        """feed's raw XML stream"""

    def update(self):
        """Refresh RSS feed content."""
        try:
            self.raw = urllib.urlopen(self.url).read()
        except:
            xbmc.log('Couldn\'t fetch %s data from %s !' %
                     (self.name, self.url), xbmc.LOGERROR)
        # parse raw data
        xml = ElementTree.fromstring(self.raw)
        self.namespace = (re.findall('\{.*\}', xml.tag) or ['']).pop()
        self.articles = [
            Article(self, tag) for tag_name in ('item', 'entry')
            for tag in xml.iter(self.namespace + tag_name)]

        # append articles to feed
        self.addItems(self.articles)

    def read_article(self):
        """Retrieve the selected article from the list

        :returns: article to read
        """
        selected_item = super(Feed, self).getSelectedPosition()
        if selected_item != -1:
            article = self.articles[selected_item]
            article.update_status()
            return article
        return None


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
        self.feed = Feed()
        """RSS feed"""
        self.close_button = pyxbmct.Button('Close')
        """close button"""

        self.setGeometry(self.width, self.height, self.rows, self.columns)
        self.draw_layout()
        self.connect_controls()

    def _activated(self):
        """Open selected feed's article in webbrowser."""
        link = self.feed.read_article().link
        if link:
            webbrowser.open(link)

    def draw_layout(self):
        """Draw elements on the grid."""
        # place the close button on the grid.
        self.placeControl(self.close_button, 11, 3, columnspan=2)
        # place the feed on the grid.
        self.placeControl(self.feed, 0, 0,
                          columnspan=self.columns, rowspan=self.rows - 1)

        if self.feed.size():
            self.setFocus(self.feed)
        else:
            self.setFocus(self.close_button)

        self.feed.update()

    def connect_controls(self):
        """Register actions."""
        # Connect feed's article to webbrowser function
        self.connect(self.feed, self._activated)

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
