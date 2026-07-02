import subprocess
import os

class Validator:
    def __init__(self):
        pass

    def check_syntax_with_feedback(self, file_path):
        """Verifies if the Python file has any syntax errors, returning feedback if compile fails."""
        try:
            subprocess.run(["python", "-m", "py_compile", file_path], capture_output=True, text=True, check=True)
            return True, None
        except subprocess.CalledProcessError as e:
            return False, e.stderr
        except FileNotFoundError:
            return False, "Python executable not found in path."
        except Exception as e:
            return False, str(e)