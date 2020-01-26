import glob
import os
import re
import logging
import sys
import nbformat

from traitlets.config import Config
from nbconvert import HTMLExporter
from shutil import copyfile

class Converter:
    def __init__(self, config_dict=None, new_nbs=None, existing_nbs=None):
        ''' The converter workhorse '''
        self.config_dict = config_dict
        self.logger = logging.getLogger(__name__)

        self.new_nbs = new_nbs or self.collect_new_notebooks()
        self.existing_nbs = existing_nbs or self.collect_existing_nbs()
        
        # Setup html exporter template/configs
        self.html_exporter = HTMLExporter()
        self.html_exporter.template_file = 'basic'
 
    def collect_new_notebooks(self):
        pass
    
    def get_body(self, nb):
        pass


    def get_info(self, nb):
        pass


    def get_title(self, nb):
        pass


    def get_nav(self, nb):
        pass


    def get_front_matter(self, nb):
        pass

    
    def write_notebook(self, nb_list=None):
        pass


    def get_assets(self, nb):
        pass


    def copy_and_move_assets(self, nb):
        pass