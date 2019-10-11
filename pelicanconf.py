#!/usr/bin/env python
# -*- coding: utf-8 -*- #
from __future__ import unicode_literals

AUTHOR = 'Ahmad Al-Shishtawy'
SITENAME = 'Ahmad Al-Shishtawy'
SITESUBTITLE = 'Senior Researcher, PhD'
SITEURL = ''
TIMEZONE = 'Europe/Stockholm'
DEFAULT_LANG = 'en'
THEME = 'mytheme'

PATH = 'content'
STATIC_PATHS = ['images', 'pdfs', 'static']
ARTICLE_EXCLUDES = ['static']
EXTRA_PATH_METADATA = {'images/favicon.ico': {'path': 'favicon.ico'}, }
PAGE_PATHS = ['pages']
PAGE_ORDER_BY = 'menu_order'
INDEX_SAVE_AS = 'blog_index.html'

DISPLAY_CATEGORIES_ON_MENU = False
DEFAULT_PAGINATION = 10
TYPOGRIFY = True

# Menu
#MENUITEMS = (('RISE SICS', 'https://www.sics.se/'),)

GOOGLE_ANALYTICS = 'UA-103785875-1'
GITHUB_URL = 'https://github.com/alshishtawy/alshishtawy.github.io/tree/source'

# Blogroll
LINKS = (('RISE AB', 'https://www.ri.se'),
         ('Computer Systems Lab', 'https://www.sics.se/groups/computer-systems-laboratory-csl'),
         ('My Page @ RISE', 'https://www.ri.se/en/ahmad-al-shishtawy'),
         ('Powered by Pelican', 'http://getpelican.com'))

# Social widget
SOCIAL = (('LinkedIn', 'https://www.linkedin.com/in/alshishtawy'),
          ('Twitter', 'https://twitter.com/alshishtawy'),
          ('Github', 'https://github.com/alshishtawy/'),)

# Twitter Button
TWITTER_USERNAME = 'alshishtawy'

# Feed generation is usually not desired when developing
FEED_ALL_ATOM = None
CATEGORY_FEED_ATOM = None
TRANSLATION_FEED_ATOM = None
AUTHOR_FEED_ATOM = None
AUTHOR_FEED_RSS = None

# Good for debugging
LOAD_CONTENT_CACHE = False

# Uncomment following line if you want document-relative URLs when developing
RELATIVE_URLS = True

# Don't generate Authors page
AUTHOR_SAVE_AS = ''

