import subprocess
import time

class Validator:
    def check_health(self, project_path: str, max_wait: int = 45) -> bool:
        """Polls Kubernetes to see if pods reach Running or Error states."""
        print(f"🔍 Validating deployment health (waiting up to {max_wait}s)...")
        
        # Poll every 3 seconds
        for _ in range(max_wait // 3):
            time.sleep(3)
            
            # 1. Check for explicit error states
            error_check = subprocess.run(
                "kubectl get pods | grep -E 'CrashLoopBackOff|Error|ImagePullBackOff|ErrImagePull'", 
                shell=True, capture_output=True, text=True
            )
            if error_check.stdout.strip():
                print("⚠️ Detected pod error state.")
                return False
            
            # 2. Check if pods are still creating/pending
            pending_check = subprocess.run(
                "kubectl get pods | grep -E 'ContainerCreating|Pending'", 
                shell=True, capture_output=True, text=True
            )
            if pending_check.stdout.strip():
                continue # Still spinning up, keep waiting
                
            # 3. If no errors and nothing pending, check if running
            running_check = subprocess.run(
                "kubectl get pods | grep 'Running'", 
                shell=True, capture_output=True, text=True
            )
            if running_check.stdout.strip():
                return True # Success!
        
        print("⏳ Validation timed out. Assuming failure.")
        return False