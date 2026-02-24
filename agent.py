import datetime

class StryxAgent:
    def __init__(self):
        self.memory = []
        print("\n🦉 STRYX Core Initialized")
        print("Autonomous Intelligence Ready.\n")

    def log(self, message):
        with open("stryx_log.txt", "a") as f:
            f.write(f"{datetime.datetime.now()} - {message}\n")

    def generate_report(self, topic):
        content = f"""
STRYX INTELLIGENCE REPORT
Generated: {datetime.datetime.now()}

Topic: {topic}

Summary:
Artificial Intelligence continues to evolve rapidly,
with strong growth in automation and autonomous systems.

End of Report.
"""
        with open("report.txt", "w") as f:
            f.write(content)

        return "Report generated successfully → report.txt"

    def summarize(self, text):
        words = text.split()
        short = " ".join(words[:15])
        return f"Summary: {short}..."

    def think(self, task):
        task_lower = task.lower()
        self.memory.append(task)
        self.log(f"User: {task}")

        if task_lower == "memory":
            return f"Memory: {self.memory}"

        elif task_lower.startswith("report "):
            topic = task.replace("report ", "")
            return self.generate_report(topic)

        elif task_lower.startswith("summary "):
            text = task.replace("summary ", "")
            return self.summarize(text)

        elif "trend" in task_lower:
            return "AI trends show rapid growth in automation and autonomous agents."

        elif "hello" in task_lower:
            return "Hello. STRYX fully operational."

        elif task_lower == "help":
            return "Commands: hello, trend, memory, report topic, summary text, help, exit"

        else:
            return "Task processed successfully."