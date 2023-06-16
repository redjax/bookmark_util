from __future__ import annotations

from pathlib import Path
from typing import Any, Union

from core.config import app_settings, logging_settings
from utils.logger import get_logger

log = get_logger(__name__, level=logging_settings.LOG_LEVEL)

from bs4 import BeautifulSoup, ResultSet, Tag
from core.db import Base, create_base_metadata, get_engine, get_session
from utils.validators import valid_dir

engine = get_engine(connection="db/demo.sqlite", echo=True)
create_base_metadata(base_obj=Base, engine=engine)
SessionLocal = get_session(engine=engine)

bookmarks_dir: str = "bookmarks"
bookmarks_file: str = "bookmarks_6_13_23.html"
bookmarks_file_path: str = f"{bookmarks_dir}/{bookmarks_file}"


from dataclasses import dataclass, field

@dataclass
class FileObj:
    path_obj: Path = field(default=None)
    absolute_path: str = field(default=None)
    type: str = field(default=None)
    name: str = field(default=None)
    # resolve_path: str = field(default=None)
    # posix_path: str = field(default=None)
    # uri: str = field(default=None)
    is_symlink: bool = field(default=False)
    owner: str = field(default=None)
    parents: list[str] = field(default=None)
    parent: str = field(default=None)

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

    def __post_init__(self):
        if self.type not in self.allowed_types:
            raise ValueError(f"File object 'type' must be one of {self.allowed_types}")


def get_files(root_dir: Union[str, Path] = None) -> dict[str, list[FileObj]]:
    root_dir = valid_dir(root_dir)

    files: list[FileObj] = []
    dirs: list[FileObj] = []

    log.debug(f"root_dir: {root_dir}")

    for item in root_dir.glob("**/*"):
        if item.is_file():
            item_type = "file"

        elif item.is_dir():
            item_type = "dir"

        # files.append(item)

        item_dict: dict[str, Union[str, Any]] = {
            "path_obj": item,
            "absolute_path": item.absolute(),
            "type": item_type,
            "name": item.name,
            # "resolve_path": item.resolve(),
            # "posix_path": item.as_posix(),
            # "uri": item.as_uri(),
            "is_symlink": item.is_symlink(),
            "owner": item.owner(),
            "parents": item.parents,
            "parent": item.parent,
        }

        append_item: FileObj = FileObj(**item_dict)
        # log.debug(f"Test Dir class object: {append_item}")

        if append_item.type == "file":
            files.append(append_item)
        elif append_item.type == "dir":
            files.append(append_item)

    return_obj: dict[str, Union[str, Path]] = {"dirs": dirs, "files": files}

    return return_obj


def read_bookmarks(file: Union[str, Path, FileObj] = None):
    if not file:
        raise ValueError("Missing bookmarks file")

    if (
        not isinstance(file, Path)
        and not isinstance(file, str)
        and not isinstance(file, FileObj)
    ):
        raise ValueError("File must be str, FileObj, or Path")

    if not isinstance(file, Path):
        if isinstance(file, str):
            file: Path = Path(file)

        else:
            file = Path(file.absolute_path)

    if not file.exists():
        raise FileNotFoundError(f"Could not find file {file}")

    try:
        with open(file, "r+") as f:
            contents = f.read()

        return contents
    except Exception as exc:
        raise Exception(f"Unhandled exception opening file '{file}'. Details: {exc}")


if __name__ == "__main__":
    log.info("Starting app")

    log.debug(f"App settings: {app_settings}")

    log.debug(f"Bookmarks file: {bookmarks_file_path}")

    # log.debug(f"Bookmark files: {get_files('core')}")

    bookmark_files = get_files(bookmarks_dir)

    log.debug(f"Bookmark files: {bookmark_files}")

    _sample: Path = bookmark_files["files"][0]

    _contents = read_bookmarks(file=_sample)

    # log.debug(f"Bookmark file contents: {_contents}")

    soup = BeautifulSoup(_contents, "lxml")

    _dt: ResultSet = soup.find_all("dt")

    html_folders: list[Tag] = []
    html_bookmarks: list[Tag] = []

    for line in _dt:
        # log.debug(f"line: {line}")

        item: Tag = line.find_next()

        if item.name == "h3":
            folder_name = item.text
            # log.debug(f"Folder: {folder_name}")

            html_folders.append(item)

            continue

        else:
            # log.debug(
            #     f"URL: {item.get('href')}, Website Name: {item.text}, Add Date: {item.get('add_date')}, Folder name: {folder_name}"
            # )
            html_bookmarks.append(item)

    log.debug(
        f"Found [{len(html_folders)}] bookmark folders and [{len(html_bookmarks)}] bookmarks"
    )

    _test = html_bookmarks[0]

    log.debug(f"Test ({type(_test)}): {_test}")
    log.debug(f"Test dict: {_test.__dict__}")

    log.debug(f"Test name: {_test.name}")
    log.debug(f"Test text: {_test.text}")
