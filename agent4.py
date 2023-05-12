from langchain import PromptTemplate, HuggingFaceHub, LLMChain

fl = HuggingFaceHub(
    repo_id="mrm8488/bertin-gpt-j-6B-ES-8bit",
    model_kwargs={"temperature":1e-10}
)

template = """Question: {question}

Answer: """
prompt = PromptTemplate(template=template, input_variables=["question"])

llm_chain = LLMChain(
    prompt=prompt,
    llm = fl,
)

question="Who is the leader of Nigeria?"

print(llm_chain.run(question))
