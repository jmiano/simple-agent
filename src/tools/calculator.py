from typing import Dict, Any
import math

class CalculatorTool:
    name = "calculator"
    description = "Useful for performing mathematical calculations"

    def run(self, expression: str) -> Dict[str, Any]:
        """
        Evaluates a mathematical expression and returns the result
        """
        try:
            # Create a safe dictionary of allowed functions
            safe_dict = {
                'math': math,
                'abs': abs,
                'round': round,
                'pow': pow
            }
            
            # Evaluate the expression in a safe context
            result = eval(expression, {"__builtins__": {}}, safe_dict)
            return {
                "success": True,
                "result": str(result)  # Convert to string to ensure JSON serialization
            }
        except Exception as e:
            return {
                "success": False,
                "result": f"Error: {str(e)}"
            } 