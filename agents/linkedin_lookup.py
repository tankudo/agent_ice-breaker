from dotenv import load_dotenv

load_dotenv()

from langchain_openai import ChatOpenAI
from langchain_core.prompts import PromptTemplate
from langchain_core.tools import Tool
from langchain.agents import (create_react_agent, AgentExecutor,)
from langchain import hub
from langchain_ollama import ChatOllama
from langchain_tavily import TavilySearch
import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from tools.tools import get_profile_url_tavily


def lookup_multiple(name: str) -> list:
    """Find multiple LinkedIn profiles with comprehensive search"""
    print(f"🔍 Direct search for multiple profiles: {name}")
    
    try:
        all_profiles = []
        
        # Try multiple search variations to get more results
        search_queries = [
            f"{name} LinkedIn",
            f"{name} LinkedIn profile",
            f'"{name}" site:linkedin.com/in',
            name  # Simple name search
        ]
        
        seen_urls = set()  # Avoid duplicates
        
        for query in search_queries:
            try:
                print(f"📞 Searching with: {query}")
                search_results = get_profile_url_tavily(query)
                
                if isinstance(search_results, dict) and 'results' in search_results:
                    print(f"📊 Found {len(search_results['results'])} results for '{query}'")
                    
                    for i, result in enumerate(search_results['results']):
                        url = result.get('url', '')
                        title = result.get('title', '')
                        content = result.get('content', '')
                        
                        # Only process LinkedIn profile URLs we haven't seen
                        if '/in/' in url and 'linkedin.com' in url and url not in seen_urls:
                            seen_urls.add(url)
                            
                            name_part = title.split(' - ')[0] if ' - ' in title else title
                            job_title = title.split(' - ')[1] if ' - ' in title else content[:100]
                            
                            picture_url = get_profile_picture(url, name_part)
                            
                            profile = {
                                'url': url,
                                'name': name_part,
                                'preview': job_title + '...' if job_title else 'No description',
                                'picture': picture_url
                            }
                            all_profiles.append(profile)
                            print(f"✅ Added profile: {profile['name']} - {profile['picture']}")
                            
            except Exception as e:
                print(f"❌ Search failed for '{query}': {e}")
                continue
        
        print(f"🎯 Total unique profiles found: {len(all_profiles)}")
        return all_profiles
        
    except Exception as e:
        print(f"❌ Search error: {e}")
        import traceback
        traceback.print_exc()
        return []


def get_profile_picture(linkedin_url: str, name: str) -> str:
    """Try to get the actual profile picture from LinkedIn"""
    try:
        print(f"🖼️ Trying to get picture for: {linkedin_url}")
        
        # Quick scrape just for the picture
        from third_parties.linkedin import scrape_linkedin_profile
        profile_data = scrape_linkedin_profile(linkedin_url, mock=False)
        
        if profile_data and isinstance(profile_data, dict):
            # Try different picture field names
            picture_fields = ['profile_pic_url', 'photoUrl', 'profile_picture', 'image_url', 'picture']
            for field in picture_fields:
                if field in profile_data and profile_data[field]:
                    picture_url = profile_data[field]
                    # Validate it's a real image URL
                    if picture_url.startswith('http') and ('image' in picture_url or 'photo' in picture_url):
                        print(f"✅ Found picture: {picture_url}")
                        return picture_url
                        
    except Exception as e:
        print(f"⚠️ Could not get picture for {linkedin_url}: {e}")
    
    # Enhanced placeholder with better styling
    initials = get_initials(name)
    # Use different colors for different people
    colors = ['4A90E2', '28A745', 'DC3545', 'FFC107', '6F42C1', '20C997']
    color = colors[hash(name) % len(colors)]
    placeholder = f"https://via.placeholder.com/80x80/{color}/ffffff?text={initials}"
    print(f"📱 Using enhanced placeholder: {placeholder}")
    return placeholder
    


def get_initials(name: str) -> str:
    """Get initials from name for placeholder"""
    words = name.split()
    if len(words) >= 2:
        return f"{words[0][0]}{words[1][0]}".upper()
    elif len(words) == 1 and words[0]:
        return words[0][0].upper()
    else:
        return "?"
