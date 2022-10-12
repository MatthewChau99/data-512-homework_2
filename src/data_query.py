import json, time, urllib.parse, os

import requests
from tqdm import tqdm
import pandas as pd

from src.global_constants import GlobalConstants

articles_df = pd.read_csv('politicians_by_country_SEPT.2022.csv')

def request_pageinfo_per_article(article_title=None, gc=None):
    if not article_title: return None
    
    if gc is None:
        gc = GlobalConstants(articles_df)
    
    endpoint_url = gc.page_info_constants.API_ENWIKIPEDIA_ENDPOINT
    request_template = gc.page_info_constants.PAGEINFO_PARAMS_TEMPLATE
    headers = gc.page_info_constants.REQUEST_HEADERS

    request_template['titles'] = article_title
        
    # make the request
    try:
        # we'll wait first, to make sure we don't exceed the limit in the situation where an exception
        # occurs during the request processing - throttling is always a good practice with a free
        # data source like Wikipedia - or any other community sources
        if gc.page_info_constants.API_THROTTLE_WAIT > 0.0:
            time.sleep(gc.page_info_constants.API_THROTTLE_WAIT)
        response = requests.get(endpoint_url, headers=headers, params=request_template)
        
        json_response = response.json()
        json_info = json_response['query']['pages']
        gc.ores_constants.ARTICLE_REVISIONS[article_title] = json_info[list(json_info)[0]]['lastrevid']
    except Exception as e:
        gc.error_files.update({article_title: f'Page info request error: {e}'})
        print(f'Page info request error: {e}')
        json_info = None

    return json_info


def request_ores_score_per_article(article_revid = None, gc=None, features=False):
    # Make sure we have an article revision id
    if not article_revid: 
        return None

    if gc is None:
        gc = GlobalConstants(articles_df)
    
    endpoint_url = gc.ores_constants.API_ORES_SCORE_ENDPOINT
    endpoint_params = gc.ores_constants.API_ORES_SCORE_PARAMS
    request_template = gc.ores_constants.ORES_PARAMS_TEMPLATE
    headers = gc.ores_constants.REQUEST_HEADERS
    
    request_template['revid'] = article_revid
    
    request_url = endpoint_url + endpoint_params.format(**request_template)
    
    if features:
        request_url = request_url + "?features=true"
    
    # make the request
    try:
        if gc.ores_constants.API_THROTTLE_WAIT > 0.0:
            time.sleep(gc.ores_constants.API_THROTTLE_WAIT)
        response = requests.get(request_url, headers=headers)
        json_response = response.json()
        json_info = json_response['enwiki']['scores']
    except Exception as e:
        gc.error_files.update({article_revid: f'ORES request error: {e}'})
        print(f'ORES request error: {e}')
        json_info = None

    return json_info



if __name__ == '__main__':
    articles = articles_df['name']
    global_constants = GlobalConstants(articles_df)
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
    
    if not os.path.exists(os.path.join(global_constants.project_root, 'data')):
        os.mkdir('data')

    with open(os.path.join(global_constants.project_root, "data", "info.json"), "w") as f:
        json.dump(info_json, f, indent=4)

    with open(os.path.join(global_constants.project_root, "data", "ores.json"), "w") as f:
        json.dump(ores_json, f, indent=4)

    with open(os.path.join(global_constants.project_root, 'data', 'error_files.txt'), "w") as f:
        for error_file in global_constants.error_files:
            f.write(error_file + '\n')