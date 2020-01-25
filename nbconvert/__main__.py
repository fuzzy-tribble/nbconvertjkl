"""Allow to be executable through `python -m nbconvert`."""

print("main.py's __name__: {}".format(__name__))
print("main.py's __package__: {}".format(__package__))

from nbconvert.cli import main

if __name__ == "__main__":
    main()