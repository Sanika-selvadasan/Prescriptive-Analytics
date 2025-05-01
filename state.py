from langgraph.graph.message import AnyMessage, add_messages
from typing import Annotated
from typing_extensions import TypedDict, Union
from parsers import AreasOfConcern, ActionPlan
import operator


class ActionPlanState(TypedDict):
    messages: Annotated[list[AnyMessage], add_messages]
    coverage: Union[str, None]
    division: Union[str, None]
    type: Union[str, None]
    action_plans: Union[list[str], None]


# Define the state for the agent
class State(TypedDict):
    messages: Annotated[list[AnyMessage], add_messages]
    agent_outcome: Union[str, None]
    areas_of_concern: Union[list[AreasOfConcern], None]
    action_plans: Annotated[list[ActionPlan], operator.add]
    
