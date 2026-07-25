from google import genai

client = genai.Client(api_key="REMOVED")

response = client.models.generate_content(
    model="gemini-2.0-flash",
    contents="Say only: Hello"
)

print(response.text)