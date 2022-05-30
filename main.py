#Python
from typing import Optional
from enum import Enum
from typing import List
# Pydantic
from pydantic import BaseModel, EmailStr
from pydantic import Field
from pydantic import SecretStr
# FastAPI
from fastapi import FastAPI, File, Form, Header,Cookie, Path, Query, UploadFile, status
from fastapi import Body, HTTPException

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
class PersonBase(BaseModel):
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
    class Config:
        schema_extra = {
            "example" : {
                "first_name":"Bruce",
                "last_name": "Wayne",
                "age":30,
                "hair_color":"black",
                "is_married":False,
                "password":"hello_world",
                
            }
        }
class PersonOut(PersonBase):
    pass    
class Person(PersonBase):
    password: str = Field(...,min_length=8)
class LoginOut(BaseModel):
    username:str = Field(...,max_length=20, example="LasterLG117")

@app.get(
    path="/",
    status_code=status.HTTP_200_OK
    )
def home():
    return {"Hello": "World"}

# Request and Response Body
@app.post(
    path="/person/new/",
    status_code=status.HTTP_201_CREATED, 
    response_model=PersonOut
    )
def new_person(person: Person = Body(...)):
    return person


# Validations: Query Parameters

@app.get(
    path="/person/detail",
    status_code=status.HTTP_200_OK 
    )
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
persons = [1,2,3,4,5,117]
@app.get(
    path="/person/detail/{person_id}",
    status_code=status.HTTP_200_OK
    )
def show_person(
    person_id: int = Path(
        ...,
        gt=0,
        example=117,
        title="person id",
        description="This is the person id. It's required"
        )
):
    if person_id not in persons:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="This person doesn't exist"
        )
    return{'person_id':person_id,'name':'Bruce','age':30}



# Validations: RequestBody Parameters
@app.put(
    path="/person/{person_id}",
    status_code=status.HTTP_200_OK
    )
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


 # Forms

@app.post(
    path="login",
    response_model=LoginOut,
    status_code=status.HTTP_200_OK
)
def login(
    username: str = Form(...),
    password: SecretStr = Form(...)
):
    return LoginOut

# Cookies and Headers Parameters

@app.post(
    path="/contact/",
    status_code=status.HTTP_200_OK
)
def contact(
    fisrt_name: str = Form(
        ...,
        min_length=1,
        max_length=20,
    ),
    last_name: str = Form(
        ...,
        min_length=1,
        max_length=20,
    ),
    email: EmailStr = Form(...),
    message: str = Form(
        min_length=20
    ),
    user_agent: Optional[str] = Header(default=None),
    ads: Optional[str] = Cookie(default=None)
    
):
    return user_agent

# Files
@app.post(
    path="/post-image",
    status_code=status.HTTP_201_CREATED
)
def post_image(
    image: UploadFile = File(...)
):
    return {
        "Filename":image.filename,
        "Format":image.content_type,
        "Size(kb)":round(len(image.file.read())/1024, ndigits=2),
        "file":image
    }


@app.post(
    path='/post-multi-image'
)
def post_image(
    images: List[UploadFile] = File(...)
):
    info_images = [{
        "filename": image.filename,
        "Format": image.content_type,
        "Size(kb)": round(len(image.file.read())/1024, ndigits=2)
    } for image in images]

    return info_images

