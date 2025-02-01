from typing import Dict, Any
from datetime import datetime, timedelta

class DateTimeTool:
    name = "datetime"
    description = "Perform date calculations relative to today"

    def run(self, query: str) -> Dict[str, Any]:
        """
        Performs date calculations and returns the result
        """
        try:
            today = datetime.now()
            
            if query == "today":
                target_date = today
            elif query.startswith("days_ago:"):
                days = int(query.split(":")[1])
                target_date = today - timedelta(days=days)
            elif query.startswith("days_ahead:"):
                days = int(query.split(":")[1])
                target_date = today + timedelta(days=days)
            else:
                return {
                    "success": False,
                    "result": "Error: Invalid query format"
                }
            
            # Format the result with both date and day of week
            formatted_date = target_date.strftime("%Y-%m-%d")
            day_of_week = target_date.strftime("%A")
            result = f"{formatted_date} ({day_of_week})"
                
            return {
                "success": True,
                "result": result
            }
            
        except Exception as e:
            return {
                "success": False,
                "result": f"Error: {str(e)}"
            } 