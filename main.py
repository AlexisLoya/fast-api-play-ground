#Python
from operator import gt
from typing import Optional

# Pydantic
from pydantic import BaseModel

# FastAPI
from fastapi import FastAPI, Path, Query
from fastapi import Body
app = FastAPI()

# Models
class Location(BaseModel):
    city: str
    state: str
    country: str

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
    name : Optional[str] = Query(
        None,
        min_length=1,
        max_length=50,
        title="person name",
        description="This is the person name. It's between 1-50 characters"
        ),
    age = Query(
        ...,
        title="person age",
        description="This is the person age. It's required"
        )
):
    return {'name':name,'age':age}


# Validations: Path Parameters
@app.get("/person/detail/{person_id}")
def show_person(
    person_id: int = Path(
        ...,
        gt=0,
        title="person id",
        description="This is the person id. It's required"
        
        )
):
    return{'person_id':person_id,'name':'Bruce','age':30}



# Validations: RequestBody Parameters
@app.put("/person/{person_id}")
def update_person(
    person_id : int = Path(
     ...,
     title='Person Id',
     description='This is the person id',
     gt=0   
    ),
    person : Person = Body(
        ...,
        title='The person to update',
        description='data to update'
    ),
    location : Location = Body(
        ...,
        title='The person to update',
        description='data to update'
    )
    
):  
    response = person.dict()
    response.update(location.dict())
    return response