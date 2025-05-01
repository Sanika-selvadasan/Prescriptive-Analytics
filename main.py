from dotenv import load_dotenv
load_dotenv()

import os
import io
from state import State, ActionPlanState
from typing import Literal
from PIL import Image as PILImage
from langgraph.graph import END, StateGraph, START
from langchain_core.runnables.graph import MermaidDrawMethod
from utilities import create_tool_node_with_fallback
from custom_tool import list_tables_tool,get_schema_tool, db_query_tool
from node import first_tool_call, model_get_schema, query_gen_node, model_check_query, action_plan, run_parse_required
from langgraph.types import Send




#Langsmith tracking
langchain_api_key = os.getenv('LANGCHAIN_API_KEY')
os.environ["LANGCHAIN_TRACING_V2"] = "true"
os.environ['LANGCHAIN_API_KEY'] = langchain_api_key


# Name of the nodes
FIRST_TOOL_CALL = "first_tool_call"
LIST_TABLE_TOOL = "list_tables_tool"
GET_SCEHEMA_TOOL = "get_schema_tool"
MODEL_GET_SCHEMA = "model_get_schema"
QUERY_GEN = "query_gen"
CORRECT_QUERY = "correct_query"
EXECUTE_QUERY = "execute_query"
ACTION_PLAN = "action_plan"
PARSE = 'run_parse_required'

# Define a conditional edge to decide whether to continue or end the workflow
def should_continue(state: State) -> Literal[ACTION_PLAN , CORRECT_QUERY , QUERY_GEN]:
    messages = state["messages"]
    last_message = messages[-1]
    areas_of_concern = []
    if getattr(last_message, "tool_calls", None):
        for tc in last_message.tool_calls:
            if tc["name"] == "AreasOfConcern":
                areas_of_concern_i = tc['args']['areas_of_concern']
                areas_of_concern += areas_of_concern_i
        return [Send(ACTION_PLAN, ac) for ac in areas_of_concern]
    if last_message.content.startswith("Error:"):
        return QUERY_GEN
    else:
        return CORRECT_QUERY


# ACTION_PLAN = "action_plan"


# ap_flow = StateGraph(ActionPlanState)
# ap_flow.add_node(ACTION_PLAN, action_plan)
# ap_flow.set_entry_point(ACTION_PLAN)
# ap_flow.add_edge(ACTION_PLAN, END)
# ap_flow_app = ap_flow.compile()



# Define a new graph
workflow = StateGraph(State)

workflow.add_node(FIRST_TOOL_CALL, first_tool_call)
workflow.add_node(LIST_TABLE_TOOL, create_tool_node_with_fallback([list_tables_tool]))
workflow.add_node(GET_SCEHEMA_TOOL, create_tool_node_with_fallback([get_schema_tool]))
workflow.add_node(
    MODEL_GET_SCHEMA,
    lambda state: {
        "messages": [
            # Debug: Print the state messages before invoking model_get_schema
            # print(f"Debug: model_get_schema invoked with state['messages']: {state['messages']}"),
            model_get_schema.invoke(state["messages"]),
        ],
    },
)
workflow.add_node(QUERY_GEN, query_gen_node)
workflow.add_node(CORRECT_QUERY , model_check_query)
workflow.add_node(EXECUTE_QUERY, create_tool_node_with_fallback([db_query_tool]))
workflow.add_node(ACTION_PLAN, action_plan)

# Specify the edges between the nodes
workflow.add_edge(START, FIRST_TOOL_CALL)
workflow.add_edge(FIRST_TOOL_CALL, LIST_TABLE_TOOL)
workflow.add_edge(LIST_TABLE_TOOL, MODEL_GET_SCHEMA)
workflow.add_edge(MODEL_GET_SCHEMA, GET_SCEHEMA_TOOL)
workflow.add_edge(GET_SCEHEMA_TOOL, QUERY_GEN)

workflow.add_conditional_edges(
    QUERY_GEN,
    should_continue,
)
workflow.add_edge(CORRECT_QUERY ,EXECUTE_QUERY)
workflow.add_edge(EXECUTE_QUERY, QUERY_GEN)
workflow.add_edge(ACTION_PLAN , END)

# Compile the workflow into a runnable
app = workflow.compile()


# Draw the graph as PNG
mermaid_png_bytes = app.get_graph().draw_mermaid_png(draw_method=MermaidDrawMethod.API)
img = PILImage.open(io.BytesIO(mermaid_png_bytes))
img.save("graph_modified.png") 


if __name__ == "__main__":
    messages = app.invoke(
        {"messages": [("user", "Limit to the GSMJIF division")]}
    )
    # json_str = messages["messages"][-1].tool_calls[0]["args"]["final_answer"]
    # print(f'\n\n\nFINAL OUPTUT : {json_str}\n\n\n')

