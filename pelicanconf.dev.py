#!/usr/bin/env python
# -*- coding: utf-8 -*- #

from pelican_jupyter import markup as nb_markup

AUTHOR = 'Python Granada Org'
SITENAME = 'Python Granada'
SITEURL = ''

PATH = 'content'

THEME = "themes/buruma"
TIMEZONE = 'Europe/Madrid'
DEFAULT_LANG = 'es'

# Feed generation is usually not desired when developing
FEED_ALL_ATOM = None
CATEGORY_FEED_ATOM = None
TRANSLATION_FEED_ATOM = None
AUTHOR_FEED_ATOM = None
AUTHOR_FEED_RSS = None

MARKUP = ("md", "ipynb")
IGNORE_FILES = [".ipynb_checkpoints"]

PLUGIN_PATHS = ["plugins"]


LIQUID_TAGS = []
PLUGINS = ["i18n_subsites", "assets", nb_markup]


IPYNB_FIX_CSS = True
IPYNB_SKIP_CSS = False
IPYNB_STOP_SUMMARY_TAGS = [('div', ('class', 'input')), ('div', ('class', 'output')), ('h2', ('id', 'Header-2'))]
IPYNB_GENERATE_SUMMARY = True


JINJA_ENVIRONMENT = {
    "extensions": ["jinja2.ext.i18n"],
}

LIQUID_CONFIGS = (("IPYNB_EXPORT_TEMPLATE", "notebook.tpl", ""), )



# Blogroll
LINKS = (('Pelican', 'https://getpelican.com/'),
         ('Python.org', 'https://www.python.org/'),
         ('Jinja2', 'https://palletsprojects.com/p/jinja/'),
         ('You can modify those links in your config file', '#'),)

# Social widget
SOCIAL = (('You can add links in your config file', '#'),
          ('Another social link', '#'),)

DEFAULT_PAGINATION = False
SITEURL=""

# Theme config
MENUITEMS_NAVBAR = (("Asociación", f"{SITEURL}/pages/about.html"),("Código de Conducta", f"{SITEURL}/pages/coc.html"), ("COVID-19", f"{SITEURL}/pages/covid-19.html"),)
NAVBAR_STYLE = "is-primary"
THEME_LOGO = f"{SITEURL}/theme/images/logo_grande.svg"
FOOTER= "Made with ❤️ using Python from Granada. Under construction 🚧"

