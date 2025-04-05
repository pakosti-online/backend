from pydantic import BaseModel, StringConstraints, condecimal
from typing import Annotated, Optional, Dict, Union


class NotificationsDto(BaseModel):
    text: str
