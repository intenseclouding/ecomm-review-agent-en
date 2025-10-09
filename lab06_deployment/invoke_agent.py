import boto3
import json
from uuid import uuid4

def invoke_agentcore_runtime(prompt: dict):
    client = boto3.client('bedrock-agentcore', region_name='us-west-2')
    payload = json.dumps({
        "input": prompt
    })

    runtime_arn = "<your-runtime-agent>"
    session_id = str(uuid4())

    response = client.invoke_agent_runtime(
        agentRuntimeArn=runtime_arn,
        runtimeSessionId=session_id,  # Must be 33+ chars
        payload=payload
    )

    response_body = response['response'].read()
    response_data = json.loads(response_body)
    return response_data
    
if __name__ == "__main__":
    response_data = invoke_agentcore_runtime({"prompt": "Explain machine learning in simple terms"})
    print("Agent Response:", response_data)
