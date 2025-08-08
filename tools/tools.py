from langchain_tavily import TavilySearch

def get_profile_url_tavily(name: str):
    """
    Seerch LinkedIn
    """
    search = TavilySearch()
    res = search.run(f'{name} LinkedIn profile')

    return res