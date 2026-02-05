import requests
import os
from .base import register_tool

@register_tool("github_search")
class GitHubTool:
    """Searches GitHub repositories for a query."""
    def execute(self, query):
        token = os.getenv("GITHUB_TOKEN")
        headers = {"Authorization": f"token {token}", "Accept": "application/vnd.github.v3+json"}
        url = f"https://api.github.com/search/repositories?q={query}&sort=stars&order=desc&per_page=3"
        
        try:
            response = requests.get(url, headers=headers)
            response.raise_for_status()
            data = response.json()
            return [
                {
                    "name": item["full_name"],
                    "stars": item["stargazers_count"],
                    "url": item["html_url"],
                    "description": item["description"]
                }
                for item in data.get("items", [])
            ]
        except Exception as e:
            return f"Error searching GitHub: {str(e)}"