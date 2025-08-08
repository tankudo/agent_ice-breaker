import os
from dotenv import load_dotenv
from langchain_core.prompts import PromptTemplate
from langchain_openai import ChatOpenAI
from langchain_ollama import ChatOllama
from third_parties.linkedin import scrape_linkedin_profile
from agents.linkedin_lookup import lookup as linkedin_lookup_agent

load_dotenv()  

def ice_breake_with(name:str) -> str:
    linedin_username = linkedin_lookup_agent(name=name)
    print("Scraping LinkedIn data...")
    linkedin_data = scrape_linkedin_profile(
        linkedin_profile_url=linedin_username, 
        mock=True
        )
    print("LinkedIn data retrieved!")
    print(f"Found LinkedIn: {linedin_username}")

   
    template = """
    Based on this LinkedIn profile data: {name_of_person} 
    1. Create 3 personalized ice breaker conversation starters for networking.
    2. Give me 2 facts anout the person.
    """
    summary_prompt_template = PromptTemplate(
        template=template,
        input_variables=['name_of_person'],
    )

    llm = ChatOllama(
        model="qwen2.5:7b"
    )
    chain = summary_prompt_template | llm
    print("Invoking LLM...")
    res = chain.invoke(input={"name_of_person":linkedin_data})
    print("Done!")

    return res.content

if __name__ == '__main__':
    load_dotenv()
    print("Ice Break!")
    result = ice_breake_with(name="Vera Bereczky")  # Store the result
    print(result.content)
    # print("Ice breaker enter")
    # # print(os.environ['OPENAI_API_KEY'])
    # summary_template = """
    #                     Given the LinkedIn information {information}, create:
    #                     1. A conversational ice breaker question
    #                     2. Two interesting conversation starters
    #                     3. Common interests or background we might share

    #                 Make it natural and engaging for networking!
    #                     """
    # summary_prompt_template = PromptTemplate(input_variables={"information"}, template=summary_template)
    # # llm = ChatOpenAI(temperature=0, model_name="gpt-3.5-turbo")
    # llm = ChatOllama(model="qwen2.5:7b")
    # # llm = ChatOllama(model="mistral")
    # chain = summary_prompt_template | llm 
    # linkedinUrl = "https://www.linkedin.com/in/ankudo"
    # linkedIn_data = scrape_linkedin_profile(linkedinUrl)
    # res = chain.invoke(input={"information":linkedIn_data})
    # print(res.content)
            