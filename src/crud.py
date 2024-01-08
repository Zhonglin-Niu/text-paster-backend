from sqlalchemy.orm import Session

from . import models, schemas


class CRUDError(Exception):
    def __init__(self, err_msg: str):
        self.err_msg = err_msg


def get_tags(db: Session, skip: int = 0, limit: int = 100):
    # skip + 1 to avoid return first empty tag
    return db.query(models.Tag).offset(skip+1).limit(limit).all()


def get_tag(db: Session, id: int):
    db_tag = db.query(models.Tag).filter(models.Tag.id == id).first()
    if db_tag is None:
        raise CRUDError("Tag not found")
    return db_tag


def get_tag_by_name(db: Session, name: str):
    return db.query(models.Tag).filter(models.Tag.name == name).first()


def create_tag(db: Session, tag: schemas.TagPost):
    if get_tag_by_name(db, name=tag.name):
        raise CRUDError("Tag already exists")
    db_tag = models.Tag(**tag.model_dump())
    db.add(db_tag)
    db.commit()
    db.refresh(db_tag)
    return db_tag


def delete_tag(db: Session, id: int):
    delete_num = db.query(models.Tag).filter(models.Tag.id == id).delete()

    # update all records with this tag to default tag
    db.query(models.Record)\
        .filter(models.Record.tag_id == id)\
        .update({"tag_id": 1})

    if delete_num == 0:
        raise CRUDError("Tag not found, delete failed")
    db.commit()
    return True


def update_tag(db: Session, id: int, tag: schemas.TagPost):
    db_tag = get_tag(db, id=id)
    if db_tag is None:
        raise CRUDError("Tag not found")
    db_tag.name = tag.name
    db.commit()
    db.refresh(db_tag)
    return db_tag


def get_records(db: Session, skip: int = 0, limit: int = 100):
    """return records sort by updated time"""
    return (
        db.query(models.Record)
        .order_by(models.Record.created.desc())
        .offset(skip)
        .limit(limit)
        .all()
    )


def get_record(db: Session, id: int):
    db_record = db.query(models.Record).filter(models.Record.id == id).first()
    if db_record is None:
        raise CRUDError("Record not found")
    return db_record


def get_records_by_tag(db: Session, tag_id: int, skip: int = 0, limit: int = 100):
    return (
        db.query(models.Record)
        .filter(models.Record.tag_id == tag_id)
        .offset(skip)
        .limit(limit)
        .all()
    )


def create_record(db: Session, record: schemas.RecordPost):
    db_record = models.Record(**record.model_dump())
    if get_tag(db, id=record.tag_id) is None:
        raise CRUDError("Tag id not found")
    if not record.content.strip():
        raise CRUDError("Content can't be empty")
    db.add(db_record)
    db.commit()
    db.refresh(db_record)
    return db_record


def delete_record(db: Session, id: int):
    delete_num = db.query(models.Record)\
        .filter(models.Record.id == id).delete()
    if delete_num == 0:
        raise CRUDError("Record not found, delete failed")
    db.commit()
    return True


def update_record(db: Session, id: int, record: schemas.RecordPost):
    db_record = get_record(db, id=id)
    if db_record is None:
        raise CRUDError("Record not found")
    db_record.desc = record.desc
    db_record.content = record.content
    db_record.tag_id = record.tag_id
    db.commit()
    db.refresh(db_record)
    return db_record
