#Python
from typing import Optional

# Pydantic
from pydantic import BaseModel

# FastAPI
from fastapi import FastAPI, Query
from fastapi import Body
app = FastAPI()

# Models
class Person(BaseModel):
    firs_name: str
    last_name: str
    age: int
    hair_color: Optional[str] = None 
    is_married: Optional[bool] = None


@app.get("/")
def home():
    return {"Hello": "World"}

# Request and Response Body
@app.post("/person/new/")
def new_person(person: Person = Body(...)):
    return person


# Validations: Query Parameters

@app.get("/person/detail")
def show_person(
    name : Optional[str] = Query(None, min_length=1,max_length=50),
    age = Query(...)
):
    return{'name':name,'age':age}