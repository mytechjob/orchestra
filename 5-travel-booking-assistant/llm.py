from langchain_openai import ChatOpenAI
from os import getenv

llm = ChatOpenAI(model="gpt-5-nano", api_key=getenv("OPENAI_API_KEY"))
