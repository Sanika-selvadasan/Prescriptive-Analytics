# Prescriptive Analytics for Insurance Data
This project is a Streamlit-based application that uses LangChain, OpenAI's GPT models, and SQL database integration to perform prescriptive analysis on insurance datasets. The tool identifies key areas of concern based on frequency or severity of claims and generates actionable recommendations.


 ## The Purpose

Imagine you’re buried under piles of insurance claims, trying to spot trends and figure out what to do next. Instead of chugging coffee and crying over pivot tables, let our app:


Read your insurance data

Identify pain points (frequency, severity, etc.)

Generate rational, explainable, and actionable recommendations

Present it all in a Streamlit dashboard


It's like having a data scientist and an insurance strategist rolled into one — and neither of them complains about meetings.

## File Index (aka Who Does What?)
app.py: Launches the Streamlit UI

main.py: Orchestrates the AI-driven workflow

db.py: Uploads Excel/CSV files into SQLite

custom_tool.py: SQL magic using LangChain tools

node.py: Brains of the operation (logic nodes)

parsers.py: Data models for structure and sanity

prompts.py: Templated messages for LLM guidance

state.py: Defines LangGraph’s shared memory

utilities.py: Helper tools and graceful error handling
