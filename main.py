import argparse
import os

from dotenv import load_dotenv
from google import genai
from google.genai import types

from call_function import call_function
from config import available_functions, model_name, system_prompt

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
    model=model_name,
    contents=messages,
    config=types.GenerateContentConfig(
        tools=[available_functions],
        system_instruction=system_prompt,
        temperature=0),
)
if not response.usage_metadata:
    raise RuntimeError("Usage meta data not found")
prompt_tokens = response.usage_metadata.prompt_token_count
response_tokens = response.usage_metadata.candidates_token_count
if args.verbose:
    print(f"User prompt: {args.user_prompt}")
    print(f"Prompt tokens: {prompt_tokens}")
    print(f"Response tokens: {response_tokens}")
else:
    pass
if not response.function_calls:
    print("Response: ")
    print(response.text)
else:
    function_responses = []
    for function in response.function_calls:
        result = call_function(function, args.verbose)
        if (
            not result.parts
            or not result.parts[0].function_response
            or not result.parts[0].function_response.response
        ):
            raise RuntimeError(
                f"Empty function response for {
                    function.name}")
        if args.verbose:
            print(f"-> {result.parts[0].function_response.response}")
        function_responses.append(result.parts[0])
