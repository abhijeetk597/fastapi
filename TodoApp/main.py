from fastapi import FastAPI, Depends, HTTPException, Path
from starlette import status
from typing import Annotated
from sqlalchemy.orm import Session
import models
from database import engine, SessionLocal
from models import Todos
from pydantic import BaseModel

app = FastAPI()

models.Base.metadata.create_all(bind=engine)

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

db_dependancy = Annotated[Session, Depends(get_db)]

class TodoRequest(BaseModel):
    title: str
    description: str
    priority: int
    complete: bool


@app.get("/", status_code=status.HTTP_200_OK)
async def read_all(db: db_dependancy):
    return db.query(Todos).all()

@app.get("/todo/{todo_id}", status_code=status.HTTP_200_OK)
async def read_todo(db: db_dependancy, todo_id: int = Path(gt=0)):
    todo_model = db.query(Todos).filter(Todos.id == todo_id).first()
    if todo_model is not None:
        return todo_model
    raise HTTPException(status_code=404, detail='Todo not found')