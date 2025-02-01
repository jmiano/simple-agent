from typing import List, Dict, Any
import openai
import json
from tools import CalculatorTool, GoogleSearchTool, DateTimeTool, WikipediaTool

class Agent:
    def __init__(self, openai_api_key: str):
        # Set up OpenAI client
        self.client = openai.OpenAI(api_key=openai_api_key)
        
        # Initialize tools
        self.tools = {
            "calculator": CalculatorTool(),
            "google_search": GoogleSearchTool(),
            "datetime": DateTimeTool(),
            "wikipedia": WikipediaTool()
        }
        
        # Define tools for OpenAI
        self.available_tools = [
            {
                "type": "function",
                "function": {
                    "name": "calculator",
                    "description": "Perform mathematical calculations with support for basic operations and math functions",
                    "parameters": {
                        "type": "object",
                        "properties": {
                            "expression": {
                                "type": "string",
                                "description": "The mathematical expression to evaluate (e.g., '2 + 2', 'math.sqrt(16)')"
                            }
                        },
                        "required": ["expression"],
                        "additionalProperties": False
                    },
                    "strict": True
                }
            },
            {
                "type": "function",
                "function": {
                    "name": "google_search",
                    "description": "Search the internet for current information",
                    "parameters": {
                        "type": "object",
                        "properties": {
                            "query": {
                                "type": "string",
                                "description": "The search query to find information"
                            }
                        },
                        "required": ["query"],
                        "additionalProperties": False
                    },
                    "strict": True
                }
            },
            {
                "type": "function",
                "function": {
                    "name": "datetime",
                    "description": "Get dates relative to today, including the day of the week",
                    "parameters": {
                        "type": "object",
                        "properties": {
                            "operation": {
                                "type": "string",
                                "enum": ["today", "days_ago", "days_ahead"],
                                "description": "The type of date calculation to perform"
                            },
                            "days": {
                                "type": "integer",
                                "description": "Number of days for ago/ahead operations. Required when operation is 'days_ago' or 'days_ahead'."
                            }
                        },
                        "required": ["operation", "days"],
                        "additionalProperties": False
                    },
                    "strict": True
                }
            },
            {
                "type": "function",
                "function": {
                    "name": "wikipedia",
                    "description": "Search Wikipedia articles and read their content",
                    "parameters": {
                        "type": "object",
                        "properties": {
                            "action": {
                                "type": "string",
                                "enum": ["search", "read"],
                                "description": "Whether to search for articles or read a specific article"
                            },
                            "query": {
                                "type": "string",
                                "description": "The search term or article title"
                            }
                        },
                        "required": ["action", "query"],
                        "additionalProperties": False
                    },
                    "strict": True
                }
            }
        ]
        
        # Create the system prompt
        self.system_prompt = """You are a helpful AI assistant that can use tools to answer questions.
Your task is to help users by using the available tools appropriately.
For date-related queries, always use the datetime tool to get accurate results.
For the datetime tool:
- Use operation="today" with days=0 to get today's date
- Use operation="days_ago" with the number of days to get a past date
- Use operation="days_ahead" with the number of days to get a future date
For Wikipedia queries:
- Use action="search" to find relevant articles
- Use action="read" to get the content of a specific article
Always show your reasoning and use tools to verify facts rather than making assumptions."""

        # Add planning prompt
        self.planning_prompt = """You are a planning assistant. Your task is to create a step-by-step plan to answer the user's question.
Available tools:
1. calculator: For mathematical calculations
2. google_search: For searching the internet for current information
3. datetime: For date calculations (today, days_ago, days_ahead)
4. wikipedia: For searching and reading Wikipedia articles
   - Use action="search" to find relevant articles
   - Use action="read" to get article content and summary

Create a plan that breaks down the task into steps. Each step should specify:
1. Which tool to use
2. What input to provide to the tool
3. How to use the result

For Wikipedia queries, it's often good to:
1. First search for relevant articles
2. Then read the most relevant article
3. Use google_search if additional current information is needed

Respond in this format:
PLAN:
1. [First step with tool and purpose]
2. [Second step with tool and purpose]
...
REASONING: [Why this plan will answer the question]"""

    def _execute_tool(self, tool_name: str, tool_args: Dict[str, Any]) -> Dict[str, Any]:
        """Execute a tool with the given arguments"""
        if tool_name not in self.tools:
            return {
                "success": False,
                "result": f"Error: Tool '{tool_name}' not found"
            }
        
        # Convert the arguments to the format expected by each tool
        if tool_name == "datetime":
            operation = tool_args["operation"]
            days = tool_args["days"]  # Now required
            if operation == "today":
                query = "today"
            else:
                query = f"{operation}:{days}"
            return self.tools[tool_name].run(query)
        elif tool_name == "calculator":
            return self.tools[tool_name].run(tool_args["expression"])
        elif tool_name == "google_search":
            return self.tools[tool_name].run(tool_args["query"])
        elif tool_name == "wikipedia":
            action = tool_args["action"]
            query = tool_args["query"]
            formatted_query = f"{action}:{query}"
            return self.tools[tool_name].run(formatted_query)
        
        return {
            "success": False,
            "result": "Error: Invalid tool configuration"
        }

    def _create_plan(self, query: str) -> str:
        """Create a plan for solving the query"""
        try:
            response = self.client.chat.completions.create(
                model="gpt-4",
                messages=[
                    {"role": "system", "content": self.planning_prompt},
                    {"role": "user", "content": f"Create a plan to answer: {query}"}
                ],
                temperature=0
            )
            return response.choices[0].message.content
        except Exception as e:
            return f"Error creating plan: {str(e)}"

    def run(self, query: str) -> str:
        """
        Run the agent with a query and return the response
        """
        try:
            # First, create a plan
            plan = self._create_plan(query)
            steps = [f"🤔 **Question:** {query}\n\n📋 **Planning Phase:**\n{plan}"]
            
            messages = [
                {"role": "system", "content": self.system_prompt},
                {"role": "user", "content": f"Execute this plan to answer the question: {query}\n\nPlan:\n{plan}"}
            ]
            
            while True:
                # Get the next action from the model
                response = self.client.chat.completions.create(
                    model="gpt-4o",
                    messages=messages,
                    tools=self.available_tools,
                    tool_choice="auto",
                    temperature=0
                )
                
                message = response.choices[0].message
                
                # If no tool calls, we're done
                if not message.tool_calls:
                    if message.content:
                        steps.append("---")
                        steps.append(f"✨ **Final Answer:** {message.content}")
                    return "\n\n".join(steps)
                
                # Process each tool call
                for tool_call in message.tool_calls:
                    # Extract tool call details
                    function_name = tool_call.function.name
                    try:
                        function_args = json.loads(tool_call.function.arguments)
                    except Exception as e:
                        steps.append(f"Error parsing tool arguments: {str(e)}")
                        continue
                    
                    # Add the tool call to steps
                    steps.append("---")
                    steps.append(f"💭 **Executing Plan Step:** {message.content if message.content else 'Using tool to find information'}")
                    steps.append(f"🔧 **Tool:** {function_name}")
                    steps.append(f"📥 **Input:** {json.dumps(function_args, indent=2)}")
                    
                    # Execute the tool
                    result = self._execute_tool(function_name, function_args)
                    steps.append(f"📝 **Result:** {result['result']}")
                    
                    # Add the interaction to messages
                    messages.append({
                        "role": "assistant",
                        "content": message.content,
                        "tool_calls": [tool_call]
                    })
                    messages.append({
                        "role": "tool",
                        "tool_call_id": tool_call.id,
                        "content": str(result["result"])
                    })
                
        except Exception as e:
            return f"Error: {str(e)}" 