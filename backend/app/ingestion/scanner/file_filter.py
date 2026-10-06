from pathlib import Path



EXCLUDED_EXTENSIONS={
    ".pyc",
    ".pyo",
    ".class",
    ".log"
}

EXCLUDED_DIRECTORIES = {
    "__pycache__",
    ".git",
    ".venv",
    "venv",
    "node_modules"
}

class FileFilter:

    def should_include(self,file_path:str):
        path=Path(file_path)

        if path.suffix.lower() in EXCLUDED_EXTENSIONS:
            return False

        for part in path.parts:
            if part in EXCLUDED_DIRECTORIES:
                return False

        return True


