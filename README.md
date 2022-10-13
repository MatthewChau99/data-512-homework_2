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

## Data Processing
The data is combined to form a structured table with the below columns (stored in `data/wp_politicians_by_country.csv`):
- **country**: the country that the politician belongs to
- **region**: the region that the country is in
- **continent**: the continent that the region is in
- **population**: the population of the *country*
- **article_title**: the name of the article
- **revision_id**: the latest revision id of the article
- **article_quality**: the predicted quality of the article by ORES
- **region_population**: the population of the *region*

## Data Analysis and Results
To do a simple analysis, we have generated the total article per population in `data/clean_data/tapp.csv`, as well as the total high quality article per population in `data/clean_data/qapp.csv`. Using these two tables, we have generated the following tables in `src/homework2.ipynb`:
- Top 10 countries by coverage
- Bottom 10 countries by coverage
- Top 10 countries by high quality
- Bottom 10 countries by high quality
- Geographic regions by total coverage
- Geographic regions by high quality coverage


