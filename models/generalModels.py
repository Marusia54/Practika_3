from pydantic import BaseModel
from enum import Enum


class Tags(Enum):
    main = "Main Controller"
    disciplines = "Disciplines"
    directors = "Directors"


class NewResponse(BaseModel):
    message: str
