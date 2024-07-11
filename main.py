from fastapi import FastAPI, Depends
from dotenv import load_dotenv
from sqlalchemy.orm import Session
from fastapi.middleware.cors import CORSMiddleware
from model.student import Student
from database import SessionLocal, engine, Base
from dto.student import StudentDTO

load_dotenv()

def get_db():
    db = SessionLocal()

    try:
        yield db
    finally:
        db.close()

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
def get_root():
    return {'message': 'Hello World'}


@app.get("/students")
async def get_students(db: Session = Depends(get_db)):
    return db.query(Student).all()


@app.get("/students/{student_id}")
async def get_student_by_id(student_id: int, db: Session = Depends(get_db)):
    return db.query(Student).filter(Student.id == student_id).first()


@app.post("/students")
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


@app.delete("/students/{student_id}")
async def delete_student_by_id(student_id: int, db: Session = Depends(get_db)):
    student = db.query(Student).filter(Student.id == student_id).first()
    db.delete(student)
    db.commit()
    return {'message': 'Student deleted successfully'}


@app.patch("/students/{student_id}")
async def edit_student(student_id: int, student_dto: StudentDTO, db: Session = Depends(get_db)):
    student_to_edit = db.query(Student).filter(Student.id == student_id).first()
    student_to_edit.firstname = student_dto.firstname
    student_to_edit.lastname = student_dto.lastname
    student_to_edit.student_id = student_dto.student_id
    student_to_edit.date_of_birth = student_dto.date_of_birth
    db.commit()
    db.refresh(student_to_edit)
    return {'message': 'Student updated successfully'}


@app.get('/triangle/{base}/{height}')
def get_triangle_area(base: int, height: int):
    return {'area': 0.5 * base * height}

if __name__ == '__main__':
    import uvicorn
    uvicorn.run(app)