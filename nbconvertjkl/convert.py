""" The converter workhorse """

import glob
import os
import re
import logging
import sys
import nbformat

from traitlets.config import Config
from nbconvert import HTMLExporter
from shutil import copyfile

logger = logging.getLogger(__name__)

# Setup html exporter template/configs
html_exporter = HTMLExporter()
html_exporter.template_file = 'basic'

def get_body(nb_node):
    """ Get HTML body from notebook and fix links """
    (body, resources) = html_exporter.from_notebook_node(nb_node)
    fixed_body = fix_links(body)
    return fixed_body


def link_repl(matchobj):
    """ Replace src/link matchobj with corrected link """
    print("called repl: {}".format(matchobj.groups()))
    corrected_link = 'src={{{{ "/assets/{}" | relative_url }}}} '.format(matchobj.groups()[0])
    return corrected_link


def fix_links(body):
    """ Find all local asset links and correct """
    asset_dirs = ['figures', 'data', 'images', 'imgs']
    s = '|'.join(asset_dirs)
    regex = re.compile(r'(?:source|src)=\"(\/?(?:%s)\/[\w\d\-_\.]+)\"' % s, re.IGNORECASE)
    fixed_body = re.sub(regex, link_repl, body)
    return fixed_body


def get_nb_info(nb_node):
    """ Return nb info from configs or nothing"""
    nb_info =  "<!--NB_INFO-->" + """<img align="left" width="30" style="padding-right:10px;" src="{{ '/assets/figures/python-logo.png' | relative_url }}"><p style="font-style:italic;font-size:smaller;">This notebook is part of the {{ site.title }}; the content is available <a href="https://github.com/nancynobody/python3_fluency">on GitHub</a>. If you want to launch the notebooks interactively click on the binder stamp below to launch a live notebook server or download the notebooks and run them locally. .</p>"""
    return nb_info or False


def get_nb_title(nb_node):
    """ Get notebook title give a nb_node (json) """

    logging.debug('Getting nb_title: {}'.format(type(nb_node)))

    for cell in nb_node.cells:
        if cell.source.startswith('#'):
            title = cell.source[1:].splitlines()[0].strip()
            cleaned_title = re.sub(r'[^\w\s]', '', title)
            break

    logging.debug('Got title: {}'.format(cleaned_title))
    return cleaned_title or ''


def get_nb_topics(nb_node):
    """ Get notebook topics give a nb_node (json) """

    logging.debug('Getting nb_topics: {}'.format(type(nb_node)))

    regex = r"\*\*Topics\sCovered\*\*([\\n\*\s]+[\w\s]+)+"

    txt_src = nb_node.cells[0].source
    m = re.search(regex, txt_src)

    if len(m.group()) != 0:
        topics = m.group().replace("**Topics Covered**\n* ", "").split("\n* ")
    else: 
        topics = ''

    logging.debug('Got topics: {}'.format(str(topics)))
    return str(topics)


def get_front_matter(nb_node):
    """ Get front matter for Jekyll """

    logging.debug('Getting front_matter: {}'.format(type(nb_node)))

    layout = "notebook"
    title = get_nb_title(nb_node)
    
    # TODO HARDEN - check for special chars in title?
    permalink = title.lower().replace(" ", "-")

    logging.debug('Got permalink: {}'.format(permalink))

    topics = str(get_nb_topics(nb_node))

    logging.debug('Got topics: {}'.format(topics))

    return "---\nlayout: {}\ntitle: {}\npermalink: /{}/\ntopics: {}\n---\n".format(layout, title, permalink, topics)


def get_nb_nav(prev, nxt):
    """ Get html for notebook navigation """

    logging.debug('Getting nb nav: {}, {}'.format(type(prev), type(nxt)))

    nav_comment = '<!-- NAV -->'

    if prev == None:
        prev_nb = ''
    else:
        prev_title = get_nb_title(prev)
        prev_link = prev_title.lower().replace(" ", "-")
        prev_nb = '&lt; <a href="{{{{ "{}" | relative_url }}}}">{}</a> | '.format(prev_link, prev_title)

    logging.debug('Got prev_nb: {}'.format(prev_nb))

    contents = '<a href="/ipynb_template_site/">Contents</a>'

    if nxt == None:
        nxt_nb = ''
    else:
        nxt_title = get_nb_title(nxt)
        nxt_link = nxt_title.lower().replace(" ", "-")
        nxt_nb = ' | <a href="{{{{ "{}" | relative_url }}}}">{}</a> &gt;'.format(nxt_link, nxt_title)
    
    logging.debug('Got nxt_nb: {}'.format(nxt_nb))

    nb_nav = '{}<p style="font-style:italic;font-size:smaller;">{}{}{}</p>'.format(nav_comment, prev_nb, contents, nxt_nb)
    return nb_nav


def get_nb_files(nbs=None):
    """ Get sorted list of nb files from nb_dir """

    logger.debug("Getting notebook files: {}".format(nbs))

    nb_files = glob.glob(nbs)
    nb_files.sort()
    logger.debug("Found nb_files: {}".format(nb_files))

    return nb_files