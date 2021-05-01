from fastapi import FastAPI, Depends, status, Response, HTTPException
from . import schema, model
from .database import engine, SessionLocal
from sqlalchemy.orm import Session

app = FastAPI()
model.Base.metadata.create_all(engine)


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@app.post('/blog', status_code=status.HTTP_201_CREATED)
def create(request: schema.Blog, db: Session = Depends(get_db)):
    new_blog = model.Blog(title=request.title, body=request.body)
    db.add(new_blog)
    db.commit()
    db.refresh(new_blog)
    return new_blog


@app.get("/blog")
def all(db: Session = Depends(get_db)):
    blogs = db.query(model.Blog).all()
    return blogs


@app.get('/blog/{id}')
def show(id, db: Session = Depends(get_db)):
    blog = db.query(model.Blog).filter(model.Blog.id == id).first()
    if not blog:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail={'detail': f"Blog with id {id} is not available"})
    return blog


@app.delete('/blog/{id}')
def delete(id, db: Session = Depends(get_db)):
    blog = db.query(model.Blog).filter(model.Blog.id == id).first()
    if not blog:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail={'detail': f"Blog with id {id} is not available"})
    db.query(model.Blog).filter(model.Blog.id == id).delete(synchronize_session=False)
    db.commit()
    return {'detail': 'Blog successful deleted'}


@app.put('/blog/{id}', status_code=status.HTTP_202_ACCEPTED)
def update(id, request: schema.Blog, db: Session = Depends(get_db)):
    blog = db.query(model.Blog).filter(model.Blog.id == id).first()
    if not blog:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail={'detail': f"Blog with id {id} is not available"})

    db.query(model.Blog).filter(model.Blog.id == id) \
        .update({model.Blog.title: request.title, model.Blog.body: request.body}, synchronize_session=False)
    db.commit()

    return {'detail': 'Successfully updated'}
