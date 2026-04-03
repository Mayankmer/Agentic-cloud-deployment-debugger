import os
import shutil

class PatchApplier:
    def apply(self, patch: dict, project_path: str) -> bool:
        """Applies a search-and-replace fix safely."""
        if not patch:
            return False
            
        filepath = os.path.join(project_path, patch["file"])
        if not os.path.exists(filepath):
            return False

        # 1. Backup the file
        shutil.copy(filepath, f"{filepath}.bak")
        print(f" Backed up {filepath}")

        # 2. Apply fix
        with open(filepath, 'r') as file:
            content = file.read()
        
        content = content.replace(patch["search"], patch["replace"])

        with open(filepath, 'w') as file:
            file.write(content)
            
        print(f" Patched {filepath}")
        return True