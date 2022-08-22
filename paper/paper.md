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

# Statement of need

Obtaining data from social media is one of the tools researchers use to gain insights
on people's perception or preferences on a specific topic. Even though getting a
representative sample is often very difficult or impossible, the text data available
in platforms like Twitter are an important asset in research, especially given that 
other researchers, politicians, and renowned organizations usually use this platform 
to spread ideas, plans, and proposals. To make this data available to researchers, Twitter
developed its own API, which also offers free access for academic research. However, 
dealing with authentication, API calls, and data response handling can be overwhelming
for researchers that have little to none experience in coding but still could highly benefit
from the nature of this data. For this reason we have developed `GTdownloader`, a high level 
package that offers easy access to the full-archive-search Twitter API endpoint and compiles the 
retrieved data in standard formats for its further manipulation and analysis. Although there are
currently other great Python based interfaces to retrieve data from Twitter, 
we identified that none of them offer a simple approach for little experienced or
first time programmers. The closest package identified in our search is `TTLocVis`,
which also offers geographical data pre-visualization, but it is mostly for static
visualizations and focuses mainly in topic modelling, which is out of the 
`GTdownloader` scope.


# Summary

The `GTdownloader` `TweetDownloader` class offers  methods to download and visualize the 
data in interactive formats by leveraging the `Plotly`, `Matplotlib`, and `Wordlcoud` libraries. 
The query parameters available from the Twitter API can be passed as arguments of the downloading
method `get_tweets()`. This reduces the chance of ambiguity, specially for first time users that 
might not be familiar with the boolean operators within Twitter queries. One of the key features 
targeted to one-time or inexperienced users is the `tweets_from_csv()` method that reads all the 
query parameters from a parameters table stored in csv format. This functionality allows to make use
of the API by writing just one single command line to run the script. 

Once a download is carried out, the data can be exported in shapefile format to be used as needed.
In addition to exporting the data, preliminary visualization methods are available to gain 
insights on the downloaded data.

### Static visualization

After downloading the tweets, you can quickly preview the centroids of the tweets by calling 
the `preview_tweet_locations()` method:
![image](figures/bike_simple_map.png)

### Interactive maps
The interactive map displays a map in which tweet data such as text and location are displayed
upon hovering. Panning, zooming in and out, and snap shot saving are available n the animation. 
![image](figures/interactive.png)

### Time animation
The time animation method allows to choose from a time unit to visualize the evolution of the amount
of tweets aggregated per location in time. This is an quick way to see if the downloaded data displays
the expected temporal behavior before working on the actual dataset in detail. 

### Wordcloud
Notice we make use of the custom_stopwords parameter to exclude the query words and the http and
https tags that may arise from url posting.
![image](figures/wordcloud_white.png)




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