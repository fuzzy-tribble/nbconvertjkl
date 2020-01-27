"""Global configuration handling."""

import logging
import os
from pathlib import Path

logger = logging.getLogger(__name__)

#TODO consider moving nb_info to _config.yml

DEFAULT_CONFIG = {
    "nbs": os.path.join(os.path.dirname(__file__), '../../notebooks/*.ipynb'),
    "nb_read_path": os.path.join(os.path.dirname(__file__), '../../notebooks/'),
    "nb_write_path": os.path.join(os.path.dirname(__file__), '../../docs/_notebooks/'),
    "asset_write_path": os.path.join(os.path.dirname(__file__), '../../docs/assets/'),
    "asset_subdirs": ['figures', 'data', 'images', 'imgs', 'img'],
    "nb_info": "<!--NB_INFO-->" + """<img align="left" width="30" style="padding-right:10px;" src="{{ '/assets/figures/python-logo.png' | relative_url }}"><p style="font-style:italic;font-size:smaller;">This notebook is part of the {{ site.title }}; the content is available <a href="https://github.com/nancynobody/python3_fluency">on GitHub</a>. If you want to launch the notebooks interactively click on the binder stamp below to launch a live notebook server or download the notebooks and run them locally. .</p>""",
    "nb_nav": True,
}


def get_config():
    """Retrieve the config from the specified path, returning a config dict."""
    #TODO
    config_dict = DEFAULT_CONFIG
    return config_dict

def get_user_config(config_file=None, default_config=False):
    """Return the user config as a dict"""
    #TODO
    pass