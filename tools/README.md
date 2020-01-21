# Tools

These are tools for managing the notebooks in this repository.

`configs.py`: this file is for your custom build customizations

`convert_ipynbs.py`: running this script will perform the following tasks:

* **Writes `front_matter`** to the top of the output file. The front matter resides in between three dashes at the top of the output file and can be customized in `configs.py`

```bash
---
title: My Notebook
permalink: /my_nb/
topics: ['nb topic 1', 'nb topic 2']
---
```

* **Writes `nb_info`** just below `front_matter` that will be included on every notebook page; can be customized in `configs.py`

```html
<!--NB_INFO-->
<img align="left" style="padding-right:10px;" src="images/my_image.png">
<p>
    This collection of notebooks is very special to me and this is something I would like to say about them.
</p>
```

* **Writes `nb_body`** just below `nb_info` that is the contents of your notebook.

*Note: Navigation is also added to each of the notebook pages but this is done in the `_layouts/notebook.html` using Liquid; customizations to navigation can be made there.*