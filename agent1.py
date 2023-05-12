from langchain.utilities import GoogleSerperAPIWrapper
from langchain.llms.openai import OpenAI
from langchain.agents import initialize_agent, Tool
from langchain.agents import AgentType

import os

os.environ['SERPER_API_KEY'] = "d204a3336877e5419f12e0e5d46ad6eb94e5dde1"



def ask_lc(prompt: str) -> str:

    llm = OpenAI(temperature=0, max_retries=2)
    search = GoogleSerperAPIWrapper()
    tools = [
        Tool(
            name="Intermediate Answer",
            func=search.run,
            description="useful for when you need to ask with search"
        )
    ]

    self_ask_with_search = initialize_agent(tools, llm, agent=AgentType.SELF_ASK_WITH_SEARCH, verbose=True)
    result = self_ask_with_search.run(prompt)
    return result


