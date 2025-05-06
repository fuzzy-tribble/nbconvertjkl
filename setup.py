import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

with open('requirements.txt') as f:
    requirements = f.read().splitlines()

setuptools.setup(
    name="nbconvertjkl-fuzzy-tribble",
    version="0.0.1",
    author="fuzzy-tribble",
    # author_email="author@example.com",
    description="A package to convert ipynbs to jekyll compatable for GitHub pages (including front matter, nav/links, etc)",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/fuzzy-tribble/python3_fluency",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3.6",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6,<3.7',
    install_requires=requirements,
)