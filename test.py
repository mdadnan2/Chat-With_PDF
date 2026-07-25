from google import genai

client = genai.Client(api_key="REMOVED")

for model in client.models.list():
    print(model.name)