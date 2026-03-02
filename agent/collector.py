import subprocess

class LogCollector:
    def gather_logs(self, failed_cmd_result: dict, project_path: str) -> str:
        logs = f"--- Command Stderr ---\n{failed_cmd_result.get('stderr', '')}\n"
        
        # Grab actual pod statuses
        pod_status = subprocess.run(
            "kubectl get pods", 
            shell=True, capture_output=True, text=True
        )
        logs += f"\n--- Pod Status ---\n{pod_status.stdout}"
        
        # Grab recent K8s events
        k8s_logs = subprocess.run(
            "kubectl get events --sort-by='.metadata.creationTimestamp' | tail -n 15",
            shell=True, capture_output=True, text=True
        )
        logs += f"\n--- Kubernetes Events ---\n{k8s_logs.stdout}"
        
        return logs