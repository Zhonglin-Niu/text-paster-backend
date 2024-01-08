from typing import Generic, TypeVar, Optional
from pydantic import BaseModel, ConfigDict
from datetime import datetime


"""""""""""""""""""""
"   BASIC SCHEMAS   "
"""""""""""""""""""""


class TagPost(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    name: str


class TagGet(TagPost):
    id: int


class RecordPost(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    tag_id: int = 1
    desc: str = ""
    content: str


class RecordGet(RecordPost):
    id: int
    created: datetime
    updated: datetime
    tag: TagGet | None = None


""""""""""""""""""""""""
"  API RESPONSE MODEL  "
""""""""""""""""""""""""


M = TypeVar("M", bound=BaseModel)


class GenericResponse(BaseModel, Generic[M]):
    code: int = 200
    msg: str = ""
    data: Optional[M] = None


class BadResponse(GenericResponse):
    code: int = 400
    msg: str = "Bad Request"


class RspTag(GenericResponse[TagGet]):
    ...


class RspTagList(GenericResponse[list[TagGet]]):
    ...


class RspRecord(GenericResponse[RecordGet]):
    ...


class RspRecordList(GenericResponse[list[RecordGet]]):
    ...
