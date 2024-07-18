from sqlalchemy import ARRAY, Boolean, Column, Integer, String
from database import Base

class Book(Base):
    __tablename__ = 'book'

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, index=True)
    description = Column(String, index=True)
    short_description = Column(String, index=True)
    category = Column(ARRAY(String), index=True)
    author = Column(String, index=True)
    year = Column(Integer, index=True)
    is_published = Column(Boolean, index=True)