# # app.py

# from google.adk.agents import Agent
# from google.adk.tools import google_search
# from .sub_agents import filesystem_agent

# root_agent = Agent(
#     name="google_search_agent",
#     model="gemini-2.0-flash-exp",
#     description="Agent to answer questions using Google Search and browse files and directories",
#     instruction="Agent to answer questions using Google Search and browse files and directories",
#     tools=[google_search]
#     # sub_agents=[filesystem_agent],
# )



from google.adk.agents import Agent
from .tools import (
    filesystem_tool,
    file_read_tool,
    file_write_tool,
    websearch_tool,
    weather_tool,
    wikipedia_tool,
    arxiv_tool
)

root_agent = Agent(
    name="multi_tool_agent",
    model="gemini-2.0-flash-exp",
    description="Agent that uses multiple tools including web search, file system, weather, Wikipedia, and arXiv.",
    instruction="""
    You are an intelligent assistant capable of:
    - Searching the web using the web_search tool
    - Reading files using the read_file tool
    - Writing files using the write_file tool
    - Listing files in directories using the list_files tool
    - Checking the weather using the get_weather tool
    - Looking up Wikipedia summaries using the search_wikipedia tool
    - Finding academic papers on arXiv using the search_arxiv tool
    
    Use the appropriate tool based on the user's request. Always check the status field
    in the tool response to determine if the operation was successful.
    
    For file operations, handle errors gracefully and provide helpful feedback.
    For search operations, present results in a clear and organized manner.
    For weather queries, provide comprehensive weather information.
    """,
    tools=[
        websearch_tool,
        filesystem_tool,
        file_read_tool,
        file_write_tool,
        weather_tool,
        wikipedia_tool,
        arxiv_tool,
    ]
)