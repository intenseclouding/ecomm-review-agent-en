from bedrock_agentcore.runtime import BedrockAgentCoreApp
from strands import Agent
from strands.models import BedrockModel
from pydantic import BaseModel

SYSTEM_PROMPT="""
Check if this review is okay for diplay
"""

class AnalysisResult(BaseModel):
    is_okay: bool

bedrock_model = BedrockModel(
    model_id="us.anthropic.claude-3-5-sonnet-20241022-v2:0",
    region_name="us-west-2",
    temperature=0.3,
)

# @tools
# def save_review_analysis_result():
#     return 

app = BedrockAgentCoreApp()
agent = Agent(
    model=bedrock_model,
    system_prompt=SYSTEM_PROMPT
)

@app.entrypoint
def invoke(payload):
    """Process user input and return a response"""
    print(payload)
    user_message = payload.get("input", "My name is Steve. What is my name?")
    print(user_message)
    result = agent.structured_output(
        output_model=AnalysisResult,
        prompt = user_message
    )
    return {"result": result}

if __name__ == "__main__":
    app.run()