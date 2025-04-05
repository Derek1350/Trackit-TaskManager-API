import os
from .dev import DevConfig
from .prod import ProdConfig
from .staging import StagingConfig

def get_config():
    env = os.getenv("FLASK_ENV", "development").lower()

    if env == "production":
        return ProdConfig
    elif env == "staging":
        return StagingConfig
    else:
        return DevConfig
