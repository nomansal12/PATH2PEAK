import requests
import json
import os

# Set your API key (either directly or via environment variable)
api_key = "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"

# Ensure API key is present
if not api_key:
    raise ValueError("API key is not set. Please set the OPENAI_API_KEY environment variable.")

# Define the endpoint and headers
url = "https://api.openai.com/v1/chat/completions"
headers = {
    "Content-Type": "application/json",
    "Authorization": f"Bearer {api_key}"
}

# Define the payload (request data)
payload = {
    "model": "gpt-3.5-turbo",  # Replace with the correct model name
    "messages": [{"role": "user", "content": "Say this is a test!"}],
    "temperature": 0.7
}

# Send the POST request to the OpenAI API
response = requests.post(url, headers=headers, json=payload)

# Check if the request was successful
if response.status_code == 200:
    response_data = response.json()
    print("Response:", response_data['choices'][0]['message']['content'])
else:
    print(f"Error {response.status_code}: {response.text}")
