import os
import subprocess


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
                    result = subprocess.run(
                        command,
                        cwd=working_dir_abs,
                        capture_output=True,
                        text=True,
                        timeout=30,
                    )
                    output = []
                    if result.returncode != 0:
                        output.append(
                            f"Process exited with code {
                                result.returncode}")
                    if not result.stdout and not result.stderr:
                        output.append("No output produced")
                    if result.stdout:
                        output.append(f"STDOUT:\n{result.stdout}")
                    if result.stderr:
                        output.append(f"STDERR:\n{result.stderr}")
                    return "\n".join(output)
                return f'Error: "{file_path}" is not a Python file'
            return f'Error: "{file_path}" does not exist or is not a regular file'
        return f'Error: Cannot execute "{file_path}" as it is outside the permitted working directory'
    except (BaseException) as e:
        return f"Error: executing Python file: {e}"


print(run_python_file("./calculator", "tests.py"))
