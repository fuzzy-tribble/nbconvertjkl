"""Allow to be executable through `python -m ipynb_to_jekyll`."""

print("main.py's __name__: {}".format(__name__))
print("main.py's __package__: {}".format(__package__))

from ipynb_to_jekyll.cli import main

if __name__ == "__main__":  # pragma: no cover
    main(prog_name="ipynb_to_jekyll")