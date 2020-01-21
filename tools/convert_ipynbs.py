import nbformat
import glob
import os
import re
from traitlets.config import Config
from nbconvert import HTMLExporter
from shutil import copyfile

import custom_configs as conf

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
    s = '|'.join(conf.NB_ASSET_DIRS)
    regex = re.compile(r'(?:source|src)=\"(\/?(?:%s)\/[\w\d\-_\.]+)\"' % s, re.IGNORECASE)
    fixed_body = re.sub(regex, link_repl, body)
    return fixed_body


def get_nb_info(nb_node):
    """ Return nb info from configs or nothing"""
    return conf.NB_INFO or False


def get_nb_title(nb_node):
    """ Get notebook title give a nb_node (json) """
    for cell in nb_node.cells:
        if cell.source.startswith('#'):
            return cell.source[1:].splitlines()[0].strip()


def get_nb_topics(nb_node):
    """ Get notebook topics give a nb_node (json) """
    txt_src = nb_node.cells[0].source
    m = re.search(conf.REGEX_TOPICS, txt_src)
    if len(m.groups) != 0:
        topics = m.group(0).replace("**Topics Covered**\n* ", "").split("\n* ")
    else topics = ''
    return str(topics)


def get_front_matter(nb_node):
    """ Get front matter for Jekyll """
    layout = "notebook"
    title = get_nb_title(nb_node)
    # TODO HARDEN - check for special chars in title?
    permalink = title.lower().replace(" ", "-")
    topics = str(get_nb_topics(nb_node))
    return "---\nlayout: {}\ntitle: {}\npermalink: /{}/\ntopics: {}\n---\n".format(layout, title, permalink, topics)


def get_nb_nav(prev, nxt):
    """ Get html for notebook navigation """
    #TODO update to use Liquid relative urls

    nav_comment = '<!-- NAV -->'

    if prev == None:
        prev_nb = ''
    else:
        prev_title = get_nb_title(prev)
        prev_link = prev_title.lower().replace(" ", "-")
        prev_nb = '&lt; <a href="{{{{ "{}" | relative_url }}}}">{}</a> | '.format(prev_link, prev_title)

    contents = '<a href="/ipynb_template_site/">Contents</a>'

    if nxt == None:
        nxt_nb = ''
    else:
        nxt_title = get_nb_title(nxt)
        nxt_link = nxt_title.lower().replace(" ", "-")
        nxt_nb = ' | <a href="{{{{ "{}" | relative_url }}}}">{}</a> &gt;'.format(nxt_link, nxt_title)
    
    nb_nav = '{}<p style="font-style:italic;font-size:smaller;">{}{}{}</p>'.format(nav_comment, prev_nb, contents, nxt_nb)
    return nb_nav


def ipynb_to_html(in_dir=conf.INPUT_NB_DIR, out_dir=conf.OUTPUT_NB_DIR):
    """
    Convert list of ipython notebooks to final html files
    with front matter, navigation, body, etc.
    """

    nb_files = glob.glob(in_dir + '*.ipynb')
    nb_files.sort()
    print(nb_files)

    if len(nb_files) < 1:
        print("Found no notebooks to convert in {}".format(in_dir))

    for i in range(len(nb_files)):
        #TODO optimize this by passing titles and permalinks 
        # around instead of reopening nb nodes

        # track prev, curr, next for navigation purposes
        curr_nb_node = nbformat.read(nb_files[i], as_version=4)
        if i == 0:
            prev_nb_node = None
            next_nb_node = nbformat.read(nb_files[i+1], as_version=4)
        elif i == len(nb_files)-1:
            prev_nb_node = nbformat.read(nb_files[i-1], as_version=4)
            next_nb_node = None
        else:
            prev_nb_node = nbformat.read(nb_files[i-1], as_version=4)
            next_nb_node = nbformat.read(nb_files[i+1], as_version=4)
        
        # convert, add into, front matter, etc
        front_matter = get_front_matter(curr_nb_node)
        nb_info = get_nb_info(curr_nb_node)
        nb_nav = get_nb_nav(prev_nb_node, next_nb_node)
        body = get_body(curr_nb_node)

        curr_nb_file_name = nb_files[i].split("/")[-1]
        write_path = out_dir + curr_nb_file_name[:-5] + "html"
        print("Writing notebook: {}...".format(write_path))

        with open(write_path, "w") as file:
            file.write(front_matter)
            if nb_info:
                file.write(nb_info)
            if nb_nav:
                file.write(nb_nav)
            file.write(body)


def move_assets(inp=conf.NB_ASSET_DIRS):
    """ Move assets (images, etc) from notebook folder to docs/assets folder """
    #TODO fix so it doesn't overwrite by default

    dest = os.path.join(os.path.dirname(__file__), '..', 'docs/assets/')
    print("Preparing to copy asset files...")

    for subdir in inp:
        print("Looking in: {}".format(subdir))
        files = glob.glob(conf.INPUT_NB_DIR + subdir + '/*')
        print("Found files: {}".format(files))
        for src in files:
            if os.path.isfile(src):
                fname = src.split("/")[-1]
                print("Copying file: {}...".format(fname))
                fdest = dest + subdir
                if not os.path.exists(fdest):
                    os.mkdir(fdest)
                copyfile(src, fdest + '/' + fname)

if __name__ == '__main__':
    ipynb_to_html()
    move_assets()
