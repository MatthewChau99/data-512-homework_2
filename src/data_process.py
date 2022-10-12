import pandas as pd
from tqdm import tqdm
import os

from src.data_query import request_pageinfo_per_article, request_ores_score_per_article
from src.global_constants import GlobalConstants

def merge_wiki_page_and_population(wiki_pages_df, pop_df, info_dict, ores_dict, gc=None):
    new_df = pd.DataFrame(columns=[
                          'country', 'region', 'continent', 'population', 'article_title', 'revision_id', 'article_quality'])
    population_dict = {}
    article_to_country = {}
    country_to_article = {}
    country_to_region = {}

    rows = []
    latest_region = 'WORLD'

    for _, row in pop_df.iterrows():
        population_dict.update(
            {row['Geography']: row['Population (millions)']})
        
        if row['Geography'].upper() == row['Geography']:
            latest_region = row['Geography']
        else:
            country_to_region.update({row['Geography']: latest_region})
    
    for _, row in wiki_pages_df.iterrows():
        article_to_country.update({row['name']: row['country']})
        country_to_article.update({row['country']: []})
    
    for page_id, page_info in tqdm(info_dict.items()):
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
            print(f"Error occurred during processing {title}. {e}")

    # Outputs countries with no mathing articles
    with open(os.path.join(gc.project_root, 'data', 'wp_countries-no_match.txt'), 'w') as f:
        for country, articles in country_to_article.items():
            if not articles:
                f.write(country + '\n')
    
    new_df = pd.concat(rows)

    return new_df




if __name__ == '__main__':
    wiki_pages_df = pd.read_csv('politicians_by_country_SEPT.2022.csv')

    populations_df = pd.read_csv('population_by_country_2022.csv')
    articles = wiki_pages_df['name'][:50]
    global_constants = GlobalConstants(wiki_pages_df)
    info_json = {}
    ores_json = {}

    for article in tqdm(articles):
        info = request_pageinfo_per_article(article_title=article, gc=global_constants)
        article_revid = global_constants.ores_constants.ARTICLE_REVISIONS[article]
        ores = request_ores_score_per_article(article_revid=article_revid, gc=global_constants)

        if info is not None:
            info_json.update(info)
        
        if ores is not None:
            ores_json.update(ores)
    
    merged_df = merge_wiki_page_and_population(wiki_pages_df=wiki_pages_df, pop_df=populations_df, info_dict=info_json, ores_dict=ores_json, gc=global_constants)
    # print(merged_df.head())
