from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from database import get_db
from dto.student import StudentDTO
from model.student import Student
from model.student import Student

student_router = APIRouter(prefix='/students')

@student_router.get("/")
async def get_students(db: Session = Depends(get_db)):
    return db.query(Student).all()


@student_router.get("/{student_id}")
async def get_student_by_id(student_id: int, db: Session = Depends(get_db)):
    student = db.query(Student).filter(Student.id == student_id).first()
    
    if not student:
        raise HTTPException(status_code=404, detail="Student not found")
    
    return student


@student_router.post("/")
async def create_student(student_dto: StudentDTO, db: Session = Depends(get_db)):
    student = Student()
    student.firstname = student_dto.firstname
    student.lastname = student_dto.lastname
    student.student_id = student_dto.student_id
    student.date_of_birth = student_dto.date_of_birth

    db.add(student)
    db.commit()
    db.refresh(student)
    return student


@student_router.delete("/students/{student_id}")
async def delete_student_by_id(student_id: int, db: Session = Depends(get_db)):
    student = db.query(Student).filter(Student.id == student_id).first()

    if not student:
        raise HTTPException(status_code=404, detail="Student not found")

    db.delete(student)
    db.commit()
    return {'success': True, 'message': 'Student deleted successfully'}


@student_router.patch("/{student_id}")
async def edit_student(student_id: int, student_dto: StudentDTO, db: Session = Depends(get_db)):
    student_to_edit = db.query(Student).filter(Student.id == student_id).first()
    
    if not student_to_edit:
        raise HTTPException(status_code=404, detail="Student not found")

    student_to_edit.firstname = student_dto.firstname
    student_to_edit.lastname = student_dto.lastname
    student_to_edit.student_id = student_dto.student_id
    student_to_edit.date_of_birth = student_dto.date_of_birth
    db.commit()
    db.refresh(student_to_edit)
    return {'success': True, 'message': 'Student updated successfully'}