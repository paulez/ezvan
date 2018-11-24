#!/usr/bin/env python
# -*- coding: utf-8 -*- #
from __future__ import unicode_literals

AUTHOR = 'Paul Ezvan'
SITENAME = 'Portail Ezvan'
SITEURL = ''

PATH = 'content'

TIMEZONE = 'Europe/Paris'

DEFAULT_LANG = 'fr'
LOCALE = 'fr_FR.utf8'

# Feed generation is usually not desired when developing
FEED_ALL_ATOM = None
CATEGORY_FEED_ATOM = None
TRANSLATION_FEED_ATOM = None
AUTHOR_FEED_ATOM = None
AUTHOR_FEED_RSS = None

USE_FOLDER_AS_CATEGORY = True

# Blogroll
LINKS = (
    ("Roundcube", "https://www.ezvan.fr/roundcube"),
    ("Photos", "https://www.ezvan.fr/nextcloud"),
    ("Lecteur RSS", "https://www.ezvan.fr/rss/"),
    ("Agenda", "https://www.ezvan.fr/agenda"),
    ("Messagerie instantannée", "https://www.ezvan.fr/jappix/"),
)

# Social widget
SOCIAL = ()

# Plugins
PLUGIN_PATHS = [
    "/home/paul/data/logiciels/pelican-plugins"
]
PLUGINS = [
    'i18n_subsites', 
    'tipue_search',
]
JINJA_ENVIRONMENT = {
    'extensions': ['jinja2.ext.i18n'],
}
BOOTSTRAP_THEME = "united"
I18N_TEMPLATES_LANG = "ti"

DISPLAY_ARTICLE_INFO_ON_INDEX = False
SHOW_ARTICLE_AUTHOR = True
SHOW_DATE_MODIFIED = True
SHOW_ARTICLE_CATEGORY = False
DISPLAY_AUTHORS_ON_SIDEBAR = True

# Archives
ARCHIVES_SAVE_AS = 'archives.html'

# Menu
MENUITEMS = ()

# Search
DIRECT_TEMPLATES = ('index', 'categories', 'authors', 'archives', 'search')

THEME = "/home/paul/data/logiciels/pelican-themes/pelican-bootstrap3"

DEFAULT_PAGINATION = 10

# Uncomment following line if you want document-relative URLs when developing
#RELATIVE_URLS = True