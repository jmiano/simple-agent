from typing import Dict, Any
import wikipedia

class WikipediaTool:
    name = "wikipedia"
    description = "Search Wikipedia articles and read their content"

    def run(self, query: str) -> Dict[str, Any]:
        """
        Search Wikipedia or get article content based on the query type.
        Query format:
        - "search:term" to search for articles
        - "read:title" to get article content
        """
        try:
            if query.startswith("search:"):
                search_term = query[7:].strip()  # Remove "search:" prefix
                results = wikipedia.search(search_term, results=5)
                if not results:
                    return {
                        "success": True,
                        "result": "No Wikipedia articles found."
                    }
                formatted_results = "\n".join([f"- {title}" for title in results])
                return {
                    "success": True,
                    "result": f"Found these articles:\n{formatted_results}"
                }
            
            elif query.startswith("read:"):
                article_title = query[5:].strip()  # Remove "read:" prefix
                try:
                    # Try to get the most relevant page
                    page = wikipedia.page(article_title, auto_suggest=True)
                    # Get a summary (first few paragraphs)
                    summary = wikipedia.summary(article_title, sentences=5)
                    return {
                        "success": True,
                        "result": f"Title: {page.title}\n\nSummary:\n{summary}\n\nFull URL: {page.url}"
                    }
                except wikipedia.DisambiguationError as e:
                    options = "\n".join([f"- {option}" for option in e.options[:5]])
                    return {
                        "success": False,
                        "result": f"This title is ambiguous. Did you mean:\n{options}"
                    }
                except wikipedia.PageError:
                    return {
                        "success": False,
                        "result": f"No Wikipedia article found with title: {article_title}"
                    }
            else:
                return {
                    "success": False,
                    "result": "Error: Query must start with 'search:' or 'read:'"
                }
                
        except Exception as e:
            return {
                "success": False,
                "result": f"Error: {str(e)}"
            } 