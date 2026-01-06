import os
from pathlib import Path


def write_file(working_directory, file_path, content):
    try:
        working_directory_abs = os.path.abspath(working_directory)
        target_file_path = os.path.normpath(
            os.path.join(working_directory_abs, file_path))
        if os.path.normpath(os.path.commonpath(
                [working_directory_abs, target_file_path])) == working_directory_abs:
            path = Path(target_file_path)
            if path.exists() and path.is_dir():
                return f'Error: Cannot write to "{file_path}" as it is a directory'
            try:
                os.makedirs(
                    os.path.dirname(working_directory_abs),
                    exist_ok=True)
            except BaseException:
                return f'Error: Directory {file_path} cannot be created'
            try:
                with open(target_file_path, "w") as f:
                    f.write(content)
                return f'Successfully wrote to "{file_path}" ({
                    len(content)} characters written)'
            except BaseException:
                return f'Error: writing to "{file_path}" failed'

        else:
            return f'Error: Cannot write to "{file_path}" as it is outside the permitted working directory'
    except BaseException:
        return f'Error: something went wrong'
