from llm.openai_client import OpenAIClient

print("=" * 60)
print("Testing OpenAI Connection")
print("=" * 60)

client = OpenAIClient()

response = client.test_connection()

print()

print("Response:")

print(response)