from flask import Flask, render_template, request, send_file
import os

app = Flask(__name__)

# ========================
# STRYX CORE SYSTEM
# ========================

class StryxCore:
    def __init__(self):
        self.memory_log = []

    def execute(self, task):
        if not task:
            return "No task provided."

        response = f"AI processed task: {task}"
        self.memory_log.append(task)
        return response

    def memory(self):
        return self.memory_log


system = StryxCore()

# ========================
# ROUTES
# ========================

@app.route("/", methods=["GET", "POST"])
def home():
    response = None

    if request.method == "POST":
        task = request.form.get("task")

        if task == "download":
            # Generate temporary report
            file_path = "/tmp/report.txt"
            with open(file_path, "w") as f:
                f.write("STRYX AI REPORT\n")
                f.write("=================\n\n")
                for item in system.memory():
                    f.write(f"- {item}\n")

            return send_file(file_path, as_attachment=True)

        response = system.execute(task)

    return render_template(
        "index.html",
        response=response,
        memory=system.memory()
    )

# IMPORTANT: DO NOT USE app.run() FOR VERCEL