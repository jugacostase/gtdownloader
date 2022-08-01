from setuptools import setup, find_packages

# To use a consistent encoding
from codecs import open
from os import path

# The directory containing this file
HERE = path.abspath(path.dirname(__file__))

# Get the long description from the README file
with open(path.join(HERE, 'README.md'), encoding='utf-8') as f:
    long_description = f.read()

# This call to setup() does all the work
setup(
    name="gtdownloader",
    version="0.1.0",
    description="A Python package for the simple downloading of tweets with geographical information",
    long_description="GTdownloader is a geographical tweets downloading tool that leverages the Twitter \
                      API and searchtweets-v2 to retrieve tweets with geographical information and store \
                      them in easy access formats like .csv and .shp.",
    long_description_content_type="text/markdown",
    url="https://gtdownloader.readthedocs.io/",
    author="Juan G Acosta",
    author_email="jgacostas@icloud.com",
    license="MIT",
    classifiers=[
        "Intended Audience :: Developers",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Operating System :: OS Independent"
    ],
    packages=["gtdownloader"],
    include_package_data=True,
    install_requires=["pandas",
                      "geopandas",
                      "matplotlib",
                      "seaborn",
                      "shapely",
                      "wordcloud",
                      "plotly",
                      "searchtweets-v2"]
)