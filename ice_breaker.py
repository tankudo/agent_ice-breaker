import os
from output_parser import summry_parser, Summary
from dotenv import load_dotenv
from langchain_core.prompts import PromptTemplate
from langchain_openai import ChatOpenAI
from langchain_ollama import ChatOllama
from third_parties.linkedin import scrape_linkedin_profile
from agents.linkedin_lookup import lookup as linkedin_lookup_agent
from typing import Optional, Tuple


load_dotenv()  

def ice_breake_with(name:str) -> Tuple[Summary, str]:
    """
    Generate ice breakers for a person based on their LinkedIn profile.
    
    Args:
        name (str): Full name of the person to research
        
    Returns:
        Tuple[Summary, str]: Summary object and photo URL
    """

    linedin_username = linkedin_lookup_agent(name=name)
    print("Scraping LinkedIn data...")
    linkedin_data = scrape_linkedin_profile(
        linkedin_profile_url=linedin_username, 
        mock=False
        )
    print("LinkedIn data retrieved!")
    print(f"Found LinkedIn: {linedin_username}")

   
    template = """
    Based on this LinkedIn profile data: {name_of_person}
    1. Extract prifile picture URL
    2. Create a brief summary of this person's professional background.
    3. Give me 2 interesting facts about the person.
    4. Offer 3 ice-breaking question for the convertation beginning
    5. Show me interests of this person
    \n{format_instructions}
    """
    summary_prompt_template = PromptTemplate(
        template=template,
        input_variables=['name_of_person'],
        partial_variables={"format_instructions":summry_parser.get_format_instructions()}
    )

    llm = ChatOllama(
        # model="qwen2.5:7b"
        model='llama3:latest'
    )
    # chain = summary_prompt_template | llm
    chain = summary_prompt_template | llm | summry_parser
    print("Invoking LLM...")
    res:Summary = chain.invoke(input={"name_of_person":linkedin_data})
    print("Done!")

    return res, linkedin_data.get("photoUrl", "")