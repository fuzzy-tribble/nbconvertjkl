"""Global configuration handling."""

import logging
import os
from pathlib import Path

logger = logging.getLogger(__name__)

DEFAULT_CONFIG = {
    "nbs": os.path.join(os.path.dirname(__file__), '../../notebooks/*.ipynb'),
    "site_dir": "../docs/",
    "site_nb_dir": os.path.join(os.path.dirname(__file__), '../../docs/_notebooks/'),
    "site_assets_dir": Path("../docs/assets/"),
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