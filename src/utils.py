import importlib.util
import os

from fastapi import FastAPI


def load_routers(app: FastAPI, router_dir: str = "src"):
    """
    Load FastAPI router modules from a specified directory and add them to the app.
    Will take './src' as default

    Args:
        app (FastAPI): The FastAPI app instance to add the routers to.
        router_dir (str): The path to the directory containing the router modules.
    """
    # Traverse the directory tree and find all router modules
    for root, _, files in os.walk(router_dir):
        for module_file in files:
            if module_file.endswith(".py") and module_file != "__init__.py":
                module_name = module_file[:-3]  # Remove ".py" extension
                module_path = os.path.join(root, module_name).replace(os.sep, ".")
                module = importlib.import_module(module_path)
                router = getattr(module, "router", None)
                if router:
                    app.include_router(router)
