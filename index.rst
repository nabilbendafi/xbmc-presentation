XBMC
=====

**An extensible media center**

*Nabil BENDAFI - November 2015*

nabil@bendafi.fr

https://github.com/nabilbendafi

History
=======

* 2003/12/13:  XBMP -> XBMC
* 2004/06/29:  1st stable release of XBMC (XboxMediaCenter 1.0.0)
* 2010/05/27:  XBMC4Xbox dev splitted
* 2014/08/01:  Name change to become KODI

(source: Wikipedia)

Multi-platform
==============
* Linux
* Mac OS X
* Windows
* Android
* iOS

.. class:: fragment

Open Source

.. class:: fragment

Boxee, GeeXboX, OpenELEC, Plex, XBian, XBMC4Xbox ...

add-on
======
.. class:: fragment

Script

.. class:: fragment

Plugin

.. class:: fragment

   ... all in Python !


To do what ?
=================

.. csv-table:: 
   :header: "Add-on type", "Media type"
   :widths: 50, 50

   "plugin", "audio"
   "plugin", "video"
   "plugin", "picture"
   "plugin", "weather"
   "script", "module"
   "script", "service"

API
===

.. csv-table:: API XBMC
   :header: "module", "description"
   :widths: 20, 50

   "xbmc", "Handles media (image/audio/video) (ex. stop, start, keyboard...)"
   "xbmcgui", "Graphical user interface (ex. windows, dialog boxes, widgets...)"
   "xbmcplugin", "Structures menus"
   "xbmcaddon", "Add-on settings"
   "xbmcvfs", "Virtual filesystem abstraction amoung platform"

Python-docs_

.. _Python-docs: http://mirrors.kodi.tv/docs/python-docs/

Hello
=====

.. class:: prettyprint lang-python

::

    import xbmc
    xbmc.log('Hello world!')

Frameworks
==========

PyXBMCt_

.. _PyXBMCt: http://romanvm.github.io/PyXBMCt/docs/

xbmcswift2_

.. _xbmcswift2: http://xbmcswift2.readthedocs.org/
  
PyXBMCt
=======

A Python framework for simple creating UI for XBMC addons.

https://github.com/romanvm

.. class:: fragment

* Inspired by PyQt
* Container classes for UI elements
* Widgets
* Grid layout 
* Event connection manager


XRS
===

An example of RSS feed reader

xbmcswift2
==========

A micro-framework for creating XBMC plugins.

xbmc@jonathanbeluch.com

.. class:: fragment

Makes creating and testing easier ...

.. class:: fragment

... with command line enabled interface

.. class:: fragment

.. class:: prettyprint c

::

   $ xbmcswift2 create
   $ xbmcswift2 [once|interactive|crawl] [url]

.. class:: fragment

* URL routing
* Caching
* Storage

animeseed
=========

* xbmcswift2
* mechanize
* BeautifulSoup

Debug
=====

Python ♥ PyDev

Use **same** pydev version on both sides

* Eclipse 
* XBMC

Tools
=====
* vim, Eclipse or your favorites IDE
* rst2html5

:: 

    XBMC
    =====
    
    **An extensible media center**
    
    *Nabil BENDAFI - November 2015*
    
    nabil@bendafi.fr
    https://github.com/nabilbendafi

.. class:: prettyprint lang-html

::

    <body class="reveal">
      <div class="slides">
        <section id="xbmc">
          <header><h2>XBMC</h2></header>
          <p><strong>An extensible media center</strong></p>
          <p><em>Nabil BENDAFI - November 2015</em></p>
          <p><a class="reference external" href="mailto:nabil@bendafi.fr">nabil@bendafi.fr</a></p>
          <p><a class="reference external" href="https://github.com/nabilbendafi">https://github.com/nabilbendafi</a></p>
        </section>

Presentation slides generated with rst2html5
https://github.com/marianoguerra/rst2html5

resources
==========
http://mirrors.kodi.tv/docs/python-docs/
http://kodi.wiki/view/Python_development
http://romanvm.github.io/PyXBMCt/docs/
http://xbmcswift2.readthedocs.org/
https://github.com/marianoguerra/rst2html5

and many more ...

Thanks !
========
