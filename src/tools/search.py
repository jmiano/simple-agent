from typing import Dict, Any
from serpapi import GoogleSearch
import os

class GoogleSearchTool:
    name = "google_search"
    description = "Search the internet for information"

    def __init__(self):
        self.api_key = os.getenv("SERPAPI_API_KEY")
        if not self.api_key:
            raise ValueError("SERPAPI_API_KEY environment variable is not set")

    def run(self, query: str) -> Dict[str, Any]:
        """
        Performs a Google search and returns the results
        """
        try:
            search = GoogleSearch({
                "q": query,
                "api_key": self.api_key,
                "num": 3  # Limit to top 3 results
            })
            results = search.get_dict()
            
            if "error" in results:
                return {
                    "success": False,
                    "result": f"Error: {results['error']}"
                }

            # Extract and format organic results
            organic_results = results.get("organic_results", [])
            if not organic_results:
                return {
                    "success": True,
                    "result": "No results found."
                }

            # Format results as a clean string
            formatted_results = []
            for result in organic_results:
                title = result.get("title", "")
                snippet = result.get("snippet", "")
                formatted_results.append(f"{title}\n{snippet}")

            return {
                "success": True,
                "result": "\n\n".join(formatted_results)
            }

        except Exception as e:
            return {
                "success": False,
                "result": f"Error performing search: {str(e)}"
            } 