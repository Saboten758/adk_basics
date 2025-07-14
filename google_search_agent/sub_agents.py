# google_search_agent/sub_agents.py

import os
from google.adk.agents import LlmAgent
from google.adk.tools import FunctionTool

# Define the target folder path
TARGET_FOLDER_PATH = "/home/saboten/Games"

# Ensure the path exists
if not os.path.exists(TARGET_FOLDER_PATH):
    print(f"Creating target folder: {TARGET_FOLDER_PATH}")
    os.makedirs(TARGET_FOLDER_PATH, exist_ok=True)

def list_files(path: str) -> str:
    """
    List files and directories in the given path.
    If you pass an empty string, it will default to the configured TARGET_FOLDER_PATH.
    """
    # If no path provided, fall back to the TARGET_FOLDER_PATH
    if not path:
        path = TARGET_FOLDER_PATH

    try:
        if not os.path.exists(path):
            return f"Path {path} does not exist"
        
        items = os.listdir(path)
        if not items:
            return f"Directory {path} is empty"
        
        result = f"Contents of {path}:\n"
        for item in items:
            full_path = os.path.join(path, item)
            if os.path.isdir(full_path):
                result += f"📁 {item}/\n"
            else:
                result += f"📄 {item}\n"
        return result
    except Exception as e:
        return f"Error listing files: {str(e)}"

def read_file(filename: str) -> str:
    """
    Read the contents of a file in the TARGET_FOLDER_PATH.
    Pass just the filename (no folders). If you pass an empty string,
    it will return an error message.
    """
    if not filename:
        return "No filename provided."

    full_path = os.path.join(TARGET_FOLDER_PATH, filename)
    try:
        if not os.path.exists(full_path):
            return f"File {filename} does not exist"
        
        with open(full_path, 'r', encoding='utf-8') as f:
            content = f.read()
        return f"Contents of {filename}:\n{content}"
    except Exception as e:
        return f"Error reading file: {str(e)}"

# Create filesystem agent with simple tools
filesystem_agent = LlmAgent(
    model='gemini-2.0-flash-exp',  # or 'gemini-2.0-flash-live-001'
    name='filesystem_assistant_agent',
    instruction='Help the user manage their files. You can list files and read file contents.',
    tools=[
        FunctionTool(list_files),
        FunctionTool(read_file),
    ],
)
