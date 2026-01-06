import os

MAX_CHARS = 10000


def get_file_content(working_directory, file_path):
    try:
        working_directory_abs = os.path.abspath(working_directory)
        target_file_path = os.path.normpath(
            os.path.join(working_directory_abs, file_path))
        valid_file_path = os.path.normpath(os.path.commonpath(
            [target_file_path, working_directory_abs])) == working_directory_abs
        if valid_file_path:
            content = ""
            try:
                with open(target_file_path) as f:
                    content += f.read(MAX_CHARS)
                    if f.read(1):
                        content += f'[...File "{file_path}" truncated at {MAX_CHARS} characters]'
                return content
            except BaseException:
                return f'Error: File not found or is not a regular file: "{file_path}"'

        else:
            return f'Error: Cannot read "{file_path}" as it is outside the permitted working directory'
    except BaseException:
        return f'Error: not a valid file'
