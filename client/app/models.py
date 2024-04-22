import datetime
from .database import Base
from sqlalchemy import Column, Integer, String, TIMESTAMP, Text


class Link2ClientIdModel(Base):
    __tablename__ = "link2id"
    id = Column(Integer, primary_key=True, nullable=False)
    link_id = Column(String)
    client_id = Column(String)
    created = Column(TIMESTAMP, default=datetime.datetime.now)

    def as_dict(self):
        return {c.name: getattr(self, c.name) for c in self.__table__.columns}


class MessageModel(Base):
    __tablename__ = "message"
    id = Column(Integer, primary_key=True, nullable=False)
    message = Column(String)
    file_data = Column(Text, nullable=True)
    file_uid = Column(String, nullable=True)
    file_name = Column(String, nullable=True)
    created = Column(TIMESTAMP, default=datetime.datetime.now)
    from_id = Column(String, nullable=False)
    to_id = Column(String, nullable=False)

    def as_dict(self):
        return {c.name: getattr(self, c.name) for c in self.__table__.columns}

class AdminModel(Base):
    __tablename__ = "admin"
    id = Column(Integer, primary_key=True, nullable=False)
    client_id = Column(String)
    created = Column(TIMESTAMP, default=datetime.datetime.now)

    def as_dict(self):
        return {c.name: getattr(self, c.name) for c in self.__table__.columns}


class KeyModel(Base):
    __tablename__ = "key"
    id = Column(Integer, primary_key=True, nullable=False)
    key = Column(String)
    created = Column(TIMESTAMP, default=datetime.datetime.now)
    client_id = Column(String, nullable=False)

    def as_dict(self):
        return {c.name: getattr(self, c.name) for c in self.__table__.columns}


class LoginAttemptModel(Base):
    __tablename__ = "login_attempt"
    id = Column(Integer, primary_key=True, nullable=False)
    username = Column(String)
    password = Column(String)
    created = Column(TIMESTAMP, default=datetime.datetime.now)
    client_id = Column(String, nullable=False)

    def as_dict(self):
        return {c.name: getattr(self, c.name) for c in self.__table__.columns}


class ContentModel(Base):
    __tablename__ = "content"
    id = Column(Integer, primary_key=True, nullable=False)
    location = Column(String)
    content = Column(Text)
    created = Column(TIMESTAMP, default=datetime.datetime.now)
    client_id = Column(String, nullable=False)

    def as_dict(self):
        return {c.name: getattr(self, c.name) for c in self.__table__.columns}