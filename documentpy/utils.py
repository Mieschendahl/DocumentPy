from pathlib import Path

def add_suffix_to_path(path: Path, suffix: str) -> Path:
    """
    Adds a suffix before the file extension of a Path object.

    Example:
        Path("folder/file.py") + suffix "x" -> Path("folder/file.x.py")
    """
    stem = path.stem
    suffixes = ''.join(path.suffixes)
    new_name = f"{stem}.{suffix}{suffixes}"
    return path.with_name(new_name)