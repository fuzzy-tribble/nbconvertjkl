import click
import sys

print("main.py's __name__: {}".format(__name__))
print("main.py's __package__: {}".format(__package__))

from ipynb_to_jekyll.log import configure_logger

@click.command()
def main():
    """Simple program that helps you build Jekyll compatable html files from ipython notebooks"""

    click.echo("This script will help you build Jekyll html files from ipynb files")

    if not click.confirm('Do you want to continue?'):
        sys.exit(1)

    # try:
    #     # Collect nb files
    #     click.echo("Looking for notebooks (*.ipynb) in {} folder".format(nb_folder))
    #     nb_files = ipynb_to_jekyll.get_nb_file_list()
    #     if len(nb_files) < 1:
    #         click.echo("Hmmm...No *.ipynb files found in folder X\nExiting...")
    #         sys.exit(1)
    #     elif len(nb_files) > 10:
    #         click.echo("More than 10 *.ipynb files found...do you want to automate?")
    #     else:
    #         if not click.confirm('Found the following notebooks.\nDo you want to continue?'):
    #             sys.exit(1)

    #         # Convert nb_files
    #         for i in range(len(nb_files)):
    #             click.echo("Converting notebook: {}".format(nb_fname))
    #             break


if __name__ == "__main__":
    main()