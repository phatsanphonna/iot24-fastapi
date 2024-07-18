from dotenv import load_dotenv
from fastapi import APIRouter, FastAPI, Depends, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session

from database import get_db

from dto.book import BookDTO
from dto.student import StudentDTO

from model.book import Book
from model.student import Student

from database import Base, engine

load_dotenv()

app = FastAPI()
router_v1 = APIRouter(prefix='/api/v1')

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

@router_v1.get("/books")
async def get_books(db: Session = Depends(get_db)):
    return db.query(Book).all()


@router_v1.get("/books/{book_id}")
async def get_book_by_id(book_id: int, db: Session = Depends(get_db)):
    book = db.query(Book).filter(Book.id == book_id).first()
    
    if not book:
        raise HTTPException(status_code=404, detail="Book not found")
    
    return book


@router_v1.post("/books")
async def create_book(book: BookDTO, db: Session = Depends(get_db)):
    db.add(book)
    db.commit()
    db.refresh(book)
    return book


@router_v1.delete("/books/{book_id}")
async def delete_book_by_id(book_id: int, db: Session = Depends(get_db)):
    book = db.query(Book).filter(Book.id == book_id).first()

    if not book:
        raise HTTPException(status_code=404, detail="Book not found")

    db.delete(book)
    db.commit()
    return {'success': True, 'message': 'Book deleted successfully'}


@router_v1.get("/students")
async def get_students(db: Session = Depends(get_db)):
    return db.query(Student).all()


@router_v1.get("/students/{student_id}")
async def get_student_by_id(student_id: int, db: Session = Depends(get_db)):
    student = db.query(Student).filter(Student.id == student_id).first()
    
    if not student:
        raise HTTPException(status_code=404, detail="Student not found")
    
    return student


@router_v1.post("/students")
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


@router_v1.delete("/students/{student_id}")
async def delete_student_by_id(student_id: int, db: Session = Depends(get_db)):
    student = db.query(Student).filter(Student.id == student_id).first()

    if not student:
        raise HTTPException(status_code=404, detail="Student not found")

    db.delete(student)
    db.commit()
    return {'success': True, 'message': 'Student deleted successfully'}


@router_v1.patch("/students/{student_id}")
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


@app.get('/triangle/{base}/{height}')
def get_triangle_area(base: int, height: int):
    return {'area': 0.5 * base * height}


app.include_router(router_v1)

if __name__ == '__main__':
    import uvicorn
    Base.metadata.create_all(bind=engine)
    uvicorn.run(app)