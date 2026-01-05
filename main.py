import argparse
import os

from dotenv import load_dotenv
from google import genai
from google.genai import types

parser = argparse.ArgumentParser(description="Chatbot")
parser.add_argument("user_prompt", type=str, help="User prompt")
parser.add_argument(
    "--verbose",
    action="store_true",
    help="Enable verbose output")
args = parser.parse_args()
messages = [
    types.Content(
        role="user", parts=[
            types.Part(
                text=args.user_prompt)])]
load_dotenv()
api_key = os.environ.get("GEMINI_API_KEY")
if not api_key:
    raise RuntimeError("API key not found")
client = genai.Client(api_key=api_key)
response = client.models.generate_content(
    model='gemini-2.5-flash',
    contents=messages
)
if not response.usage_metadata:
    raise RuntimeError("Usage meta data not found")
prompt_tokens = response.usage_metadata.prompt_token_count
response_tokens = response.usage_metadata.candidates_token_count
if args.verbose:
    print(f"Prompt tokens: {prompt_tokens}")
    print(f"Response tokens: {response_tokens}")
else:
    pass
print(response.text)
