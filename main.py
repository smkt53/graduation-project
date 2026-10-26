print("Hello, World!")

from dotenv import load_dotenv
from google import genai
load_dotenv()

import os

KEY_API = os.getenv("KEY_API")

print("KEY_API:", KEY_API)

client =genai.Client(api_key=KEY_API)

interaction = client.interactions.create(
    model="gemini-3.8-flash",
    input="日本語対応していますか？"
)

print(interaction.output_text)