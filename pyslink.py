"""Soft link a file/directory with python site-packages directory"""
import os
import ast
import subprocess
import sys
from distutils.sysconfig import get_python_lib

__version__ = "0.4.0"


def sh(command: str) -> str:
    return subprocess.Popen(
        command,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        shell=True,
        universal_newlines=True,
    ).communicate()[0]


def get_path_info(path: str):
    pylib = get_python_lib()
    original = os.path.abspath(path)
    root_path, target = os.path.split(original)
    dest = os.path.join(pylib, target)
    return original, dest, root_path, pylib


def create_symlink(path: str) -> int:
    original, dest, root_path, pylib = get_path_info(path)
    #
    print(sh("ln -sfnv %s %s" % (original, dest)))
    #
    setup = os.path.join(root_path, "setup.py")
    if os.path.isfile(setup):
        eggdir = None
        current = os.getcwd()
        try:
            os.chdir(root_path)
            print(sh("%s setup.py egg_info" % sys.executable))
            for name in os.listdir(root_path):
                if name.endswith(".egg-info"):
                    eggdir = name
                    break
        finally:
            os.chdir(current)

        if eggdir:
            original = os.path.join(root_path, eggdir)
            dest = os.path.join(pylib, eggdir)
            print(sh("ln -sfnv %s %s" % (original, dest)))
    return 0


def extract_setup_name(setup_path):
    """
    Extract the name field from the setup() function in setup.py.

    Args:
        setup_path (str): Path to the setup.py file.

    Returns:
        str: The value of the name field if found, else None.
    """
    try:
        with open(setup_path, 'r', encoding='utf-8') as file:
            setup_code = file.read()
    except IOError as e:
        print(f"Error reading {setup_path}: {e}")
        return None

    try:
        tree = ast.parse(setup_code)
    except SyntaxError as e:
        print(f"Syntax error in {setup_path}: {e}")
        return None
    for node in ast.walk(tree):
        if isinstance(node, ast.Call) and isinstance(node.func, ast.Name) and node.func.id == 'setup':
            for keyword in node.keywords:
                if keyword.arg == 'name':
                    if isinstance(keyword.value, ast.Constant):
                        return keyword.value.value

    return None


def remove_symlink(path: str) -> int:
    original, dest, root_path, pylib = get_path_info(path)

    if os.path.islink(dest):
        os.unlink(dest)
        print(f"Removed symlink: {dest}")
    else:
        print(f"No symlink found: {dest}")

    setup_path = os.path.join(root_path, "setup.py")
    if os.path.isfile(setup_path):
        if package_name := extract_setup_name(setup_path):
            package_name += ".egg-info"
            egginfo_path = os.path.join(pylib, package_name)
            if os.path.isdir(egginfo_path) and os.path.islink(egginfo_path):
                os.unlink(egginfo_path)
                print(f"Removed egg-info symlink: {egginfo_path}")
    return 0


def main() -> int:
    argv = sys.argv
    if len(argv) != 3:
        print("Usage: pyslink <create/remove> <path_to_target>")
        return 1

    action, path = argv[1], argv[2]

    if action == "create":
        return create_symlink(path)
    elif action == "remove":
        return remove_symlink(path)
    else:
        print("Invalid action. Use 'create' or 'remove'.")
        return 1


if __name__ == "__main__":
    sys.exit(main())
