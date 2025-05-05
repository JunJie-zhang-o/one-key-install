


import importlib
from pathlib import Path


def load_modules(module_path:Path, package_name:str):
    if module_path.is_file():
        importlib.import_module(module_path.stem)
    elif module_path.is_dir():
        for file in module_path.iterdir():
            if file.is_file():
                index = file.parts.index(package_name)
                if index >= 0:
                    importlib.import_module(".".join(file.parts[index:])[:-3])  
                else:
                    ModuleNotFoundError(f"package not found | package_name:{package_name}")
            elif file.is_dir():
                load_modules(file)










