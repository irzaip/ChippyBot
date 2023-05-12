from langchain.llms import OpenAI
from langchain.prompts import PromptTemplate
from langchain.chains import LLMChain


import yaml

with open('outputs.yaml') as f:
    dropdown = yaml.safe_load(f)

with open('instruction.yaml') as f:
    instruction_option = yaml.safe_load(f)



pp = PromptTemplate(input_variables=['topik'], template="buatkan saya {topik}")

prompt = input("topik:")
llm=OpenAI(temperature=0.9)
title = LLMChain(llm=llm, prompt=pp, verbose=True)
print(title.run(prompt))

rasta = LLMChain()