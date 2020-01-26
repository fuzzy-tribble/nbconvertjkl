""" The command line interface for nbconvert """

import click
import sys
import nbformat

from nbconvertjkl.log import configure_logger
from nbconvertjkl.config import get_config
from nbconvertjkl import convert

@click.command()
def run():
    """Simple program that helps you build Jekyll compatable html files from ipython notebooks"""

    file_rng = (1, 10)  # file range for manual conversion

    logger = configure_logger()

    click.echo("This script will help you build Jekyll html files from ipynb files")

    config_dict = get_config()

    # Collect nb files
    click.echo("Looking for notebooks in {}".format(config_dict["nbs"]))
    nb_files = convert.get_nb_files(config_dict['nbs'])

    if nb_files == None or len(nb_files) < file_rng[0]:
        click.secho("No notebooks found. Make sure the "
                    "'nbs' config option is set properly "
                    "and try again.\nExiting", fg='red')
        sys.exit(1)
    
    else:
        if not click.confirm('Found {} notebooks.\nDo you want to continue?'.format(len(nb_files))):
            sys.exit(1)
        else:
            click.echo("Found nb_info and nb_nav in your config file. "
                        "These will be included at the top of your notebooks.")

            for i in range(len(nb_files)):
                curr_nb_fname = nb_files[i].split("/")[-1]
                new_nb_fname = curr_nb_fname[:-5] + "html"
                click.echo("Preparing to convert notebook {} -> {}".format(curr_nb_fname, new_nb_fname))

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
                front_matter = convert.get_front_matter(curr_nb_node)
                nb_info = convert.get_nb_info(curr_nb_node)
                nb_nav = convert.get_nb_nav(prev_nb_node, next_nb_node)
                body = convert.get_body(curr_nb_node)

                # confirm / customize
                click.echo("Extracted the following front_matter:\n{}".format(front_matter))
                click.echo('Enter to save and continue or edit [e]?', nl=False)
                c = click.getchar()
                click.echo()
                if c == 'e':
                    front_matter = click.edit(front_matter)
                    #TODO validate edited front_matter

                write_path = config_dict["site_nb_dir"] + new_nb_fname
                click.echo("Writing notebook: {}".format(new_nb_fname))

                with open(write_path, "w") as file:
                    file.write(front_matter)
                    if nb_info:
                        file.write(nb_info)
                    if nb_nav:
                        file.write(nb_nav)
                    file.write(body)

                click.echo("Done.")


if __name__ == "__main__":
    run()