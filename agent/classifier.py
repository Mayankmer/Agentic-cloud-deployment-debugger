class ErrorClassifier:
    def classify(self, logs: str) -> str:
        """Simple rule-based classification."""
        logs_lower = logs.lower()
        if "imagepullbackoff" in logs_lower or "errimagepull" in logs_lower:
            return "IMAGE_PULL_ERROR"
        elif "syntax" in logs_lower or "mapping values are not allowed" in logs_lower:
            return "YAML_SYNTAX_ERROR"
        elif "crashloopbackoff" in logs_lower:
            return "RUNTIME_CRASH"
        return "UNKNOWN_ERROR"