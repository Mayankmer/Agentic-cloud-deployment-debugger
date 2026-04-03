import os
import json
from google import genai
from dotenv import load_dotenv

load_dotenv()

class FixGenerator:
    def __init__(self):
        api_key = os.getenv("GEMINI_API_KEY")
        if not api_key:
            raise ValueError("GEMINI_API_KEY not found in .env file.")
        
        # New client initialization
        self.client = genai.Client(api_key=api_key)

    def generate_fix(self, error_type: str, logs: str, target_file: str) -> dict:
        print(f"Asking Gemini to fix {error_type} in {target_file}...")
        
        try:
            with open(os.path.join(".", "test_project", target_file), 'r') as f:
                file_content = f.read()
        except FileNotFoundError:
            print(f"Could not find {target_file} to send to LLM.")
            return None

        prompt = f"""
        You are an autonomous Kubernetes debugging agent.
        A deployment failed.
        
        Error Category: {error_type}
        
        Logs:
        {logs}
        
        Current content of {target_file}:
        ```yaml
        {file_content}
        ```
        
        Identify the root cause of the failure from the logs. Provide a search-and-replace fix for the YAML file.
        Output ONLY a raw, valid JSON object. Do not include markdown formatting, code blocks (like ```json), or explanatory text.
        Use this exact schema:
        {{
            "file": "{target_file}",
            "search": "the exact string to remove",
            "replace": "the new string to insert"
        }}
        """
        
        try:
            # New generation syntax
            response = self.client.models.generate_content(
                model='gemini-2.5-flash',
                contents=prompt,
            )
            
            raw_text = response.text.strip()
            if raw_text.startswith("```json"):
                raw_text = raw_text[7:]
            if raw_text.startswith("```"):
                raw_text = raw_text[3:]
            if raw_text.endswith("```"):
                raw_text = raw_text[:-3]
                
            patch = json.loads(raw_text.strip())
            return patch
            
        except json.JSONDecodeError as e:
            print(f"Failed to parse LLM output as JSON: {e}")
            return None
        except Exception as e:
            print(f"API Error: {e}")
            return None