import subprocess

class DeploymentExecutor:
    def run_command(self, cmd: str, cwd: str = ".") -> dict:
        """Executes a shell command and returns the result."""
        print(f"⚙️ Executing: {cmd}")
        result = subprocess.run(
            cmd, shell=True, cwd=cwd, capture_output=True, text=True
        )
        return {
            "success": result.returncode == 0,
            "stdout": result.stdout,
            "stderr": result.stderr
        }

    def deploy(self, project_path: str) -> dict:
        # Example: Just applying K8s manifests for simplicity
        return self.run_command("kubectl apply -f .", cwd=project_path)