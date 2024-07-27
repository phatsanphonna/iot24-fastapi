from pydantic import BaseModel

class OrderDTO(BaseModel):
    menu_id: int
    quantity: int


