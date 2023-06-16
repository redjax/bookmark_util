from typing import Optional

import sqlalchemy as sa
from sqlalchemy.orm import Mapped, mapped_column, relationship

from core.db import Base


class Bookmark(Base):
    __tablename__ = "bookmark"
    
    id: Mapped[int] = mapped_column(primary_key=True)
    href: Mapped[Optional[str]] = mapped_column(nullable=True)
    add_date: Mapped[Optional[str]] = mapped_column(nullable=True)
    icon: Mapped[Optional[str]] = mapped_column(nullable=True)
    description: Mapped[Optional[str]] = mapped_column(nullable=True)
    icon: Mapped[Optional[str]] = mapped_column(nullable=True)
    url
    name
    folder
 'icon': ModelField(name='icon', type=Optional[str], required=False, default=None),
 'description': ModelField(name='description', type=Optional[str], required=False, default=None),
 'url': ModelField(name='url', type=Optional[str], required=False, default=None),
 'name': ModelField(name='name', type=Optional[str], required=False, default=None),
 'folder': ModelField(name='folder', type=Optional[str], required=False, default=None),
 'bs4_tag