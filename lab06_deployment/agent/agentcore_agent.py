from bedrock_agentcore import BedrockAgentCoreApp
from orchestrator.agent import comprehensive_analyzer

app = BedrockAgentCoreApp()

@app.entrypoint()
def invoke_agent(payload):
    response = comprehensive_analyzer(payload)
    return {"result": response}

if __name__ == "__main__":
    app.run()