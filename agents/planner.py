from llm.wrapper import LLMNode

# Update the prompt to show the 'limit' argument
PLANNER_PROMPT = """
You are a Planner Agent. Your job is to break a user request into a series of steps.
Available Tools:
1. github_search(query: str, limit: int) - Find repositories. Default limit is 5.
2. get_weather(city: str) - Get current weather.

Output strictly valid JSON in this format:
{
    "plan": [
        {
            "step_id": 1,
            "tool": "github_search", 
            "arguments": {"query": "python agents", "limit": 5},
            "description": "Search for top 5 python agent repos"
        },
        {
            "step_id": 2,
            "tool": "get_weather",
            "arguments": {"city": "London"},
            "description": "Get weather in London"
        }
    ]
}
If no tool is needed for a step (e.g., summary), use "tool": "none".
"""

class PlannerAgent:
    def __init__(self):
        self.llm = LLMNode(PLANNER_PROMPT)

    def create_plan(self, user_request):
        print(f"--> Planner: Creating plan for '{user_request}'")
        return self.llm.generate(user_request, json_mode=True)