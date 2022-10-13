import pandas as pd
from tqdm import tqdm
import os
import json

from src.global_constants import GlobalConstants

def merge_wiki_page_and_population(wiki_pages_df, pop_df, info_dict, ores_dict, gc=None):
    """
    Merge the politicians and population dataframes into a structured table with the following columns:
    Country     Region      Continent       Population      Article title       Revision ID     Article Quality

    :params wiki_pages_df: the politicians dataframe
    :params pop_df: the population dataframe
    :params info_dict: the page info dictionary
    :params ores_dict: the ORES prediction dictionary
    :params gc: the global constant object

    Return: the combined dataframe if there is valid politicians else None
    """
    new_df = pd.DataFrame(columns=[
                          'country', 'region', 'continent', 'population', 'article_title', 'revision_id', 'article_quality'])
    population_dict = {}
    article_to_country = {}
    country_to_article = {}
    country_to_region = {}

    rows = []
    latest_region = 'WORLD'

    # Iterate population dataframe and add mappings to population_dict and country_to_region mapping.
    for _, row in pop_df.iterrows():
        population_dict.update(
            {row['Geography']: row['Population (millions)']})
        
        if row['Geography'].upper() == row['Geography']:
            latest_region = row['Geography']
        else:
            country_to_region.update({row['Geography']: latest_region})
    
    # Iterate the politicians dataframe and update the article to country & country to article mappings
    for _, row in wiki_pages_df.iterrows():
        article_to_country.update({row['name']: row['country']})
        country_to_article.update({row['country']: []})
    
    # Add all required info in a new row
    for _, page_info in tqdm(info_dict.items()):
        try:
            title = page_info['title']
            country = article_to_country[title]
            region = country_to_region[country]
            continent = gc.region_hierarchy[region]
            population = population_dict[country]
            revision_id = page_info['lastrevid']
            article_quality = ores_dict[str(revision_id)]['articlequality']['score']['prediction']
            region_population = population_dict[region]

            country_to_article[country].append(title)
            new_row = {
                'country': [country],
                'region': [region],
                'continent': [continent],
                'population': [population],
                'article_title': [title],
                'revision_id': [revision_id],
                'article_quality': [article_quality],
                'region_population': [region_population]
            }

            rows.append(pd.DataFrame.from_dict(new_row))
        except Exception as e:
            print(f"Error occurred during processing {title}.")
    
    # Outputs countries with no matching articles
    with open(os.path.join(gc.project_root, 'data', 'wp_countries-no_match.txt'), 'w') as f:
        for country, articles in country_to_article.items():
            if not articles:
                f.write(country + '\n')
    
    # If rows contains valid data, merge them and output the result dataframe
    if rows:
        new_df = pd.concat(rows)
        return new_df
    
    return None




if __name__ == '__main__':
    wiki_pages_df = pd.read_csv('politicians_by_country_SEPT.2022.csv')
    populations_df = pd.read_csv('population_by_country_2022.csv')
    global_constants = GlobalConstants(wiki_pages_df)
    
    with open(os.path.join(global_constants.project_root, "data", "info.json"), "r") as f:
        info_json = json.load(f)

    with open(os.path.join(global_constants.project_root, "data", "ores.json"), "r") as f:
        ores_json = json.load(f)
    
    merged_df = merge_wiki_page_and_population(wiki_pages_df=wiki_pages_df, pop_df=populations_df, info_dict=info_json, ores_dict=ores_json, gc=global_constants)
    # print(merged_df.head())
