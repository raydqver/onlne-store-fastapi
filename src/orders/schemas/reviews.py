from pydantic import BaseModel, Field
from typing import Annotated


class ReviewInSchema(BaseModel):
    text: str
    rate: Annotated[int, Field(ge=1, le=5)]
