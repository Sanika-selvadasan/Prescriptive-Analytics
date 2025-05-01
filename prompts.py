
from langchain_openai import ChatOpenAI
from langchain import hub
from custom_tool import db_query_tool
from parsers import ActionPlan, areas_of_concern_parser, query_out, AreasOfConcern

query_check_prompt = hub.pull("query_check_system")
query_check = query_check_prompt | ChatOpenAI(model="gpt-4o", temperature=0).bind_tools(
    [db_query_tool], tool_choice="required"
)

query_gen_prompt = hub.pull("query_gen_system")
query_gen_prompt = query_gen_prompt.partial(format_instructions = query_out.get_format_instructions() )
query_gen = query_gen_prompt | ChatOpenAI(model="gpt-4o", temperature=0).bind_tools(
    [AreasOfConcern]
)

format_output_prompt = hub.pull("format_output_prompt")
prompt = format_output_prompt.partial(format_instructions =areas_of_concern_parser.get_format_instructions())
final_out = prompt | ChatOpenAI(model="gpt-4o", temperature=0)


action_plan_prompt = hub.pull("action_plan_prompt")
action_plan_llm = action_plan_prompt | ChatOpenAI(model="gpt-4o", temperature=0).bind_tools(
    [ActionPlan]
)
