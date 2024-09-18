import importlib
import logging
import os
import sys
from pathlib import Path

logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.INFO)


def import_models_in_current_path():
    base_path = Path(__file__).parent

    for root, dirs, files in os.walk(base_path):
        if "models.py" in files:
            relative_path = Path(root).relative_to(base_path)
            module_name = ".".join(relative_path.parts) + ".models"
            try:
                importlib.import_module(module_name)
                logger.info(f"Successfully imported {module_name}")
            except ModuleNotFoundError as e:
                logger.error(f"Failed to import {module_name}: {e}")
            except Exception as e:
                logger.error(f"An error occurred while importing {module_name}: {e}")


sys.path.append(str(Path(__file__).parent))
import_models_in_current_path()
