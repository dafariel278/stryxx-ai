import datetime
import time

class ExecutorAgent:
    def execute(self, plan):
        print("⚙ Executor running task...")
        time.sleep(1)

        if plan["type"] == "report":
            content = f"""
STRYX INTELLIGENCE REPORT
Generated: {datetime.datetime.now()}

Topic: {plan['topic']}

This is an automatically generated report.
"""
            with open("report.txt", "w") as f:
                f.write(content)

            return "Report generated → report.txt"

        elif plan["type"] == "summary":
            words = plan["content"].split()
            short = " ".join(words[:15])
            return f"Summary: {short}..."

        else:
            return "Task executed successfully."