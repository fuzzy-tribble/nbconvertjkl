import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

with open('requirements.txt') as f:
    requirements = f.read().splitlines()

setuptools.setup(
    name="nbconvertjkl-nancynobody",
    version="0.0.1",
    author="nancynobody",
    # author_email="author@example.com",
    description="A small package to convert ipynbs to jekyll compatable for GitHub pages",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/nancynobody/python3_fluency",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
    install_requires=requirements,
)