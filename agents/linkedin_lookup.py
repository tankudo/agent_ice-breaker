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


def lookup (name: str) -> str:
    llm = ChatOllama(
        model="llama3.2:3b",
        temperature=0
    )
    template = """
    given the full name person {name_of_person} I want you to get it me a link to their 
    LinkedIn profile page. Your answer should contain only a URL
    """
    prompt_template = PromptTemplate(
        template=template,
        input_variables=['name_of_person'],
    )
    tools_for_agent = [
        Tool(
            name="Crawl Google 4 LinkedIn profile page",
            func=lambda x: get_profile_url_tavily(f"{x} site:linkedin.com/in"), 
            description="Search specifically for LinkedIn profile URLs (not directory pages)"
        )
    ]
    react_promt = hub.pull(
        "hwchase17/react"
    )
    agent = create_react_agent(llm=llm, tools=tools_for_agent, prompt=react_promt)
    agent_executer = AgentExecutor(
        agent=agent, 
        tools=tools_for_agent, 
        verbose=True,
        handle_parsing_errors=True,
        # max_iterations=3,
        return_intermediate_steps=True
        )
    result = agent_executer.invoke(
        input={"input": prompt_template.format(name_of_person=name)} 
    )
    linkedin_profile_url = result["output"]
    print(f"🔗 Agent output: {linkedin_profile_url}")

    if "iteration limit" in linkedin_profile_url.lower() or "time limit" in linkedin_profile_url.lower():
        print("🔄 Agent hit limit, checking intermediate steps...")
        # Look for URL in the search results from intermediate steps
        for step in result.get("intermediate_steps", []):
            if len(step) > 1 and "linkedin.com/in/" in str(step[1]):
                import re
                pattern = r'https://www\.linkedin\.com/in/[a-zA-Z0-9\-_]+/?'
                matches = re.findall(pattern, str(step[1]))  # Use step[1] instead of 'text'
                if matches:
                    linkedin_profile_url = matches[0].rstrip('/')
                    print(f"✅ Found URL in intermediate steps: {linkedin_profile_url}")
                    break

    return linkedin_profile_url
