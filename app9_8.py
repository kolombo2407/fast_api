import psycopg2
from fastapi import FastAPI, HTTPException, Depends
from psycopg2.extras import RealDictCursor
from pydantic import BaseModel

from loguru import logger

app = FastAPI()


class GetUser(BaseModel):
    gender: int
    age: int
    city: str

    class Config:
        orm_mode = True


class PostResponse(BaseModel):
    id: int
    text: str
    topic: str

    class Config:
        orm_mode = True


def get_db():
    conn = psycopg2.connect(
        "postgresql://robot-startml-ro:pheiph0hahj1Vaif@postgres.lab.karpov.courses:6432/startml",
        cursor_factory=RealDictCursor,
    )
    logger.info("get_db worked")
    return conn


def user_id(u_id: int):
    return u_id


def post_id(id: int):
    return id


@app.get("/user/{u_id}", response_model=GetUser, dependencies=[Depends(get_db), Depends(user_id)])
def get_user(db=Depends(get_db), u_id=Depends(user_id)):
    cursor = db.cursor()
    logger.info(db)
    cursor.execute(
        """
        SELECT gender, age, city
        FROM "user"
        WHERE id = %s
        """, [u_id]
    )
    result = cursor.fetchone()
    logger.info(result)
    if not result:
        raise HTTPException(404, 'user not found')
    else:
        return result


@app.get('/post/{id}', response_model=PostResponse, dependencies=[Depends(get_db), Depends(post_id)])
def get_post(db=Depends(get_db), id=Depends(post_id)) -> PostResponse:
    cursor = db.cursor()
    cursor.execute(
        '''
        SELECT id, text, topic
        FROM post
        WHERE id = %s
        ''', [id]
    )
    result = cursor.fetchone()
    logger.info(result)
    if not result:
        raise HTTPException(404, "post not found")
    else:
        return result
