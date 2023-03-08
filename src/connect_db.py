import os
import logging
from sqlalchemy import create_engine

required_env_vars = [
    "DATABASE_URL",
    "PGDATABASE",
    "PGHOST",
    "PGPASSWORD",
    "PGPORT",
    "PGUSER",
]

def get_engine():
    any_missing = False
    for env_var in required_env_vars:
        if env_var not in os.environ:
            logging.warning(f"Missing environment variable: {env_var}")
            any_missing = True

    if any_missing:
        return create_engine('sqlite:///db/chat.db')
    else:
        url = f"postgresql://{os.environ['PGUSER']}:{os.environ['PGPASSWORD']}@{os.environ['PGHOST']}:{os.environ['PGPORT']}/{os.environ['PGDATABASE']}"
        return create_engine(url)
