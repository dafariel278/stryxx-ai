class MemoryAgent:
    def __init__(self):
        self.history = []

    def store(self, task):
        self.history.append(task)

    def recall(self):
        return self.history