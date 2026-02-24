from core.planner import PlannerAgent
from core.executor import ExecutorAgent
from core.memory import MemoryAgent

class StryxCore:
    def __init__(self):
        print("STRYX Multi-Agent System Initialized")
        self.planner = PlannerAgent()
        self.executor = ExecutorAgent()
        self.memory = MemoryAgent()   

    def process(self, task):
        self.memory.store(task)       

        plan = self.planner.plan(task)
        result = self.executor.execute(plan)

        return result