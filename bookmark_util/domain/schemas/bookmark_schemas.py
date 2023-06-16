from pathlib import Path
from pydantic import BaseModel, Field, validator, ValidationError

from bs4 import Tag


class FileObj(BaseModel):
    path_obj: Path = Field(default=None)
    absolute_path: str = Field(default=None)
    type: str = Field(default=None)
    name: str = Field(default=None)
    # resolve_path: str = field(default=None)
    # posix_path: str = field(default=None)
    # uri: str = field(default=None)
    is_symlink: bool = Field(default=False)
    owner: str = Field(default=None)
    parents: list[str] = Field(default=None)
    parent: str = Field(default=None)

    @property
    def path(self) -> str:
        _path: str = str(self.path_obj)

        return _path

    # @property
    # def ext(self) -> Union[str, None]:
    #     if not isinstance(self.)

    @property
    def allowed_types(self) -> list[str]:
        allowed_types = ["file", "dir"]

        return allowed_types

    @validator("type")
    def valid_type(cls, v) -> str:
        if v not in cls.allowed_types:
            raise ValidationError(f"'type' must be one of {cls.allowed_types}")

        return v


class BookmarkFolder(BaseModel):
    name: str = Field(default=None)
    add_date: str = Field(default=None)
    last_modified: str = Field(default=None)
    ## Original bs4.Tag object
    bs4_tag: Tag = Field(default=None)

    class Config:
        arbitrary_types_allowed = True


class Bookmark(BaseModel):
    href: str = Field(default=None)
    add_date: str = Field(default=None)
    icon: str = Field(default=None)
    description: str = Field(default=None)
    url: str = Field(default=None)
    name: str = Field(default=None)
    folder: str = Field(default=None)
    bs4_tag: Tag = Field(default=None)

    class Config:
        arbitrary_types_allowed = True
