from pathlib import Path
from documentpy import document_file

dir_path = Path(__file__).parent

# creates a documented version of ./code_npm.py
document_file(dir_path / "code_npm.py", model_name="gpt-4o-mini")