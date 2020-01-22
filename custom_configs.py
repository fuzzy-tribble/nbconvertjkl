### DEFINE YOUR CUSTOM CONFIGS HERE ###
import os

# The directory that contains your .ipynb files
# If you followed the README they should be in the ../notebooks/ folder
INPUT_NB_DIR = os.path.join(os.path.dirname(__file__), '..', 'notebooks/')

# The directory that you want to put the converted notebooks
# If you followed the READ they will go in the /docs/_notebooks folder
OUTPUT_NB_DIR = '../docs/_notebooks/'

# NOTEBOOK INFO
# Edit the notebook info that you want at the top of your notebook pages
NB_INFO = "<!--NB_INFO-->" + """<img align="left" width="30" style="padding-right:10px;" src="{{ '/assets/images/python-logo.png' | relative_url }}"><p style="font-style:italic;font-size:smaller;">This notebook is part of the {{ site.title }}; the content is available <a href="https://github.com/nancynobody">on GitHub</a>.Lorem ipsum dolor sit amet, consectetur adipiscing elit, sed do eiusmod tempor incididunt ut labore et dolore magna aliqua. Ut enim ad minim veniam, quis nostrud exercitation ullamco laboris nisi ut aliquip ex ea commodo consequat.</p>"""

# NOTEBOOK NAV
# True shows navigation, False doesn't
NB_NAV = True

# NOTEBOOK TOPICS
# TODO allow config option of displaying nb topics in table of contents
# Regex to capture topics in markdown formatted like this in the first cell
# Topics Covered
# \n* Topic A
# \n* Topic B
REGEX_TOPICS = r"\*\*Topics\sCovered\*\*([\\n\*\s]+[\w\s]+)+" 

# NOTEBOOK TITLE
# TODO allow config option for displaying nb title

# NOTEBOOK FRONT MATTER
# TODO allow editing of front_matter

# DIRS WITH NOTEBOOK ASSETS
# These are the folders that have images/data/etc that need
# to be moved to the sites assets dir so they can be displayed
# ALL OF YOUR NB ASSETS MUST BE IN A SUBFOLDER!!!!
NB_ASSET_DIRS = ['figures', 'data', 'images', 'imgs']