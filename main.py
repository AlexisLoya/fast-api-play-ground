#Python
from operator import gt
from typing import Optional
from enum import Enum
from click import password_option

# Pydantic
from pydantic import BaseModel
from pydantic import Field

# FastAPI
from fastapi import FastAPI, Path, Query
from fastapi import Body
app = FastAPI()

# Models

class HairColor(Enum): 
    white = "white"
    brown = "brown"
    black = "black"
    blonde = "blonde"
    red = "red"

class Location(BaseModel):
    city: str = Field(
        ...,
        min_length=1,
        max_length=30,
        )
    state: str = Field(
        ...,
        min_length=1,
        max_length=30,
        )
    country: str = Field(
        ...,
        min_length=1,
        max_length=30,
        )

    class Config:
        schema_extra = {
            "example" : {
                "city":"Gotham",
                "state": "New York",
                "country":"USA"
            }
        }

class PersonOut(BaseModel):
    first_name: str = Field(
        ...,
        min_length=1,
        max_length=50,
        )
    last_name: str = Field(
        ...,
        min_length=1,
        max_length=50,
        )
    age: int = Field(
        ...,
        gt=0,
        le=130,
        )
    hair_color: Optional[HairColor] = Field(default=None, example=HairColor.black)
    is_married: Optional[bool] = Field(default=None)
    
class Person(BaseModel):
    first_name: str = Field(
        ...,
        min_length=1,
        max_length=50,
        )
    last_name: str = Field(
        ...,
        min_length=1,
        max_length=50,
        )
    age: int = Field(
        ...,
        gt=0,
        le=130,
        )
    hair_color: Optional[HairColor] = Field(default=None) 
    is_married: Optional[bool] = Field(default=None)
    password: str = Field(...,min_length=8)
    class Config:
        schema_extra = {
            "example" : {
                "first_name":"Bruce",
                "last_name": "Wayne",
                "age":30,
                "hair_color":"white",
                "is_married":False,
                "password":"hello_world",
                
            }
        }


@app.get("/")
def home():
    return {"Hello": "World"}

# Request and Response Body
@app.post("/person/new/", response_model=PersonOut)
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
    age: int  = Query(
        ...,
        gt=0,
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
    # location : Location = Body(
    #     ...,
    #     title='The person to update',
    #     description='data to update'
    # )
    
):  
    response = person.dict()
    # response.update(location.dict())
    return response