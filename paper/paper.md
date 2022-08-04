---
title: 'GTdownloader: A Python package to download, visualize, and export georeferenced tweets'
tags:
  - Python
  - data science
  - GIS
  - sentiment analysis
authors:
  - name: Juan G. Acosta-Sequeda
    equal-contrib: true
    affiliation: "1" # (Multiple affiliations must be quoted)
  - name: Sybil Derrible
    orcid: 0000-0000-0000-0000
    equal-contrib: true # (This is how you can denote equal contributions between multiple authors)
    affiliation: 2
affiliations:
  - name: Department of Civil, Materials and Environmental Engineering, Associate Professor, University of Illinois at Chicago, USA
    index: 1
  - name: Department of Civil, Materials and Environmental Engineering, PhD student, University of Illinois at Chicago, USA
    index: 2
date: 08 August 2022
bibliography: paper.bib

aas-doi: 10.3847/xxxxx <- update this with the DOI from AAS once you know it.
aas-journal: Astrophysical Journal <- The name of the AAS journal.
---

# Summary

Obtaining data from social media is one of the tools researchers use to gain insights
on people's perception or preferences on a specific topic. Even though getting a
representative sample is often very difficult or impossible, the text data available
in platforms like Twitter are an important asset in research, especially given that 
other researchers, politicians, and renowned organizations usually use this platform 
to spread ideas, plans, and proposals. To make this data available to researchers, Twitter
developed its own API, which also offers free access for academic research. However, 
dealing with authentication, API calls, and data response handling can be overwhelming
for researchers that have little to none experience in coding but still could highly benefit
from the nature of this data. For this reason we have developed a high level package that
offers easy access to the full-archive-search Twitter API endpoint and compiles the 
retrieved data in standard formats for its further manipulation and analysis.


# Statement of need

`GTdownloader` is a Python package intended to ease the download of georeferenced
tweets from Twitter for research purposes. In addition to offering user-friendly
interaction with the Twitter API, the central `TweetDownloader` class offers 
methods to visualize the data in interactive formats by leveraging the `Plotly`,
`Matplotlib`, and `wordlcoud` libraries, as shown in Figure ***9999***. There are
currently other great Python based interfaces to retrieve data from Twitter, but
we identified that none of them offer a simple approach for little experienced or
first time programmers. The closest package identified in our search is `TTLocVis`,
which also offers geographical data pre-visualization, but it is mostly for static
visualizations and focuses mainly in topic modelling, which is out of the 
`GTdownloader` domain.


enables wrapping low-level languages (e.g., C) for speed without losing
flexibility or ease-of-use in the user-interface. The API for `Gala` was
designed to provide a class-based and user-friendly interface to fast (C or
Cython-optimized) implementations of common operations such as gravitational
potential and force evaluation, orbit integration, dynamical transformations,
and chaos indicators for nonlinear dynamics. `Gala` also relies heavily on and
interfaces well with the implementations of physical units and astronomical
coordinate systems in the `Astropy` package [@astropy] (`astropy.units` and
`astropy.coordinates`).

`Gala` was designed to be used by both astronomical researchers and by
students in courses on gravitational dynamics or astronomy. It has already been
used in a number of scientific publications [@Pearson:2017] and has also been
used in graduate courses on Galactic dynamics to, e.g., provide interactive
visualizations of textbook material [@Binney:2008]. The combination of speed,
design, and support for Astropy functionality in `Gala` will enable exciting
scientific explorations of forthcoming data releases from the *Gaia* mission
[@gaia] by students and experts alike.



# Citations

Citations to entries in paper.bib should be in
[rMarkdown](http://rmarkdown.rstudio.com/authoring_bibliographies_and_citations.html)
format.

If you want to cite a software repository URL (e.g. something on GitHub without a preferred
citation) then you can do it with the example BibTeX entry below for @fidgit.

For a quick reference, the following citation commands can be used:
- `@author:2001`  ->  "Author et al. (2001)"
- `[@author:2001]` -> "(Author et al., 2001)"
- `[@author1:2001; @author2:2001]` -> "(Author1 et al., 2001; Author2 et al., 2002)"

# Figures

Figures can be included like this:
![Caption for example figure.\label{fig:example}](figure.png)
and referenced from text using \autoref{fig:example}.

Figure sizes can be customized by adding an optional second parameter:
![Caption for example figure.](figure.png){ width=20% }

# Acknowledgements

We acknowledge contributions from Brigitta Sipocz, Syrtis Major, and Semyeong
Oh, and support from Kathryn Johnston during the genesis of this project.

# References