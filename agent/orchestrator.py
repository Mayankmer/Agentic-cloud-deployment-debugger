import time

from .executor import DeploymentExecutor
from .validator import Validator
from .collector import LogCollector
from .classifier import ErrorClassifier
from .fixer import FixGenerator
from .patcher import PatchApplier
from .reporter import ReportGenerator

class Orchestrator:
    def __init__(self):
        self.executor = DeploymentExecutor()
        self.validator = Validator()
        self.collector = LogCollector()
        self.classifier = ErrorClassifier()
        self.fixer = FixGenerator()
        self.patcher = PatchApplier()
        self.reporter = ReportGenerator()

    def run(self, project_path: str, max_retries: int = 3):
        print(f"🚀 Starting autonomous deployment for {project_path}")
        
        for attempt in range(1, max_retries + 1):
            print(f"\n--- Attempt {attempt} ---")
            
            # 1. Deploy
            exec_result = self.executor.deploy(project_path)
            
            # 2. Validate
            if exec_result["success"] and self.validator.check_health(project_path):
                print("✅ Deployment Successful!")
                self.reporter.log_attempt(attempt, "Success")
                break
                
            # 3. Handle Failure
            print("❌ Deployment Failed. Debugging...")
            logs = self.collector.gather_logs(exec_result, project_path)

            print(f"\n--- DEBUG LOGS ---\n{logs}\n------------------\n")
            error_type = self.classifier.classify(logs)
            self.reporter.log_attempt(attempt, "Failed", error_type)
            
            # 4. Fix and Patch (Assuming deployment.yaml is the target for this example)
            patch = self.fixer.generate_fix(error_type, logs, "deployment.yaml")
            success = self.patcher.apply(patch, project_path)
            
            if not success:
                print("🛑 Could not generate or apply fix. Aborting.")
                break
                
            # --- NEW CLEANUP STEP ---
            print("🧹 Cleaning up old broken resources before next attempt...")
            self.executor.run_command("kubectl delete -f .", cwd=project_path)
            # Give Kubernetes a few seconds to terminate the old pods
            time.sleep(5)
                
        self.reporter.generate_markdown()