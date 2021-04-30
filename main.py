from typing import Optional

from fastapi import FastAPI
from pydantic import BaseModel

app = FastAPI()


@app.get("/")
def index():
    return {'data': 'index page'}


@app.get('/blog/unpublished')
def unpublished():
    return {'data': 'all unpublished blogs'}


@app.get('/blog/{id}')
def show(id: int):
    return {'data': id}


@app.get('/blog/{id}/comments')
def comments(id: int):
    return {'data': {'comments': [1, 2]}}


@app.get("/about")
def about():
    return {'data': {'name': 'About Page'}}


# limit
@app.get("/blog")
def getlimit(limit=10, published: bool = True, sort: Optional[str] = None):
    # only get 10 published blogs
    if published:
        return {'data': f'{limit} published blogs from the db'}
    else:
        return {'data': f'{limit} blogs from the db'}


class Blog(BaseModel):
    title: str
    body: str
    year: int
    publish: Optional[bool]


@app.post("/blog")
def create_blog(request: Blog):
    return request
