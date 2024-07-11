from pydantic import BaseModel

class StudentDTO(BaseModel):
    firstname: str
    lastname: str
    student_id: str
    date_of_birth: str