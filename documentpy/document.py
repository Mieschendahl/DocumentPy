import sys
from pathlib import Path
from typing import Optional, TextIO
from promptgpt import Prompter, prebuilt, GPT
from documentpy.utils import add_suffix_to_path
from documentpy.comparator import is_equivalent

IF = lambda x, y: y if x else ""

def document_code(code: str, docstrings: bool = True, types: bool = True, comments: bool = False, model_name: str = "gpt-4o-mini", log_file: Optional[TextIO] = sys.stdout, allow_injections: bool = False) -> str:
    """Documents the provided Python code by modifying it according to specified options.

    Args:
        code: The Python code to be documented.
        docstrings: A flag indicating whether to add Google style docstrings.
        types: A flag indicating whether to add type annotations.
        comments: A flag indicating whether to add comments.
        model_name: The name of the model to be used for documentation.
        log_file: The file to log the output.
        allow_injections: A flag indicating whether to allow code injections.

    Returns:
        The modified Python code.
    """

    model = GPT()\
        .set_cache(f"__promptgpt__/{model_name}")\
        .configure(model=model_name, temperature=0)
    
    prompter = Prompter(
            model=model,
            log_file=log_file,
            allow_injections=allow_injections
        )
    
    response = prompter\
        .add_message("You are an expert Python programmer", role="developer")\
        .add_message(
            f"I have some Python code that I want you to modify. Modify the code as follows:"
            + IF(
                docstrings,
                f"\nAdd a google style docstrings to functions, methods, and classes that explain what they do."
                f"\nDo not include type annotations in the docstrings, and fix any missing information such as functionality, parameters, or return value."
            )
            + IF(
                types,
                f"\nAdd type annotations whenever type checking would require them."
            )
            + IF(
                comments,
                f"\nAdd comments that help programmers understand the code, but avoid comments that state the obvious."
            )
            + f"\nOnly answer with the modify code."
            f"\nOnly modify what I explicitly told you to modify and nothing else, not even typos or formatting."
            f"\n\nHere is the code:\n```python{code}\n```"
        )\
        .get_response()
    return prebuilt.clean_code(response)

def document_file(file_path: str | Path, docstrings: bool = True, types: bool = True, comments: bool = False, model_name: str = "gpt-4o-mini", log_file: Optional[TextIO] = sys.stdout, allow_injections: bool = False) -> None:
    """Documents a single Python file by modifying its content according to specified options.
    The documented file will be saved with the suffix ".safe." or ".unsafe." depending on whether the LLM
    potentially did breaking changes or not.

    Args:
        file_path: The path to the Python file to be documented.
        docstrings: A flag indicating whether to add Google style docstrings.
        types: A flag indicating whether to add type annotations.
        comments: A flag indicating whether to add comments.
        model_name: The name of the model to be used for documentation.
        log_file: The file to log the output.
        allow_injections: A flag indicating whether to allow code injections.
    """
    path = Path(file_path)
    code = path.read_text()
    modified_code = document_code(code, docstrings, types, comments, model_name, log_file, allow_injections)
    if is_equivalent(code, modified_code):
        _path = add_suffix_to_path(path, "safe")
    else:
        _path = add_suffix_to_path(path, "unsafe")
    _path.write_text(modified_code)

def document_files(obj_path: str | Path, recursive: bool = True, docstrings: bool = True, types: bool = True, comments: bool = False, model_name: str = "gpt-4o-mini", log_file: Optional[TextIO] = sys.stdout, allow_injections: bool = False) -> None:
    """Documents all Python files in a directory, optionally recursively.

    Args:
        obj_path: The path to the directory or file to be documented.
        recursive: A flag indicating whether to document files in subdirectories.
        docstrings: A flag indicating whether to add Google style docstrings.
        types: A flag indicating whether to add type annotations.
        comments: A flag indicating whether to add comments.
        model_name: The name of the model to be used for documentation.
        log_file: The file to log the output.
        allow_injections: A flag indicating whether to allow code injections.
    """
    path = Path(obj_path)
    if path.is_dir():
        for p in path.iterdir():
            if p.is_dir() and recursive:
                document_files(str(p), recursive, docstrings, types, comments, model_name, log_file, allow_injections)
            elif p.is_file():
                document_file(str(p), docstrings, types, comments, model_name, log_file, allow_injections)
    elif path.is_file():
        document_file(str(path), docstrings, types, comments)