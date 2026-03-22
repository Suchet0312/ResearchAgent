from google import genai
import os
from dotenv import load_dotenv

load_dotenv()

client = genai.Client(api_key="AIzaSyBpgZk8B1o5zMYfYYCI5DtffFEuXJXarXQ")

response = client.models.generate_content(
    model="gemini-2.0-flash",
    contents="Say hello in one word"
)

print(response.text)