# DocumentPy

*DocumentPy* is a Python library for documenting Python code.

```python
from documentpy import document_file

# creates a documented version of ./examples/code_npm.py
document_file("examples/code_npm.py", model_name="gpt-4o-mini")
```

*DocumentPy* builds up on the LLM prompting library [*PromptGPT*](https://github.com/Mieschendahl/PromptGPT).

## Setup

1. Install *DocumentPy*.

    ```bash
    pip install --upgrade git+https://github.com/Mieschendahl/DocumentPy.git
    ```

2. Set your [OpenAI API Key](https://platform.openai.com/api-keys).

    ```bash
    export OPENAI_API_KEY=<your_api_key>
    ```

- *DocumentPy* can also be run as a script.

    ```bash
    python3 -m documentpy --help
    ```

The `examples` directory contains some examples.