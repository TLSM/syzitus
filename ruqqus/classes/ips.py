from flask import *
from sqlalchemy import *
from ruqqus.__main__ import Base


class IP(Base):

    __tablename__ = "ips"

    id = Column(Integer, primary_key=True)
    addr = Column(String(64), index=True)
    reason = Column(String(256), default="")
    banned_by = Column(Integer, ForeignKey("users.id"), default=True)


class Agent(Base):

    __tablename__ = "useragents"

    id = Column(Integer, primary_key=True)
    kwd = Column(String(64), index=True)
    reason = Column(String(256), default="")
    banned_by = Column(Integer, ForeignKey("users.id"))
    mock = Column(String(256), default="")
    status_code = Column(Integer, default=418)
