from Utilities.file_utilities import uniquify_file_path

if __name__ == "__main__":

    script = "Pygame"
    name = f"{input('Filename: ')}.py"

    if not name[:-3]:
        name = "new_script.py"

    name = uniquify_file_path(name)

    with open(name, "w") as f, open(f"Scripts/{script}.py", "r") as g:
        f.write(g.read())
