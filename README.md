# Python Package for Converting IPython Jupyter Notebooks to Jekyll Readable (.md, .html)

This repository contains tools for converting .ipynb files to markdown and/or html so that they can be used by Jekyll (the static compiler that GitHub pages uses)

## Notebook Conversion Workflow

This tool converts Jupyter Notebooks (`.ipynb`) into HTML pages suitable for use in a static Jekyll site, with front matter, navigation, and asset handling.

1. **Input**  
   - Jupyter Notebooks (`.ipynb`) located in a configured `nb_read_path` directory.
   - Configuration dictionary specifying read/write paths and asset subdirectories.

2. **Processing**
   - Parses metadata: title, topics (from first cell).
   - Converts notebook to HTML using `nbconvert`.
   - Fixes relative links for images and assets (e.g., `src="/images/foo.png"` → Jekyll-compatible paths).
   - Adds YAML front matter for Jekyll layout integration.
   - Inserts Prev/Next navigation links between notebooks.

3. **Output**
   - Writes processed notebooks as `.html` files to `nb_write_path`.
   - Copies any linked notebook assets (e.g., images) to the correct `assets/` subfolder for Jekyll to use.

## Installation

Install using 
```bash
pip3 install nbconvertjkl
```

## Commandline Usage

To launch interactive command line site build
```bash
python -m nbconvertjkl
```

