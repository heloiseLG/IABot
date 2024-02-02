from langchain.agents.agent_types import AgentType
from typing_extensions import Required, NotRequired
from langchain_experimental.agents.agent_toolkits import create_pandas_dataframe_agent
from langchain_openai import ChatOpenAI
from langchain_experimental.agents import create_pandas_dataframe_agent
import pandas as pd
import os

OPENAI_API_KEY = os.environ.get("OPENAI_API_KEY")

df = pd.read_json("Data.json")

agent = create_pandas_dataframe_agent(
    ChatOpenAI(openai_api_key = OPENAI_API_KEY, temperature=0, model="gpt-3.5-turbo-0613"),
    df,
    verbose=True,
    agent_type=AgentType.OPENAI_FUNCTIONS,
)

agent.run("Donne moi le titre de la première oeuvre ?")