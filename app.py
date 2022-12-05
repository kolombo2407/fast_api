from fastapi import FastAPI
from datetime import date
from pydantic import BaseModel
import json

app = FastAPI()


class User(BaseModel):
    name: str
    surname: str
    age: int
    registration_date: date

    # class Config:
    #     orm_mode = True


@app.post("/user/validate")
def user_validate(json_file: User):
    return f"Will add user: {json_file.name} {json_file.surname} with age {json_file.age}"
