from smolagents import OpenAIModel,ToolCallingAgent, CodeAgent, DuckDuckGoSearchTool, FinalAnswerTool, InferenceClientModel, load_tool, tool
from datetime import date
from openai import OpenAI

@tool
def get_current_date() -> date:
    """A tool that return current date"""
    return date.today()

@tool
def add_numbers(a: int, b: int) -> int:
    """
    Adds two integers and returns the result.

    Args:
        a: The first number to add.
        b: The second number to add.
    """
    return a + b

final_answer=FinalAnswerTool()
search = DuckDuckGoSearchTool()

model=OpenAIModel(
    model_id="gpt-4.1-mini"
)

agent=ToolCallingAgent(
    model=model,
    tools=[final_answer, add_numbers,get_current_date],
    max_steps=5,
)

agent_code=CodeAgent(
    model=model,
    tools=[final_answer, search,add_numbers,get_current_date],
    max_steps=5
)


#result = agent_code.run("Calculate the sum of the day of the month and the number of the month of the current date. For example, for the date 24-5-6, you will return 11. (Day - 6, Month - 5. 5+6=11)")
result = agent_code.run("Who is the president of the United States, and how old was he two years ago?")

print(result)