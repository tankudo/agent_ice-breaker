from dotenv import load_dotenv
from langchain.agents import tool
from langchain.prompts import PromptTemplate
from langchain.tools.render import render_text_description
from langchain.agents.output_parsers import ReActSingleInputOutputParser
from langchain.agents import AgentExecutor, create_react_agent
from langchain_ollama import ChatOllama
from langchain.agents.format_scratchpad import format_log_to_str
import os
load_dotenv()

@tool
def get_lext_length(text:str) -> int:
    """
    Return the text length
    """
    text = text.strip("'/n").strip('"')
    return len(text)

@tool
def add_numbers(expression: str) -> int:
    """Add numbers like '3 + 2' or '5 + 10'"""
    try:
        # Clean the input and evaluate
        clean_expr = expression.strip().strip("'\"")
        result = eval(clean_expr)
        return int(result)
    except Exception as e:
        return f"Error: {e}"

def run_agent_loop(agent, tools_map, question, max_steps=5):
    intermediate_steps = []
    final_thought = None
    
    for step in range(max_steps):
        print(f"\n--- STEP {step + 1} ---")
        try:
            res = agent.invoke({
                "input": question,
                "intermediate_steps": intermediate_steps
            })
        except Exception as e:
            error_msg = str(e)
            if "Could not parse LLM output:" in error_msg:
                failed_output = error_msg.split("Could not parse LLM output: `")[1].split("`")[0]
                final_thought = failed_output.strip()
                print("Agent completed task")
                # print(f"Captured final thought: {final_thought}")
    
                # Extract just the thought line
                lines = failed_output.split('\n')
                for line in lines:
                    if line.strip().startswith('Thought:'):
                        final_thought = line.strip()
                break
            else:
                final_thought = failed_output.strip()
                break
        
        if hasattr(res, 'return_values'):  # AgentFinish
            print(f"Final Answer: {res.return_values['output']}")
            break
            
        elif hasattr(res, 'tool'):  # AgentAction
            print(f"Tool: {res.tool}")
            print(f"Input: {res.tool_input.strip()}")
            
            # Execute tool
            tool_input = res.tool_input.strip()
            result = tools_map[res.tool].invoke(tool_input)
            print(f"Result: {result}")
            
            # Add to history
            intermediate_steps.append((res, result))
        
        else:
            print("Unexpected response, stopping")
            break
    
    return intermediate_steps, final_thought

def main():
    tools = [get_lext_length, add_numbers]
    tools_map = {tool.name: tool for tool in tools}
    template = """
    Answer the following questions as best you can. You have access to the following tools:

    {tools}

    Use the following format:

    Question: the input question you must answer
    Thought: you should always think about what to do
    Action: the action to take, should be one of [{tool_names}]
    Action Input: the input to the action
    Observation: the result of the action
    ... (this Thought/Action/Action Input/Observation can repeat N times)
    Thought: I now know the final answer
    Final Answer: the final answer to the original input question

    Begin!

    Question: {input}
    Thought:{agent_scratchpad}
        """

    prompt = PromptTemplate.from_template(template=template).partial(tools=render_text_description(tools), tool_names= ", ".join([t.name for t in tools]))
    llm = ChatOllama(temperature=0, model="llama3.1:8b", stop=["Observation:", "Final Answer:", "\nThought:"])

    agent = {
        "input": lambda x: x["input"], 
        "agent_scratchpad": lambda x: format_log_to_str(x.get("intermediate_steps", []))
        } | prompt | llm | ReActSingleInputOutputParser()
    # question = "What is the length of 'Dog' plus 2?"
    question = "Hoe much 3 + 2?"

    intermediate_steps = []
    print(f"❓ Question: {question}")

    # res = agent.invoke({"input": question, "intermediate_steps": intermediate_steps})

    intermediate_steps, final_thought = run_agent_loop(agent, tools_map, question)

    print(f"\n---SUMMARY---:")
    print(f"Steps taken: {len(intermediate_steps)}")

    for i, (action, result) in enumerate(intermediate_steps):
        print(f"Step {i+1}: {action.tool} -> {result}")

    if final_thought:
        print(f"{final_thought}")

if __name__ == '__main__':
    main()

    
