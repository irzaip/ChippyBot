from langchain import OpenAI
import os

llm = OpenAI(
    openai_api_key=os.environ['OPENAI_API_KEY'],
    temperature=0
)

from langchain.callbacks import get_openai_callback

def count_tokens(agent, query):
    with get_openai_callback() as cb:
        result = agent(query)
        print(f'Spent a total of {cb.total_tokens} tokens')

    return result

from sqlalchemy import MetaData

metadata_obj = MetaData()

from sqlalchemy import Column, Integer, String, Table, Date, Float

stocks = Table(
    "stocks",
    metadata_obj,
    Column("obs_id", Integer, primary_key=True),
    Column("stock_ticker", String(4), nullable=False),
    Column("price", Float, nullable=False),
    Column("date", Date, nullable=False),    
)

from sqlalchemy import create_engine

engine = create_engine("sqlite:///:memory:")
metadata_obj.create_all(engine)

from datetime import datetime

observations = [
    [1, 'ABC', 200, datetime(2023, 1, 1)],
    [2, 'ABC', 208, datetime(2023, 1, 2)],
    [3, 'ABC', 232, datetime(2023, 1, 3)],
    [4, 'ABC', 225, datetime(2023, 1, 4)],
    [5, 'ABC', 226, datetime(2023, 1, 5)],
    [6, 'XYZ', 810, datetime(2023, 1, 1)],
    [7, 'XYZ', 803, datetime(2023, 1, 2)],
    [8, 'XYZ', 798, datetime(2023, 1, 3)],
    [9, 'XYZ', 795, datetime(2023, 1, 4)],
    [10, 'XYZ', 791, datetime(2023, 1, 5)],
]

from sqlalchemy import insert

def insert_obs(obs):
    stmt = insert(stocks).values(
    obs_id=obs[0], 
    stock_ticker=obs[1], 
    price=obs[2],
    date=obs[3]
    )

    with engine.begin() as conn:
        conn.execute(stmt)

for obs in observations:
    insert_obs(obs)

from langchain.sql_database import SQLDatabase
from langchain.chains import SQLDatabaseChain

db = SQLDatabase(engine)
sql_chain = SQLDatabaseChain(llm=llm, database=db, verbose=True)

from langchain.agents import Tool

sql_tool = Tool(
    name='Stock DB',
    func=sql_chain.run,
    description="Useful for when you need to answer questions about stocks " \
                "and their prices."
    
)


from langchain.agents import load_tools

tools = load_tools(
    ["llm-math"], 
    llm=llm
)

tools.append(sql_tool)

from langchain.agents import initialize_agent

zero_shot_agent = initialize_agent(
    agent="zero-shot-react-description", 
    tools=tools, 
    llm=llm,
    verbose=True,
    max_iterations=3,
)

result = count_tokens(
    zero_shot_agent, 
    "What is the multiplication of the ratio between stock prices for 'ABC' and 'XYZ' in January 3rd and the ratio between the same stock prices in January the 4th?"
)