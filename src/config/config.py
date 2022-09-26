import os
from pathlib import Path

import data

DATA_DIR = Path(data.__file__).parent

# for logger folder name
APP_ENV = os.environ.get("APP_ENV") or ""


IS_DEV = os.environ.get("APP_ENV") == "development"


IS_PROD = os.environ.get("APP_ENV") == "production"


IS_TESTING = bool(os.environ.get("TESTING"))


def is_cicd():
    return bool(os.environ.get("CICD"))
