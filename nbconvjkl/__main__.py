"""Allow to be executable through `python -m nbconvert`."""

from nbconvert import cli

if __name__ == "__main__":
    cli.run()