# -*- coding: utf-8 -*-
# @Time : 2024/01/01 16:18
# @Author : FQY
# @File : main.py

from fastapi import FastAPI, Depends, HTTPException, Request
from fastapi.encoders import jsonable_encoder
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from sqlalchemy.orm import Session
from contextlib import asynccontextmanager

from src import models, schemas, crud
from src.database import SessionLocal, engine

models.Base.metadata.create_all(bind=engine)


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@asynccontextmanager
async def lifespan(app: FastAPI):
    # startup operations
    db_ = get_db()
    db = next(db_)
    # create empty tag, and all records will be tagged with it by default
    if not crud.get_tag_by_name(db, name=""):
        crud.create_tag(db, schemas.TagPost(name=""))
    yield
    # shutdown operations
    ...


app = FastAPI(lifespan=lifespan)

# CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.exception_handler(crud.CRUDError)
async def custom_exception_handler(_: Request, exc: crud.CRUDError):
    """
    Handle CRUD error globally, don't need to handle it in each endpoint if the error is caused by CRUD operation
    """
    rsp_model = schemas.BadResponse(msg=exc.err_msg)
    return JSONResponse(content=jsonable_encoder(rsp_model), status_code=rsp_model.code)


@app.get("/tags/", response_model=schemas.RspTagList)
def get_tags(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    """Get all tags"""
    db_tags = crud.get_tags(db, skip=skip, limit=limit)
    return schemas.RspTagList(data=db_tags)


@app.get("/tags/{tag_id}", response_model=schemas.RspTag)
def get_tag(tag_id: int, db: Session = Depends(get_db)):
    db_tag = crud.get_tag(db, id=tag_id)
    return schemas.RspTag(data=db_tag)


@app.delete("/tags/{tag_id}", response_model=schemas.GenericResponse)
def delete_tag(tag_id: int, db: Session = Depends(get_db)):
    crud.delete_tag(db, id=tag_id)
    return schemas.GenericResponse(msg="Tag deleted")


@app.post("/tags/", response_model=schemas.RspTag)
def create_tag(db_tag: schemas.TagPost, db: Session = Depends(get_db)):
    db_tag = crud.create_tag(db, db_tag)
    return schemas.RspTag(data=db_tag)


@app.put("/tags/{tag_id}", response_model=schemas.RspTag)
def update_tag(tag_id: int, db_tag: schemas.TagPost, db: Session = Depends(get_db)):
    db_tag = crud.update_tag(db, id=tag_id, tag=db_tag)
    return schemas.RspTag(data=db_tag)


@app.get("/records/", response_model=schemas.RspRecordList)
def get_records(skip: int = 0, limit: int = 100, tag_id: int = None, db: Session = Depends(get_db)):
    if tag_id:
        db_records = crud.get_records_by_tag(
            db, tag_id=tag_id, skip=skip, limit=limit
        )
    else:
        db_records = crud.get_records(db, skip=skip, limit=limit)
    return schemas.RspRecordList(data=db_records)


@app.get("/records/{record_id}", response_model=schemas.RspRecord)
def get_record(record_id: int, db: Session = Depends(get_db)):
    db_record = crud.get_record(db, id=record_id)
    return schemas.RspRecord(data=db_record)


@app.delete("/records/{record_id}", response_model=schemas.GenericResponse)
def delete_record(record_id: int, db: Session = Depends(get_db)):
    crud.delete_record(db, id=record_id)
    return schemas.GenericResponse(msg="Record deleted")


@app.post("/records/", response_model=schemas.RspRecord)
def create_record(record: schemas.RecordPost, db: Session = Depends(get_db)):
    db_record = crud.create_record(db, record)
    return schemas.RspRecord(data=db_record)


@app.put("/records/{record_id}", response_model=schemas.RspRecord)
def update_record(record_id: int, record: schemas.RecordPost, db: Session = Depends(get_db)):
    db_record = crud.update_record(db, id=record_id, record=record)
    return schemas.RspRecord(data=db_record)


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
