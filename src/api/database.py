import os

import pymongo
from markkk.logger import logger

_USER = os.environ.get("_DB_USER", "REPLACE_ME")
_PASS = os.environ.get("_DB_PASS", "REPLACE_ME")
_NAME = os.environ.get("_DB_NAME", "REPLACE_ME")

try:
    if _USER.endswith("ME"):
        from .db_secrete import _DB_NAME, _DB_PASS, _DB_USER
    else:
        _DB_USER = _USER
        _DB_PASS = _PASS
        _DB_NAME = _NAME
except ImportError:
    logger.error("No Database Config Found.")

logger.info(
    f"""-----------------------------------
            MongoDB config:
            
            User: {_DB_USER}
            Database Name: {_DB_NAME}
         -----------------------------------
"""
)


client = pymongo.MongoClient(
    f"mongodb+srv://{_DB_USER}:{_DB_PASS}@clusteresc.xvunj.mongodb.net/{_DB_NAME}?retryWrites=true&w=majority",
    ssl=True,
)

db = client[f"{_DB_NAME}"]
db_available = False

try:
    # The ismaster command is cheap and does not require auth.
    db.command("ismaster")
    logger.debug("DB Server OK")
    db_available = True
except pymongo.errors.ConnectionFailure:
    logger.error("DB Server Not Available")

### MongoDB Collection Reference ###
# User
users_collection = db["users"]
# Admin
admins_collection = db["admins"]
# Student
students_collection = db["students"]
# ApplicationForm
applications_collection = db["applications"]
# ApplicationPeriod
application_periods_collection = db["application_periods"]
# Contract
contracts_collection = db["contracts"]
# Event
events_collection = db["events"]
# DisciplinaryRecord
records_collection = db["records"]
# Room
rooms_collection = db["rooms"]
