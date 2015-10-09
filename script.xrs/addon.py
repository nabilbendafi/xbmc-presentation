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

    def __new__(cls, name='Sam & Max', url='http://sametmax.com/feed/', *args, **kwargs):
        """Constructor."""
        feed = pyxbmct.List.__new__(cls, *args, **kwargs)

        feed.name = name
        """feed's name"""
        feed.namespace = ''
        """feed's namespace"""
        feed.url = url
        """feed's url"""
        feed.articles = []
        """feed's articles"""
        feed.raw = ''
        """feed's raw XML stream"""

        return feed

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
        self.feeds = []
        """RSS feeds"""
        self.current_feed = None
        """current RSS feed"""
        self.close_button = pyxbmct.Button('Close')
        """close button"""

        self.setGeometry(self.width, self.height, self.rows, self.columns)
        self.source_feeds()
        self.draw_layout()
        self.connect_controls()
        self.set_navigation()

    def _activated(self, feed):
        """Open selected feed's article in webbrowser."""
        if feed == self.current_feed:
            # Change title font
            link = feed.read_article().link
            if link:
                # Opent link in the browser
                webbrowser.open(link)

    def draw_layout(self):
        """Draw elements on the grid."""
        # place the close button on the grid.
        try:
            self.placeControl(self.close_button, 11, 3, columnspan=2)
        except:
            # control aready exists
            pass

        # place the feeds on the grid.
        if self.current_feed:
            self.placeControl(self.current_feed, 0, 0,
                              columnspan=self.columns, rowspan=self.rows - 1)

            self.current_feed.update()

            if self.current_feed.size():
                self.setFocus(self.current_feed)
            else:
                self.setFocus(self.close_button)
        else:
            self.setFocus(self.close_button)

    def onAction(self, action):
        """Handle control action.

        :param: action Action received by this window. 
        """
        # feed navigation: left, right
        if action in [pyxbmct.ACTION_MOVE_LEFT, pyxbmct.ACTION_MOVE_RIGHT]:
            if len(self.feeds)-1:
                index = self.feeds.index(self.current_feed)
                prev_index = (index-1) % len(self.feeds)
                next_index = (index+1) % len(self.feeds)
            else:
                prev_index = next_index = 0

            # hide current feed
            self.removeControl(self.current_feed)
            self.current_feed.setVisible(False)
            # disconnect it
            self.disconnect(self.current_feed)

            if action == pyxbmct.ACTION_MOVE_LEFT:
                self.current_feed = self.feeds[prev_index]
            if action == pyxbmct.ACTION_MOVE_RIGHT:
                self.current_feed = self.feeds[next_index]

            # redraw
            self.draw_layout()
            # reconnect
            self.connect_controls()
            self.set_navigation()
        else:
            # call super method
            super(XRSWindow, self).onAction(action)
        
    def connect_controls(self):
        """Register actions."""
        # connect feed's article to webbrowser function
        if self.current_feed:
            self.connect(self.current_feed,
                         lambda: self._activated(self.current_feed))

        # connect close button and BACK to close() function.
        self.connect(self.close_button, self.close)
        self.connect(pyxbmct.ACTION_NAV_BACK, self.close)

    def set_navigation(self):
        """Define navigation between feed elements."""
        # feed navigation: up, down
        self.current_feed.controlUp(self.close_button)
        self.current_feed.controlDown(self.close_button)

        # close_button navigation: up, down, right and left
        self.close_button.setNavigation(self.current_feed, self.current_feed,
                                        self.close_button, self.close_button)

    def source_feeds(self):
        """Source RSS feed source from file."""
        filename = xbmc.translatePath(addon.getSetting('rss_feed_file'))
        try:
            f = open(filename)

            # parse RSS feed sources file
            xml = ElementTree.fromstring(f.read())
            for feed_elem in xml.iter('feed'):
                # create a feed for each entry
                feed = Feed(url=feed_elem.text)
                self.feeds.append(feed)
                self.current_feed = feed

            f.close()
        except:
            xbmc.log('Couldn\'t open %s file!' % filename,
                     xbmc.LOGERROR)
            # fallback
            feed = Feed()
            self.current_feed = feed
            self.feeds.append(feed)


if __name__ == '__main__':
    # Rock'n'Roll
    window = XRSWindow(title='XBMC RSS Stalker')
    window.show()
    # display window until close() is called
    window.doModal()
    # xbmcgui classes are not grabage-collected, delete manually
    del window
