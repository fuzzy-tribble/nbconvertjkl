""" The command line interface for nbconvertjkl """

import click
import sys
import nbformat

from nbconvertjkl.log import configure_logger
from nbconvertjkl.config import get_config
from nbconvertjkl.converter import Converter
# from nbconvertjkl import convert
# from nbconvertjkl import copy_assets

@click.command()
def run():
    """ Simple program that helps you build Jekyll compatable html files from ipython notebooks """

    logger = configure_logger()
    config_dict = get_config()

    click.echo("Initializing converter and gathering notebooks.")
    converter = Converter(config_dict)

    if not converter.new_nbs:
        click.secho("No notebooks found.\nMake sure the "
                    "read/write config paths are set properly "
                    "and try again.\nExiting", fg='red')
        sys.exit(1)
    
    else:

        if not click.confirm("Found {} notebooks to convert.\nDo you want to continue?".format(len(converter.new_nbs))):
            sys.exit(1)
        
        else:
            
            click.echo("Converting notebooks...")
            converter.convert()

            click.echo("Please verify the front matter (title, link, topics covered) for each notebook.")
            for nbtitle in converter.new_nbs.keys():

                click.secho("*****{}*****".format(nbtitle), fg='bright_white')

                #TODO add or skip each notebook
                # click.confirm("Add this notebook to your site (skipping this notebook will simply leave it out of the site)".format(fm))
                
                fm = converter.new_nbs[nbtitle]["front_matter"]
                click.echo("Notebook front_matter:\n{}".format(fm))
                
                res = click.prompt("Press 'e' to edit or any key to save and continue.", default='s')
                if res == 'e':
                    edited_fm = click.edit(fm)
                    #TODO validate edited front_matter
                    # if not converter.is_valid_front_matter(edited_fm):
                        # edit again

            click.secho("Converter summary:".format(nbtitle), fg='bright_white')
            click.echo(converter.get_summary())
            # click.confirm("Write files and finish?")

            # #TODO Empty _notebooks folder of existing nbs
            # #TODO Add confirmation before for overwriting existing
            # click.secho("Found existing notebooks in docs/_notebooks. This action will replace all existing with the new ones in the summary.", fg='red')
            # click.confirm("Are you sure you want to overwrite all existing?")

            # # TODO add click.progressbar()
            # click.echo("Writing notebooks...")
            # converter.write_nbs()

            # # TODO add click.progressbar()
            # click.echo("Collecting and moving notebook assets...")
            # converter.copy_and_move_assets()


if __name__ == "__main__":
    run()