import boto3
import json

def lambda_handler(event, context):
    try:
        # Extract the user's message from the API Gateway event
        body = json.loads(event['body'])
        user_message = body.get('message')

        if not user_message:
            return {
                'statusCode': 400,
                'body': json.dumps({'error': 'No message provided'})
            }

        # Initialize the Bedrock runtime client
        bedrock_runtime = boto3.client('bedrock-runtime', region_name='us-east-1') # Replace with your region

        # Prepare the payload for the Bedrock model (e.g., Anthropic Claude)
        # The exact format depends on the chosen model
        model_id = 'anthropic.claude-3-sonnet-20240229-v1:0' # Example model ID
        
        # Example for a Claude 3 model
        bedrock_body = json.dumps({
            "messages": [{"role": "user", "content": user_message}],
            "max_tokens": 1000,
            "temperature": 0.7
        })

        # Invoke the Bedrock model
        response = bedrock_runtime.invoke_model(
            modelId=model_id,
            contentType='application/json',
            accept='application/json',
            body=bedrock_body
        )

        # Parse the response from Bedrock
        response_body = json.loads(response['body'].read())
        
        # Extract the model's response (adjust based on model's output structure)
        bot_response = response_body['content'][0]['text']

        return {
            'statusCode': 200,
            'body': json.dumps({'response': bot_response})
        }

    except Exception as e:
        print(f"Error: {e}")
        return {
            'statusCode': 500,
            'body': json.dumps({'error': str(e)})
        }

