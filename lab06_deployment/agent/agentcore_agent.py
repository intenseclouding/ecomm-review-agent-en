from bedrock_agentcore import BedrockAgentCoreApp
from agent.orchestrator.agent import comprehensive_analyzer

app = BedrockAgentCoreApp()

@app.entrypoint
def invoke_agent(payload):
    user_prompt = payload.get("prompt", "Hello! How can I help you today?")
    response = comprehensive_analyzer(user_prompt)
    return {"result": response}

if __name__ == "__main__":
    app.run()