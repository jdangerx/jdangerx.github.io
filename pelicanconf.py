#!/usr/bin/env python
# -*- coding: utf-8 -*- #
from __future__ import unicode_literals

AUTHOR = u'John Xia'
SITENAME = u'No Promises'
SITEURL = 'http://www.johnxia.me/blog'

TIMEZONE = 'America/Chicago'

DEFAULT_LANG = u'en'

# Feed generation is usually not desired when developing
FEED_ALL_RSS = "feeds/rss.xml"
CATEGORY_FEED_ATOM = None
TRANSLATION_FEED_ATOM = None
MENUITEMS = [("Projects", "/index.html"), ("Articles", "/archives.html"),
             ("About", "/pages/about.html")]
DISPLAY_PAGES_ON_MENU = False
DISPLAY_CATEGORIES_ON_MENU = False

# Blogroll
# LINKS = (('Studio Xia', 'http://www.studioxia.com/'),)


# Social widget
# SOCIAL = (('You can add links in your config file', '#'),
          # ('Another social link', '#'),)

DEFAULT_PAGINATION = 10
STATIC_PATHS = ['/home/john/blog/content/images']
# Uncomment following line if you want document-relative URLs when developing
# RELATIVE_URLS = True

THEME = "themes/dimple"
READERS = {'html': None}
