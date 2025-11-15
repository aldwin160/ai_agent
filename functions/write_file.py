import os
from google.genai import types


def write_file(working_directory, file_path, content):
    cur_path = os.path.join(working_directory, file_path)
    abs_working_dir = os.path.abspath(working_directory)
    abs_cur_path = os.path.abspath(cur_path)

    # VALIDATIONS
    if os.path.commonpath([abs_working_dir, abs_cur_path]) != abs_working_dir:
        return f'Error: Cannot write to "{file_path}" as it is outside the permitted working directory'

    if not os.path.exists(abs_cur_path):
        os.makedirs(os.path.dirname(abs_cur_path), exist_ok=True)
    with open(abs_cur_path, "w") as f:
        f.write(content)
        return (
            f'Successfully wrote to "{file_path}" ({len(content)} characters written)'
        )


# SCHEMA AND TOOL DECLARATION
schema_write_file = types.FunctionDeclaration(
    name="write_file",
    description="Writes or overwrites a file with the specified content, constrained to the working directory.",
    parameters=types.Schema(
        type=types.Type.OBJECT,
        properties={
            "file_path": types.Schema(
                type=types.Type.STRING,
                description="The path of the file to write to, relative to the working directory.",
            ),
            "content": types.Schema(
                type=types.Type.STRING,
                description="The content to write into the file.",
            ),
        },
    ),
)
