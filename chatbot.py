from langchain.agents.agent_types import AgentType
from typing_extensions import Required, NotRequired
from langchain_experimental.agents.agent_toolkits import create_pandas_dataframe_agent
from langchain_openai import OpenAI
from langchain_openai import ChatOpenAI
from langchain_experimental.agents import create_pandas_dataframe_agent
import pandas as pd

openai_api_key = "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"

df = pd.read_json("Data.json")

agent = create_pandas_dataframe_agent(
    ChatOpenAI(openai_api_key = openai_api_key, temperature=0, model="gpt-3.5-turbo-0613"),
    df,
    verbose=True,
    agent_type=AgentType.OPENAI_FUNCTIONS,
)

agent.run("Quel est le deuxième Titre ? et quelle est sa Date de découverte ?")
