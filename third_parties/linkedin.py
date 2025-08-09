import os
import requests
from dotenv import load_dotenv

load_dotenv()

def scrape_linkedin_profile(linkedin_profile_url: str, mock:bool=False):
    """screpe information from LinkedIn profile"""
    if mock:
        linkedin_profile_url = "https://gist.githubusercontent.com/tankudo/e5cc6dd09b392353ec2920e3072f8552/raw/tatyjana-ankudo-scraping.json"
        response = requests.get(linkedin_profile_url, timeout=10)
        return response.json()
    else:
        api_endpoint = "https://api.scrapin.io/enrichment/profile"
        params = {
            "apikey": os.environ["SCRAPIN_API_KEY"],
            "linkedInUrl": linkedin_profile_url
            }
        response = requests.get(
            api_endpoint,
            params=params,
            timeout=10,
        )
        raw_data = response.json().get("person")
        data = {
            k: v
            for k, v in raw_data.items()
            if v not in ([], "", "", None) and k not in ("certifications")
        } 
        # print(f"API Response status: {response.status_code if response else 'No response'}")
        # print(f"Raw data: {raw_data}")
        # print(f"Raw data type: {type(raw_data)}")
        return data

if __name__ == "__main__":
    print(screpe_linkedin_profile("https://www.linkedin.com/in/ankudo", mock=True))