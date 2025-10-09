from strands import Agent


def comprehensive_analyzer(prompt):
    agent = Agent(model="us.anthropic.claude-3-7-sonnet-20250219-v1:0")
    response = agent(prompt)
    return response
