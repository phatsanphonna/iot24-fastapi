from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from database import get_db
from dto.book import BookDTO
from model.book import Book

book_router = APIRouter(prefix='/books')

@book_router.get("/")
async def get_books(db: Session = Depends(get_db)):
    return db.query(Book).all()


@book_router.get("/{book_id}")
async def get_book_by_id(book_id: int, db: Session = Depends(get_db)):
    book = db.query(Book).filter(Book.id == book_id).first()
    
    if not book:
        raise HTTPException(status_code=404, detail="Book not found")
    
    return book


@book_router.post("/")
async def create_book(book: BookDTO, db: Session = Depends(get_db)):
    db.add(book)
    db.commit()
    db.refresh(book)
    return book


@book_router.delete("/books/{book_id}")
async def delete_book_by_id(book_id: int, db: Session = Depends(get_db)):
    book = db.query(Book).filter(Book.id == book_id).first()

    if not book:
        raise HTTPException(status_code=404, detail="Book not found")

    db.delete(book)
    db.commit()
    return {'success': True, 'message': 'Book deleted successfully'}