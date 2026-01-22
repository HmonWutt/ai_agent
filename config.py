
from google.genai import types

MAX_CHARS = 10000
WORKING_DIR = "./calculator"
MAX_ITERS = 20

model_name = "gemini-2.5-flash"
schema_get_files_info = types.FunctionDeclaration(
    name="get_files_info",
    description="Lists files in a specified directory relative to the working directory, providing file size and directory status",
    parameters=types.Schema(
        type=types.Type.OBJECT,
        properties={
            "directory": types.Schema(
                type=types.Type.STRING,
                description="Directory path to list files from, relative to the working directory (default is the working directory itself)",
            ),
        },
    ),
)

schema_get_file_content = types.FunctionDeclaration(
    name="get_file_content",
    description="Look for the stated file in the working directory and read the content of the file.",
    parameters=types.Schema(
        type=types.Type.OBJECT,
        properties={
            "file_path": types.Schema(
                type=types.Type.STRING,
                description="path of the file to read content from",
            ),
        },
        required=["file_path"],
    ))

schema_run_python_file = types.FunctionDeclaration(
    name="run_python_file",
    description="run python file",
    parameters=types.Schema(
        type=types.Type.OBJECT,
        properties={
            "file_path": types.Schema(
                type=types.Type.STRING,
                description="path of the file to read content from",
            ),
            "args": types.Schema(
                type=types.Type.ARRAY,
                items=types.Schema(type=types.Type.STRING,
                                   ),
                description="optional arguments",
            ),
        },
        required=[
            "file_path"],
    ))


schema_write_file = types.FunctionDeclaration(
    name="write_file",
    description="write content to file",
    parameters=types.Schema(
        type=types.Type.OBJECT,
        properties={
            "file_path": types.Schema(
                type=types.Type.STRING,
                description="path of the file to read content from",
            ),
            "content": types.Schema(
                type=types.Type.STRING,
                description="write given content to file",),
        },
        required=[
            "file_path", "content"],
    ))

available_functions = types.Tool(
    function_declarations=[
        schema_get_files_info,
        schema_get_file_content,
        schema_run_python_file, schema_write_file])
system_prompt = """
You are a helpful AI coding agent.

When a user asks a question or makes a request, make a function call plan. You can perform the following operations:

- List files and directories
- Read file contents
- Execute Python files with optional arguments
- Write or overwrite files
- Fix bugs

All paths you provide should be relative to the working directory. You do not need to specify the working directory in your function calls as it is automatically injected for security reasons.
"""
