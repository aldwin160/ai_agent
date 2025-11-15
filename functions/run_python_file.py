import os
import subprocess
import sys
from google.genai import types


def run_python_file(working_directory, file_path, args=[]):
    cur_path = os.path.join(working_directory, file_path)
    abs_working_dir = os.path.abspath(working_directory)
    abs_cur_path = os.path.abspath(cur_path)

    # VALIDATIONS
    if (
        os.path.commonpath([abs_working_dir, abs_cur_path])
        != abs_working_dir  # Prevent path traversal
    ):
        return f'Error: Cannot execute "{file_path}" as it is outside the permitted working directory'

    if not os.path.exists(abs_cur_path):
        return f'Error: File "{file_path}" not found.'

    if not abs_cur_path.endswith(".py"):
        return f'Error: "{file_path}" is not a Python file.'

    # RUN THE PYTHON FILE
    try:
        result = subprocess.run(
            [sys.executable, abs_cur_path] + args,
            stdout=subprocess.PIPE,
            stderr=subprocess.STDOUT,
            text=True,
            check=False,
            timeout=30,
        )

        output = []

        if result.stdout:
            output.append(f"STDOUT: \n{result.stdout}")
        if result.returncode != 0:
            output.append(f"Process exited with code {result.returncode}")
        if not output:
            return "No output produced."
        return "\n".join(output)
    except subprocess.TimeoutExpired as e:
        return "Error: Process timed out after 30 seconds"
    except Exception as e:
        return f"Error executing Python file: {e}"


# SCHEMA AND TOOL DECLARATION
schema_run_python_file = types.FunctionDeclaration(
    name="run_python_file",
    description="Executes a Python file with optional arguments, constrained to the working directory.",
    parameters=types.Schema(
        type=types.Type.OBJECT,
        properties={
            "file_path": types.Schema(
                type=types.Type.STRING,
                description="The path of the Python file to execute, relative to the working directory.",
            ),
            "args": types.Schema(
                type=types.Type.ARRAY,
                items=types.Schema(
                    type=types.Type.STRING,
                ),
                description="A list of arguments to pass to the Python file during execution.",
            ),
        },
    ),
)
