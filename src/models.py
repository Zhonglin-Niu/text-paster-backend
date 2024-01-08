from sqlalchemy import Column, ForeignKey, DateTime
from sqlalchemy.orm import DeclarativeBase, relationship, Mapped, mapped_column
from datetime import datetime


class Base(DeclarativeBase):
    pass


class Tag(Base):
    __tablename__ = "tags"

    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    name: Mapped[str] = mapped_column(unique=True, index=True)

    records: Mapped["Record"] = relationship(back_populates="tag")


def now(): return datetime.now()


class Record(Base):
    __tablename__ = "records"

    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    tag_id: Mapped[int] = mapped_column(ForeignKey("tags.id"))
    desc: Mapped[str] = mapped_column(index=True)
    content: Mapped[str]
    created = Column(DateTime, default=now)
    updated = Column(DateTime, default=now, onupdate=now)

    tag: Mapped["Tag"] = relationship(back_populates="records")
