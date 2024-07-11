
from sqlalchemy import Column, Integer, String

from database import Base

# from sqlalchemy.orm import relationship


class Student(Base):
    __tablename__ = 'student'

    id = Column(Integer, primary_key=True, index=True)
    firstname = Column(String, index=True)
    lastname = Column(String, index=True)
    student_id = Column(String, index=True)
    date_of_birth = Column(String, index=True)

