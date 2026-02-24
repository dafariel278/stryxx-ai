import time

class PlannerAgent:
    def plan(self, task):
        print("🧠 Planner analyzing task...")
        time.sleep(1)

        if "report" in task.lower():
            return {
                "type": "report",
                "topic": task.replace("report ", "")
            }
        elif "summary" in task.lower():
            return {
                "type": "summary",
                "content": task.replace("summary ", "")
            }
        else:
            return {
                "type": "general",
                "content": task
            }