import os


def uniquify_file_path(file_path: str) -> str:
    if os.path.exists(file_path):
        name, ext = file_path.rsplit('.', 1)
        i = 0
        while os.path.exists(f"{name}.{ext}"):
            name = name.rsplit('(', 1)[0] + f"({i})"
            i += 1
        return f"{name}.{ext}"
    return file_path
