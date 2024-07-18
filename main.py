from dotenv import load_dotenv
from fastapi import APIRouter, FastAPI
from fastapi.middleware.cors import CORSMiddleware
from routes.student import student_router

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



@app.get('/triangle/{base}/{height}')
def get_triangle_area(base: int, height: int):
    return {'area': 0.5 * base * height}

if __name__ == '__main__':
    import uvicorn
    Base.metadata.create_all(bind=engine)
    router_v1.include_router(student_router)
    app.include_router(router_v1)
    uvicorn.run(app)