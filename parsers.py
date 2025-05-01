from pydantic import BaseModel, Field
from langchain_core.output_parsers import PydanticOutputParser


# Describe a tool to represent the end state
class SubmitFinalAnswer(BaseModel):
    """Submit the final answer to the user based on the query results."""
    final_answer: str = Field(..., description="The final answer to the user")


class QueryCheck(BaseModel):
    """ Return the SQL query after analysing the output."""
    sql_query: str = Field(description="SQL query")


class AreaOfConcern(BaseModel):
    """ This is an area of Concern comprising of Division and Coverage"""
    division: str = Field(description="Name of the Divisions")
    coverage: str = Field(description="Name of the Coverages")
    type: str = Field(description="Type of the Area of Concern - Frequency or Severity")
    reason: str = Field(description="Reason for the Area of Concern")
    evidence: str = Field(description="Evidence for the Area of Concern")


class AreasOfConcern(BaseModel):
    """This is a list of Areas of Concern, which are pairs of Division and Coverage"""
    areas_of_concern: list[AreaOfConcern] = Field(description="List of Areas of Concern")
    

class ActionPlan(BaseModel):
    """This is the final action plan to be submitted to the user"""
    action_items: list[str] = Field(description="List of Action Items")
    area_of_concern: AreaOfConcern = Field(description="Area of Concern")


areas_of_concern_parser = PydanticOutputParser(pydantic_object=AreasOfConcern)
query_out = PydanticOutputParser(pydantic_object=QueryCheck)
action_plan_parser = PydanticOutputParser(pydantic_object=ActionPlan)

