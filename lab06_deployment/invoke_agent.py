import boto3
import json
from uuid import uuid4

def invoke_agentcore_runtime(review_data: dict):
    client = boto3.client('bedrock-agentcore', region_name='us-west-2')
    payload = json.dumps({
        "review_data": review_data
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
    review_data = {'review_id': 5, 'content': '이어폰 만만세', 'rating': 3, 'author': '정수연', 'timestamp': '2024-01-11 16:22'}
    response_data = invoke_agentcore_runtime(review_data)
    print("Agent Response:", response_data)
