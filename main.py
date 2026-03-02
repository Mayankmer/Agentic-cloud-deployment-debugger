import os
from agent.orchestrator import Orchestrator

if __name__ == "__main__":
    # Ensure you are passing the correct path to your testing folder
    target_project = "./test_project"
    
    # Create test directory if it doesn't exist to prevent crash
    os.makedirs(target_project, exist_ok=True)
    
    bot = Orchestrator()
    bot.run(target_project)