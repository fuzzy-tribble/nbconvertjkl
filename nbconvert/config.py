"""Global configuration handling."""

logger = logging.getLogger(__name__)

DEFAULT_CONFIG = {
    "nb_dir": os.path.expanduser("~/notebooks/"),
    "site_dir": os.path.expanduser("~/docs/"),
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