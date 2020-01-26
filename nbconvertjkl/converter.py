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
    def __init__(self, config_dict, new_nbs=None, existing_nbs=None):
        ''' The converter workhorse '''
        self.conf = config_dict
        self.logger = logging.getLogger(__name__)

        self.new_nbs = new_nbs or self.collect_new_nbs()
        self.existing_nbs = existing_nbs or self.collect_existing_nbs()

    def collect_existing_nbs(self):
        """ Collects existing notebooks from site notebooks folder """
        
        self.logger.debug("Getting existing notebook files: {}".format(self.conf['nb_write_path']))
        
        nb_file_paths = glob.glob(self.conf['nb_write_path'] + '*')
        nb_file_paths.sort()
        
        return nb_file_paths


    def collect_new_nbs(self):
        """ Return sorted dictionary of notebooks """

        self.logger.debug("Getting notebook files from {}".format(self.conf['nb_read_path']))

        nb_file_paths = glob.glob(self.conf['nb_read_path'] + '*.ipynb')
        nb_file_paths.sort()

        self.logger.debug("Glob matches: {}".format(len(nb_file_paths)))

        nbs = {}
        for nb_path in nb_file_paths:
            self.logger.debug("\nGathering notebook: {}".format(nb_path))
            
            new_nb = {}
            new_nb['read_path'] = self.conf['nb_read_path']
            new_nb['write_path'] = self.conf['nb_write_path']
            new_nb['nbnode'] = self.get_nbnode(nb_path)

            new_nb['body'] = self.get_body(new_nb['nbnode'])
            new_nb['topics'] = self.get_topics(new_nb['nbnode'])
            new_nb['title'] = self.get_title(new_nb['nbnode'])
            new_nb['permalink'] = self.get_permalink(new_nb['title'])

            new_nb['nav'] = None
            new_nb['info'] = None

            new_nb['front_matter'] = self.get_front_matter(new_nb['title'], new_nb['permalink'], new_nb['topics'])

            self.logger.debug("\n{}\n".format(new_nb['front_matter']))

            temp = {}
            temp[new_nb['title']] = new_nb
            nbs.update( temp )
        
        #TODO Add nav and info at the top

        return nbs
    

    def convert(self):
        #TODO implement convert
        pass


    # def get_summary(self, nbs=None):
    #     """ Print summary of nbs """

    #     self.logger.debug('Getting summary...')

    #     if not nbs:
    #         nbs = self.new_nbs
        
    #     intro_str = "**** SUMMARY START ****\n"
    #     nbs_str = ""
    #     close_str = "**** SUMMARY STOP ****\n"
        
    #     for title in nbs.keys():

    #         self.logger.debug(title)
            
    #         fm = self.new_nbs[title]['front_matter']
    #         info = self.new_nbs[title]['info'] or 'No info'
    #         nav = self.new_nbs[title]['nav'] or 'No navigation'
    #         body_prev = None
    #         nb_str = "\nTITLE: {}\nFRONT_MATTER:\n{}\nINFO:\n{}\nNAV:\n{}\nBODY_PREVIEW:\n{}".format(title, fm, info, nav, body_prev)
    #         nbs_str = nbs_str.join(nb_str)

    #     return intro_str + nbs_str + close_str

    def get_nbnode(self, nb_path):
        """ Returns the nbnode """
        return nbformat.read(nb_path, as_version=4)


    def get_body(self, nb_node):
        """ Get HTML body from notebook and fix links """

        self.logger.debug('Getting nb body...')

        # Setup html exporter template/configs
        html_exporter = HTMLExporter()
        html_exporter.template_file = 'basic'
 
        (body, resources) = html_exporter.from_notebook_node(nb_node)
        fixed_body = self.fix_links(body)
        return fixed_body


    def link_repl(self, matchobj):
        """ Replace src/link matchobj with corrected link """
        print("called repl: {}".format(matchobj.groups()))
        corrected_link = 'src={{{{ "/assets/{}" | relative_url }}}} '.format(matchobj.groups()[0])
        return corrected_link


    def fix_links(self, body):
        """ Find all local asset links and correct """
        s = '|'.join(self.conf['nb_asset_dirs'])
        regex = re.compile(r'(?:source|src)=\"(\/?(?:%s)\/[\w\d\-_\.]+)\"' % s, re.IGNORECASE)
        fixed_body = re.sub(regex, self.link_repl, body)
        return fixed_body


    def get_title(self, nb_node):
        """ Return notebook title """

        self.logger.debug('Getting nb title...')

        for cell in nb_node.cells:
            if cell.source.startswith('#'):
                title = cell.source[1:].splitlines()[0].strip()
                cleaned_title = re.sub(r'[^\w\s]', '', title)
                break

        return cleaned_title or ''


    def get_permalink(self, nb_title):
        """ Return notebook permalink """

        self.logger.debug('Getting nb permalink...')

        #TODO harden...check for special chars, etc
        permalink = nb_title.lower().replace(" ", "-")

        return permalink


    def get_topics(self, nb_node):
        """ Return notebook topics """

        self.logger.debug('Getting nb topics...')

        txt_src = nb_node.cells[0].source
        regex = r"\*\*Topics\sCovered\*\*([\\n\*\s]+[\w\s]+)+"
        m = re.search(regex, txt_src)
        if len(m.group()) != 0:
            topics = m.group().replace("**Topics Covered**\n* ", "").split("\n* ")
        else: 
            topics = ''

        return str(topics)


    def get_info(self, nb):
        """ Return notebook info """
        pass


    def get_nav(self, nb):
        """ Return notebook nav """
        pass


    def get_front_matter(self, title, permalink, topics):
        """ Return front_matter string """

        self.logger.debug('Getting front matter...')

        layout = "notebook"
        fm = "---\nlayout: {}\ntitle: {}\npermalink: /{}/\ntopics: {}\n---\n".format(layout, title, permalink, topics)
        return fm

    
    def write_notebook(self, nb_list=None):
        pass


    def copy_and_move_assets(self, nb):
        pass