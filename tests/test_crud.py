from src.database import SessionLocal, engine
from src import crud, models
from src import schemas
import os


def get_db():
    print()
    if os.path.exists("storage.db"):
        os.remove("storage.db")
        print("removing  storage.db")
    models.Base.metadata.create_all(bind=engine)

    db = SessionLocal()

    if not crud.get_tag_by_name(db, name=""):
        crud.create_tag(db, schemas.TagPost(name=""))

    try:
        return db
    finally:
        print("close db")
        db.close()


DB = get_db()


def test_create_tag():
    tags = [
        "test_tag",
        "ssh",
        "python",
        "docker",
        "notes"
    ]
    for tag in tags:
        crud.create_tag(DB, schemas.TagPost(name=tag))


def test_create_record():
    ssh_id = crud.get_tag_by_name(DB, name="ssh").id

    ssh_content = [
        "ssh root@210.43.89.21",
        "ssh root@40.11.21.14",
        "ssh root@220.14.13.47",
        "ssh root@160.4.35.16",
    ]

    for content in ssh_content:
        crud.create_record(DB, schemas.RecordPost(
            content=content, tag_id=ssh_id))

    notes_id = crud.get_tag_by_name(DB, name="notes").id

    notes_content = [
        "lorem ipsum dolor sit amet",
        "consectetur adipiscing elit",
        "sed do eiusmod tempor incididunt ut labore et dolore magna aliqua",
        "ut enim ad minim veniam",
        "quis nostrud exercitation ullamco laboris nisi ut aliquip ex ea commodo consequat",
        "duis aute irure dolor in reprehenderit in voluptate velit esse cillum dolore eu fugiat nulla pariatur",
        "excepteur sint occaecat cupidatat non proident",
        "sunt in culpa qui officia deserunt mollit anim id est laborum",
    ]

    import random
    for content in notes_content:
        crud.create_record(DB, schemas.RecordPost(
            content=content*random.randint(1, 10), tag_id=notes_id))
