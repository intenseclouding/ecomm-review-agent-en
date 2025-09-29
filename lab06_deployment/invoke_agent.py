import boto3
import json
from uuid import uuid4

client = boto3.client('bedrock-agentcore', region_name='us-east-1')
payload = json.dumps({
    "input": {"prompt": "Explain machine learning in simple terms"}
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
print("Agent Response:", response_data)