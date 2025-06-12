import sys
import argparse
from documentpy import document_file

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Runs DocumentPy on a given file.", add_help=False)
    parser.add_argument(
        "file_path",
        help="the file to document"
    )
    parser.add_argument(
        "--help",
        action="help",
        help="show this help message"
    )
    parser.add_argument(
        "--silent",
        action="store_true",
        help="deactives printing"
    )
    parser.add_argument(
        "--interactive",
        action="store_true",
        help="allows user injections"
    )
    parser.add_argument(
        "--no-docstrings",
        action="store_false",
        help="avoid adding docstring documentation"
    )
    parser.add_argument(
        "--no-types",
        action="store_false",
        help="avoid adding annotations documentation"
    )
    parser.add_argument(
        "--comments",
        action="store_true",
        help="adds comments documentation"
    )
    parser.add_argument(
        "--model_name",
        default="gpt-4o-mini",
        help="sets the openai model"
    )
    args = parser.parse_args()
    document_file(args.file_path, args.no_docstrings, args.no_types, args.comments, args.model_name, None if args.silent else sys.stdout, args.interactive)