import os


def get_files_info(working_directory, directory="."):
    try:
        working_dir_abs = os.path.abspath(working_directory)
        target_dir = os.path.normpath(os.path.join(working_dir_abs, directory))
        valid_target_dir = os.path.normpath(os.path.commonpath(
            [working_dir_abs, target_dir])) == working_dir_abs
        if valid_target_dir:
            output = ["Result for current directory: "]
            files = os.listdir(target_dir)
            for file in files:
                file_path = os.path.normpath(
                    os.path.join(target_dir, file))
                file_info = f'- {file}: file_size={
                    os.path.getsize(file_path)} bytes, is_dir={
                    os.path.isdir(file_path)}'
                output.append(file_info)
            return "\n".join(output)

        else:
            return f'Error: Cannot list "{directory}" as it is outside the permitted working directory'
    except BaseException:
        return f'Error: "{directory}" is not a directory'


print(get_files_info("calculator"))
