import importlib
import logging

from fast_zero.config.settings import INSTALLED_APPS

logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.INFO)

for app in INSTALLED_APPS:
    try:
        importlib.import_module(f"{app}.models")
    except ModuleNotFoundError as e:
        logger.error(e)
        continue
