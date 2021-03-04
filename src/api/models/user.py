from typing import Dict, List, Optional

from markkk.logger import logger
from pydantic import BaseModel


class User(BaseModel):
    username: str
    password: str


class Admin(User):
    full_name: str
    email_sutd: str
    read_only_privilege: bool = False