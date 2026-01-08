import os
import subprocess
import time


def run_python_file(working_directory, file_path, args=None):
    try:
        working_dir_abs = os.path.abspath(working_directory)
        target_path = os.path.normpath(
            os.path.join(working_dir_abs, file_path))
        is_in_dir = os.path.normpath(
            os.path.commonpath(
                [target_path,
                 working_dir_abs])) == working_dir_abs
        if is_in_dir:
            if os.path.isfile(target_path):
                if file_path.endswith("py"):
                    command = ["python", file_path]
                    if args:
                        command.extend(args)
                    completed_process = subprocess.run(
                        command, capture_output=True, text=True)
                    time.sleep(30)
                    if completed_process.returncode == 0:
                        if not completed_process.stdout:
                            return "No output produced"
                        return f"STDOUT: {completed_process.stdout}"
                    result = f"Process exited with code {
                        completed_process.returncode} "

                    return result + f"STDERR: {completed_process.stderr}"
                return f'Error: "{file_path}" is not a Python file'
            return f'Error: "{file_path}" does not exist or is not a regular file'
        return f'Error: Cannot execute "{file_path}" as it is outside the permitted working directory'
    except (BaseException) as e:
        return f"Error: executing Python file: {e}"
