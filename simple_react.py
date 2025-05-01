from dotenv import load_dotenv

load_dotenv()
from datetime import datetime
from langchain_openai import ChatOpenAI
from langgraph.prebuilt import create_react_agent
from langchain_core.prompts import ChatPromptTemplate
prompt = ChatPromptTemplate.from_messages([
     ("system", "You are a helpful bot named Fred."),
     ("placeholder", "{messages}"),
     ("system", "Remember, always be polite!"),
])


def check_weather(location: str, at_time: datetime | None = None) -> str:
    '''Return the weather forecast for the specified location.'''
    return f"It's always sunny in {location}"

tools = [check_weather]
model = ChatOpenAI(model="gpt-4o")
graph = create_react_agent(model, tools=tools, prompt=prompt)
inputs = {"messages": [("user", "what is the weather in sf")]}
for s in graph.stream(inputs, stream_mode="values"):
    message = s["messages"][-1]
    if isinstance(message, tuple):
        print(message)
    else:
        message.pretty_print()