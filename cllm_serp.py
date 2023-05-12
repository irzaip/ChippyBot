
from langchain import OpenAI
import os


llm = OpenAI(
    openai_api_key= os.environ['OPENAI_API_KEY'],  # platform.openai.com
    temperature=0,
    model_name="text-davinci-003"
)


from langchain.chains import LLMMathChain
from langchain.agents import Tool
import os

llm_math = LLMMathChain(llm=llm)

# initialize the math tool
math_tool = Tool(
    name='Calculator',
    func=llm_math.run,
    description='Useful for when you need to answer questions about math.'
)
# when giving tools to LLM, we must pass as list of tools
tools = [math_tool]

tools[0].name, tools[0].description


from langchain.agents import initialize_agent

zero_shot_agent = initialize_agent(
	agent="zero-shot-react-description",
	tools=tools,
	llm=llm,
	verbose=True,
	max_iterations=3
)
     
zero_shot_agent("what is (4.5*2.1)^2.2?")
 