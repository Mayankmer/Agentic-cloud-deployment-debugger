class ReportGenerator:
    def __init__(self):
        self.history = []

    def log_attempt(self, attempt: int, status: str, error: str = "None"):
        self.history.append(f"Attempt {attempt}: {status} | Error: {error}")

    def generate_markdown(self):
        with open("deployment_report.md", "w") as f:
            f.write("# Deployment Execution Report\n\n")
            for entry in self.history:
                f.write(f"- {entry}\n")
        print("📄 Report saved to deployment_report.md")