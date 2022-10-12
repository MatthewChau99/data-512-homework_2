from pathlib import Path


class GlobalConstants:
    def __init__(self, articles_df, page_info_constants=None, ores_constants=None):
        if page_info_constants is None:
            page_info_constants = PageInfoConstants(articles_df=articles_df)
        
        if ores_constants is None:
            ores_constants = ORESConstants(articles_df=articles_df)

        self.page_info_constants = page_info_constants
        self.ores_constants = ores_constants
        self.error_files = {}
        self.project_root = Path(__file__).absolute().parent.parent

        self.region_hierarchy = {
            'NORTHERN AFRICA': 'AFRICA',
            'WESTERN AFRICA': 'AFRICA',
            'EASTERN AFRICA': 'AFRICA',
            'MIDDLE AFRICA': 'AFRICA',
            'SOUTHERN AFRICA': 'AFRICA',
            'NORTHERN AMERICA': 'NORTHERN AMERICA',
            'CENTRAL AMERICA': 'LATIN AMERICA AND THE CARIBBEAN',
            'CARIBBEAN': 'LATIN AMERICA AND THE CARIBBEAN',
            'SOUTH AMERICA': 'LATIN AMERICA AND THE CARIBBEAN',
            'WESTERN ASIA': 'ASIA',
            'CENTRAL ASIA': 'ASIA',
            'SOUTH ASIA': 'ASIA',
            'SOUTHEAST ASIA': 'ASIA',
            'EAST ASIA': 'ASIA',
            'NORTHERN EUROPE': 'EUROPE',
            'WESTERN EUROPE': 'EUROPE',
            'EASTERN EUROPE': 'EUROPE',
            'SOUTHERN EUROPE': 'EUROPE',
            'OCEANIA': 'OCEANIA'
        }


class PageInfoConstants:
    def __init__(self, articles_df):
        self.API_ENWIKIPEDIA_ENDPOINT = "https://en.wikipedia.org/w/api.php"
        self.API_LATENCY_ASSUMED = 0.002       # Assuming roughly 2ms latency on the API and network
        self.API_THROTTLE_WAIT = (1.0/100.0) - self.API_LATENCY_ASSUMED
        self.REQUEST_HEADERS = {
            'User-Agent': '<mmchau@uw.edu>, University of Washington, MSDS DATA 512 - AUTUMN 2022',
        }
        self.ARTICLE_TITLES = articles_df['name']

        self.PAGEINFO_EXTENDED_PROPERTIES = "talkid|url|watched|watchers"

        self.PAGEINFO_PARAMS_TEMPLATE = {
            "action": "query",
            "format": "json",
            "titles": "",           # to simplify this should be a single page title at a time
            "prop": "info",
            "inprop": self.PAGEINFO_EXTENDED_PROPERTIES
        }

class ORESConstants:
    def __init__(self, articles_df):
        self.API_ORES_SCORE_ENDPOINT = "https://ores.wikimedia.org/v3"
        self.API_ORES_SCORE_PARAMS = "/scores/{context}/{revid}/{model}"
        self.API_LATENCY_ASSUMED = 0.002       # Assuming roughly 2ms latency on the API and network
        self.API_THROTTLE_WAIT = (1.0/100.0) - self.API_LATENCY_ASSUMED

        self.REQUEST_HEADERS = {
            'User-Agent': '<mmchau@uw.edu>, University of Washington, MSDS DATA 512 - AUTUMN 2022'
        }

        self.ARTICLE_REVISIONS = {name: '' for name in articles_df['name']}
        self.ORES_PARAMS_TEMPLATE = {
            "context": "enwiki",        # which WMF project for the specified revid
            "revid" : "",               # the revision to be scored - this will probably change each call
            "model": "articlequality"   # the AI/ML scoring model to apply to the reviewion
        }