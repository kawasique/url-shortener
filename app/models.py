from sqlalchemy import Integer, String, CheckConstraint
from sqlalchemy.orm import (
    MappedAsDataclass,
    DeclarativeBase,
    MappedColumn,
    mapped_column,
)
from pydantic import BaseModel, Field, HttpUrl


class Base(MappedAsDataclass, DeclarativeBase):
    pass


class Entry(Base):
    __tablename__ = "entries"

    id: MappedColumn[int] = mapped_column(
        Integer,
        autoincrement=True,
        primary_key=True,
        init=False,
    )
    url: MappedColumn[str] = mapped_column(String, nullable=False)

    def __repr__(self):
        return f"<Entry(id={self.id}, url={self.url})>"


class EntryIn(BaseModel):
    url: HttpUrl = Field("https://example.com")


class EntryOut(EntryIn):
    key: str = Field("abcdef", description="Уникальный ключ для ссылки")
