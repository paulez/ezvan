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

I18N_SUBSITES = {
    'en': {
        'SITENAME': 'Ezvan homepage',
    }
}

# Feed generation is usually not desired when developing
FEED_ALL_ATOM = None
CATEGORY_FEED_ATOM = None
TRANSLATION_FEED_ATOM = None
AUTHOR_FEED_ATOM = None
AUTHOR_FEED_RSS = None

USE_FOLDER_AS_CATEGORY = True

# Links
PROJECTS_TITLE = "Services"
PROJECTS = [
    {
        "name": "Roundcube",
        "url": "https://www.ezvan.fr/roundcube",
        "description": "Courriel",
    },
    {
        "name": "Nextcloud",
        "url": "https://www.ezvan.fr/nextcloud",
        "description": "Photos",
    },
    {
        "name": "Tiny Tiny RSS",
        "url": "https://www.ezvan.fr/rss/",
        "description": "Lecteur RSS",
    },
    {
        "name": "Agendav",
        "url": "https://www.ezvan.fr/agenda",
        "description": "Agenda",
    },
    {
        "name": "Jappix",
        "url": "https://www.ezvan.fr/jappix/",
        "description": "Messagerie instantanée",
    }
]

# Social widget
SOCIAL = ()

# Plugins
PLUGIN_PATHS = [
    "../../../pelican-plugins"
]
PLUGINS = [
    "i18n_subsites",
    "tipue_search",
    "neighbors",
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
DISPLAY_ARCHIVE_ON_SIDEBAR = False

# Menu
MENUITEMS = ()

# Search
DIRECT_TEMPLATES = ('index', 'tags', 'categories', 'authors', 'archives', 'search')

THEME = "../../../pelican-themes/elegant"

DEFAULT_PAGINATION = 10

READERS = {"html": None}

# Uncomment following line if you want document-relative URLs when developing
#RELATIVE_URLS = True

# Landing page for Elegant theme
LANDING_PAGE_TITLE = "Portail Ezvan.fr"
