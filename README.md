# Considering Bias in Data

## Description
This project aims to explore the concept of bias in data with Wikipedia articles. Using political figures from around the globe, we would combine a dataset of Wikipedia articles with a country populations dataset and use ORES, a machine learning service to estimate the article qualities.

## Data
1. The politicians data is collected from https://en.wikipedia.org/wiki/Category:Politicians_by_nationality as a list of politicians along with their wikipedia links and countries as to September 2022. This is located at `data/politicians_by_country.SEPT.2022.csv`.
2. The populations data is collected from the World Population Data Sheet https://www.prb.org/international/indicator/population/table/ published by the Popultaion Reference Bureau, as to 2022. This is located at `data/population_by_country_2022.csv`.

## Data Acquisition
To use the ORES system, short for "Objective Revision Evaluation Service", there are three steps to get the predictions for a politician article:
1. Read `politicians_by_country.SEPT.2022.csv` and obtain the politician name in each line
2. Make a Page info request to obtain the page info for the politician, including the revision id
3. Make a ORES request with the revision id
The code for the above is contained in `src/data_query.py`.


