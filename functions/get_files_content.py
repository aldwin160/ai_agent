import os
from google.genai import types


def get_file_content(working_directory, file_path):

    # SET ABS PATHS
    cur_path = os.path.join(working_directory, file_path)
    abs_working_dir = os.path.abspath(working_directory)
    abs_cur_path = os.path.abspath(cur_path)

    # VALIDATIONS
    if os.path.commonpath([abs_working_dir, abs_cur_path]) != abs_working_dir:
        return f'Error: Cannot read "{file_path}" as it is outside the permitted working directory'
    if not os.path.isfile(cur_path):
        return f'Error: File not found or is not a regular file: "{file_path}"'

    # READ FILE CONTENT
    with open(cur_path, "r") as f:
        content = f.read()

    if len(content) > 10000:
        return (
            content[:10000] + f'[...File "{file_path}" truncated at 10000 characters]'
        )

    return content


# SCHEMA AND TOOL DECLARATION
schema_get_file_content = types.FunctionDeclaration(
    name="get_file_content",
    description="Reads the content of a specified file, constrained to the working directory.",
    parameters=types.Schema(
        type=types.Type.OBJECT,
        properties={
            "file_path": types.Schema(
                type=types.Type.STRING,
                description="The path of the file to read, relative to the working directory.",
            ),
        },
    ),
)


get_file_content_tool = types.Tool(
    function_declarations=[schema_get_file_content],
)
