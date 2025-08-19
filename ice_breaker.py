import os

from output_parser import summry_parser, Summary
from dotenv import load_dotenv
from langchain_core.prompts import PromptTemplate
from langchain_openai import ChatOpenAI
from langchain_ollama import ChatOllama
from third_parties.linkedin import scrape_linkedin_profile
from agents.linkedin_lookup import lookup_multiple as linkedin_lookup_agent
from typing import Optional, Tuple


load_dotenv()  

def ice_breake_with_url(linkedin_url: str):
    """Process ice breaker for a specific LinkedIn URL"""
    print(f"🔍 Processing selected URL: {linkedin_url}")
    
    try:
        # Scrape the selected profile
        linkedin_data = scrape_linkedin_profile(linkedin_profile_url=linkedin_url, mock=False)
        
        if linkedin_data is None:
            print("⚠️ Scraping failed, using mock data...")
            # Extract name from URL for mock data
            profile_id = linkedin_url.split('/in/')[-1].replace('-', ' ').title()
            linkedin_data = {
                "firstName": profile_id.split()[0] if profile_id.split() else "Professional",
                "lastName": profile_id.split()[-1] if len(profile_id.split()) > 1 else "",
                "headline": "Professional",
                "summary": "Experienced professional",
                "photoUrl": "https://via.placeholder.com/300x300"
            }
        
        # Use your existing ice breaker generation logic
        from output_parser import summry_parser, Summary
        from langchain_core.prompts import PromptTemplate
        from langchain_ollama import ChatOllama
        
        template = """
        You are a networking expert helping someone prepare to connect with a professional. 
        
        Based on this LinkedIn profile: {name_of_person}
        
        Create a personalized, engaging response that shows genuine interest:

        1. **Professional Summary** (2-3 sentences): Write a compelling overview that highlights what makes this person unique and interesting. Focus on their career journey, expertise, and professional impact.

        2. **Fascinating Insights** (2 specific facts): Share genuinely interesting details about their background that would spark curiosity. Look for unique experiences, impressive achievements, or interesting career transitions.

        3. **Conversation Starters** (3 thoughtful questions): Create engaging, specific questions that:
           - Show you've researched their background
           - Are open-ended and encourage detailed responses  
           - Relate to their specific expertise or recent projects
           - Go beyond generic "how did you get started" questions

        4. **Connection Topics**: List specific areas where meaningful professional conversations could develop.

        Make this feel like advice from someone who genuinely understands networking and wants to help make a great first impression!

        \n{format_instructions}
        """
        
        summary_prompt_template = PromptTemplate(
            template=template,
            input_variables=['name_of_person'],
            partial_variables={"format_instructions": summry_parser.get_format_instructions()}
        )

        llm = ChatOllama(
            model='llama3.2:3b',
            temperature=0.9,
            top_p=0.9,
            # repeat_penalty=1.1
        )
        
        chain = summary_prompt_template | llm | summry_parser
        print("🤖 Generating ice breakers...")
        res: Summary = chain.invoke(input={"name_of_person": linkedin_data})
        
        return res, linkedin_data.get("photoUrl", "")
        
    except Exception as e:
        print(f"❌ Error processing URL: {e}")
        # Return basic fallback
        from output_parser import Summary
        fallback = Summary(
            summary="Professional profile",
            facts=["Experienced professional", "Active on LinkedIn"],
            ice_breakers=["Tell me about your experience!", "What's your favorite project?", "How did you get started?"],
            topics_of_interest=["Professional development"]
        )
        return fallback, ""