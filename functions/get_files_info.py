import os
from google.genai import types


def get_files_info(working_directory, directory="."):
    cur_path = os.path.join(working_directory, directory)
    abs_working_dir = os.path.abspath(working_directory)
    abs_cur_path = os.path.abspath(cur_path)

    # VALIDATIONS
    if os.path.commonpath([abs_working_dir, abs_cur_path]) != abs_working_dir:
        return f'Error: Cannot list "{directory}" as it is outside the permitted working directory'

    if not os.path.isdir(cur_path):
        return f'Error: "{directory}" is not a directory'

    # GET FILES INFO
    contents = os.listdir(cur_path)
    for_print = []
    for idx, item in enumerate(contents):

        def get_directory_size(start_path):
            total_size = 0
            for dirpath, dirnames, filenames in os.walk(start_path):
                for f in filenames:
                    fp = os.path.join(dirpath, f)
                    if os.path.isfile(fp):
                        total_size += os.path.getsize(fp)
            return total_size

        file_size = get_directory_size(os.path.join(cur_path, item))

        item_path = os.path.join(cur_path, item)
        if os.path.isfile(item_path):
            file_size = os.path.getsize(item_path)

        for_print.append(
            f"- {item} file_size={file_size} bytes, is_dir={os.path.isdir(item_path)}"
        )
    return "\n".join(for_print)


# SCHEMA AND TOOL DECLARATION
schema_get_files_info = types.FunctionDeclaration(
    name="get_files_info",
    description="Lists files in the specified directory along with their sizes, constrained to the working directory.",
    parameters=types.Schema(
        type=types.Type.OBJECT,
        properties={
            "directory": types.Schema(
                type=types.Type.STRING,
                description="The directory to list files from, relative to the working directory. If not provided, lists files in the working directory itself.",
            ),
        },
    ),
)

get_file_info_tool = types.Tool(
    function_declarations=[
        schema_get_files_info,
    ]
)
