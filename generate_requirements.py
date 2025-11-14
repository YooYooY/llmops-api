import ast
import importlib.metadata
import os
from typing import Set, Dict

EXCLUDE_DIRS = {
    "venv", "tests", "tmp", "storage", ".git",
    "__pycache__", ".idea", ".vscode"
}

PROJECT_DIR = "."


class Color:
    GREEN = "\033[92m"
    YELLOW = "\033[93m"
    RED = "\033[91m"
    CYAN = "\033[96m"
    END = "\033[0m"


def log_info(msg): print(f"{Color.CYAN}[INFO]{Color.END} {msg}")


def log_warn(msg): print(f"{Color.YELLOW}[WARN]{Color.END} {msg}")


def log_success(msg): print(f"{Color.GREEN}[OK]{Color.END}  {msg}")


def log_error(msg): print(f"{Color.RED}[ERR]{Color.END}  {msg}")


def is_excluded(path: str) -> bool:
    return bool(set(path.split(os.sep)) & EXCLUDE_DIRS)


def scan_imports() -> Set[str]:
    log_info("Scanning project for Python imports...")
    imports = set()

    for root, _, files in os.walk(PROJECT_DIR):
        if is_excluded(root):
            continue

        for file in files:
            if not file.endswith(".py"):
                continue

            filepath = os.path.join(root, file)
            log_info(f"Parsing: {filepath}")

            try:
                content = open(filepath, "r", encoding="utf8").read()
                tree = ast.parse(content)
            except Exception as e:
                log_warn(f"Skipped (parse error): {filepath}, Reason: {e}")
                continue

            for node in ast.walk(tree):
                if isinstance(node, ast.Import):
                    for n in node.names:
                        imports.add(n.name.split(".")[0])
                elif isinstance(node, ast.ImportFrom):
                    if node.module:
                        imports.add(node.module.split(".")[0])

    log_success(f"Found {len(imports)} unique imports.")
    return imports


def map_imports(imports: Set[str]) -> Dict[str, str]:
    installed = {
        dist.metadata["Name"].lower(): dist.version
        for dist in importlib.metadata.distributions()
    }

    module_to_pkg = {}
    for dist in importlib.metadata.distributions():
        top = dist.read_text("top_level.txt")
        if top:
            for m in top.splitlines():
                module_to_pkg[m.lower()] = dist.metadata["Name"].lower()

    mapped = {}
    for imp in imports:
        low = imp.lower()

        if low in installed:
            mapped[imp] = low
        elif low in module_to_pkg:
            mapped[imp] = module_to_pkg[low]

    return mapped


def generate_requirements():
    imports = scan_imports()
    mapped = map_imports(imports)

    installed = {
        dist.metadata["Name"].lower(): dist.version
        for dist in importlib.metadata.distributions()
    }

    reqs = []

    for imp in sorted(imports):
        if imp in mapped:
            pkg = mapped[imp]
            version = installed.get(pkg)
            if version:
                req = f"{pkg}=={version}"
                reqs.append(req)
                log_success(f"Detected dependency: {req}")
        else:
            log_warn(f"Not a third-party package or missing: {imp}")

    with open("requirements.txt", "w") as f:
        f.write("\n".join(sorted(reqs)))

    log_success("requirements.txt generated successfully.")


if __name__ == "__main__":
    log_info("Starting enhanced dependency generator (clean version)...")
    generate_requirements()
    log_success("Done.")
