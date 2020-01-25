""" The command line interface for nbconvert """

import click
import sys

from nbconvert.log import configure_logger
from nbconvert.config import get_config
from nbconvert import convert

@click.command()
def run():
    """Simple program that helps you build Jekyll compatable html files from ipython notebooks"""

    # File range for manual conversion
    file_rng = (1, 10)

    logger = configure_logger()

    click.echo("This script will help you build Jekyll html files from ipynb files")

    if not click.confirm('Do you want to continue?'):
        sys.exit(1)

    # Get configs
    config_dict = get_config()

    # Collect nb files
    click.echo("Looking for notebooks (*.ipynb) in {} folder".format(config_dict["nb_dir"]))
    nb_files = convert.get_nb_files(config_dict['nb_dir'])

    logger.debug(nb_files)

    if len(nb_files) < file_rng[0]:
        click.echo("No *.ipynb files found in {} X\nMake sure you have *.ipynb files in the 'nb_dir' of your config file...")
        sys.exit(1)
    elif len(nb_files) > file_rng[1]:
        click.echo("More than 10 *.ipynb files found...do you want to automate?")
        #TODO add automation feature for big sites
    else:
        if not click.confirm('Found the following notebooks.\nDo you want to continue?'):
            sys.exit(1)
        else:
            # Convert nb_files
            for i in range(len(nb_files)):
                click.echo("Converting notebook: {}".format(nb_files[i]))

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


if __name__ == "__main__":
    run()