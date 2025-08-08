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
        model="qwen2.5:7b"
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
            func=get_profile_url_tavily,
            description="useful for when you need get the LinkedIn page URL"
        )
    ]
    react_promt = hub.pull(
        "hwchase17/react"
    )
    agent = create_react_agent(llm=llm, tools=tools_for_agent, prompt=react_promt)
    agent_executer = AgentExecutor(agent=agent, tools=tools_for_agent, vebrese=True)
    result = agent_executer.invoke(
        input={"input": prompt_template.format_prompt(name_of_person=name)}
    )
    linkedin_profile_url = result["output"]

    return linkedin_profile_url

if __name__ == "__main__":
    linkedin_url = lookup(name="Nikos Kotoupas")
    print(linkedin_url)
