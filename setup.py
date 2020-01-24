import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="ipynb_to_jekyll-nancynobody",  # Replace with your own username
    version="0.0.1",
    author="nancynobody",
    author_email="author@example.com",
    description="A small package to convert ipynbs to jekyll readble for GitHub pages",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/pypa/sampleproject",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
)