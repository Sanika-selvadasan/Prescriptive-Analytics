from state import State, ActionPlanState
from langchain_core.messages import AIMessage, ToolMessage
from prompts import query_check, query_gen, action_plan_llm
from langchain_openai import ChatOpenAI
from custom_tool import get_schema_tool
from parsers import areas_of_concern_parser, AreaOfConcern


# First tool call to list the tables
def first_tool_call(state: State) -> dict[str, list[AIMessage]]:
    ai_tool_call = [
            AIMessage(
                content="",
                tool_calls=[
                    {
                        "name": "sql_db_list_tables",
                        "args": {},
                        "id": "tool_abcd123",
                    }
                ],
            )
        ]
    list_tables = {"messages": ai_tool_call}
    return list_tables


# Add a node for a model to choose the relevant tables based on the question and available tables
model_get_schema = ChatOpenAI(model="gpt-4o", temperature=0).bind_tools([get_schema_tool])


#check if the query is correct before executing query
def model_check_query(state: State) -> dict[str, list[AIMessage]]:
    """
    Use this tool to double-check if your query is correct before executing it.
    """
    messages = [query_check.invoke({state["messages"][-1].content})]
    print(f'\n\n\nCORRECT_QUERY_OUTPUT: "messages": {messages}\n\n\n')
    return {"messages": messages}


#Generate sql query
def query_gen_node(state: State):
    message = query_gen.invoke(state)
    print(f'\n\n\nQUERYGEN_OUTPUT: {message}\n\n\n')

    # Sometimes, the LLM will hallucinate and call the wrong tool. We need to catch this and return an error message.
    tool_messages = []
    areas_of_concern = []
    if message.tool_calls:
        for tc in message.tool_calls:
            if tc["name"] != "AreasOfConcern":
                tool_messages.append(
                    ToolMessage(
                        content=f"Error: The wrong tool was called: {tc['name']}. Please fix your mistakes. Remember to only call AreasOfConcern to submit the final answer. Generated queries should be outputted WITHOUT a tool call.",
                        tool_call_id=tc["id"],
                    )
                )
            else:
                areas_of_concern_i = tc['args']['areas_of_concern']
                areas_of_concern += areas_of_concern_i
    else:
        tool_messages = []
    return {"messages": [message] + tool_messages,
            "areas_of_concern": areas_of_concern}


# Format the output data
def action_plan(state: AreaOfConcern):
    response = action_plan_llm.invoke(state)
    if response.tool_calls:
        print(f"Division, Coverage, Type: {state['division']}, {state['coverage']}, {state['type']}")
        return {"action_plans": [{"action_items": response.tool_calls[0]["args"]["action_items"],
                                  "area_of_concern": state}]}
    else:
        return {"action_plans": []}



def run_parse_required(state: State):
    final_answer = state["agent_outcome"]
    required_data = areas_of_concern_parser.parse(final_answer)
    return {"required_data": required_data}
