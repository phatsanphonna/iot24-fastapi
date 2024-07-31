from pydantic import BaseModel


class MenuDTO(BaseModel):
    name: str
    price: float

