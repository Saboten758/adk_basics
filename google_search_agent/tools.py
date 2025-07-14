# tools.py
import os
import base64
from pathlib import Path
import requests
from typing import Optional, List, Dict
import wikipedia
import arxiv
from duckduckgo_search import DDGS
from google.adk.tools import FunctionTool

# File System Functions
def list_files(path: str = ".") -> dict:
    """List all files in the specified directory path.
    
    Args:
        path: The directory path to list files from (default: current directory)
        
    Returns:
        A dictionary with status and list of files or error message
    """
    try:
        files = [str(p) for p in Path(path).iterdir() if p.is_file()]
        return {"status": "success", "files": files}
    except Exception as e:
        return {"status": "error", "error_message": str(e)}

def read_file(path: str) -> dict:
    """Read content from a file.
    
    Args:
        path: The file path to read from
        
    Returns:
        A dictionary with status and file content or error message
    """
    try:
        with open(path, 'r', encoding='utf-8') as f:
            content = f.read()
        return {"status": "success", "content": content}
    except Exception as e:
        return {"status": "error", "error_message": str(e)}

def write_file(path: str, content: str) -> dict:
    """Write content to a file.
    
    Args:
        path: The file path to write to
        content: The content to write to the file
        
    Returns:
        A dictionary with status and success message or error message
    """
    try:
        with open(path, 'w', encoding='utf-8') as f:
            f.write(content)
        return {"status": "success", "message": f"File {path} written successfully"}
    except Exception as e:
        return {"status": "error", "error_message": str(e)}

# Web Search Function
def web_search(query: str) -> dict:
    """Search the web using DuckDuckGo for the given query.
    
    Args:
        query: The search query string
        
    Returns:
        A dictionary with status and search results or error message
    """
    try:
        results = []
        with DDGS() as ddgs:
            for r in ddgs.text(query, max_results=5):
                results.append(r)
        return {"status": "success", "results": results}
    except Exception as e:
        return {"status": "error", "error_message": str(e)}

# Weather Function
def get_weather(location: str) -> dict:
    """Get current weather information for a given location.
    
    Args:
        location: The location to get weather for (city name)
        
    Returns:
        A dictionary with status and weather information or error message
    """
    try:
        API_KEY = os.getenv("OPENWEATHER_API_KEY")
        if not API_KEY:
            return {"status": "error", "error_message": "OPENWEATHER_API_KEY environment variable not set"}
        
        URL = f"http://api.openweathermap.org/data/2.5/weather?q={location}&appid={API_KEY}&units=metric"
        response = requests.get(URL)
        data = response.json()
        
        if data.get("cod") != 200:
            return {"status": "error", "error_message": data.get("message", "Unknown error")}
        
        return {
            "status": "success",
            "location": data["name"],
            "temperature": data["main"]["temp"],
            "feels_like": data["main"]["feels_like"],
            "humidity": data["main"]["humidity"],
            "wind_speed": data["wind"]["speed"],
            "description": data["weather"][0]["description"]
        }
    except Exception as e:
        return {"status": "error", "error_message": str(e)}

# Wikipedia Function
def search_wikipedia(query: str) -> dict:
    """Search and retrieve summaries from Wikipedia.
    
    Args:
        query: The search query for Wikipedia
        
    Returns:
        A dictionary with status and Wikipedia summary or error message
    """
    try:
        summary = wikipedia.summary(query, sentences=5)
        return {"status": "success", "summary": summary}
    except wikipedia.exceptions.DisambiguationError as e:
        return {"status": "disambiguation", "options": e.options}
    except Exception as e:
        return {"status": "error", "error_message": str(e)}

# ArXiv Function
def search_arxiv(query: str) -> dict:
    """Search academic papers on arXiv.
    
    Args:
        query: The search query for arXiv papers
        
    Returns:
        A dictionary with status and list of papers or error message
    """
    try:
        client = arxiv.Client()
        search = arxiv.Search(
            query=query,
            max_results=5,
            sort_by=arxiv.SortCriterion.Relevance
        )
        results = list(client.results(search))
        
        papers = []
        for paper in results:
            papers.append({
                "title": paper.title,
                "authors": [a.name for a in paper.authors],
                "summary": paper.summary,
                "url": paper.pdf_url
            })
        
        return {"status": "success", "papers": papers}
    except Exception as e:
        return {"status": "error", "error_message": str(e)}

# Create FunctionTool instances
filesystem_tool = FunctionTool(func=list_files)
file_read_tool = FunctionTool(func=read_file)
file_write_tool = FunctionTool(func=write_file)
websearch_tool = FunctionTool(func=web_search)
weather_tool = FunctionTool(func=get_weather)
wikipedia_tool = FunctionTool(func=search_wikipedia)
arxiv_tool = FunctionTool(func=search_arxiv)