from pydantic import BaseModel


class BookDTO(BaseModel):
    title: str
    author: str
    year: int
    is_published: bool
    description: str
    short_description: str
    category: list[str]
