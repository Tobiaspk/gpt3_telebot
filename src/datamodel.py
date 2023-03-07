from sqlalchemy import Column, Integer, String, ForeignKey, TIMESTAMP, DateTime
from sqlalchemy.orm import declarative_base
from sqlalchemy.sql import func

Base = declarative_base()

class User(Base):
    __tablename__ = 'users'
    id = Column(Integer, primary_key=True)
    username = Column(String)
    current_conversation_id = Column(Integer, default=-1)
    timestamp = Column(DateTime(timezone=True), server_default=func.now())

class Message(Base):
    __tablename__ = 'messages'
    id = Column(Integer, primary_key=True, autoincrement=True)
    user_id = Column(Integer, ForeignKey('users.id'))
    chat_id = Column(Integer)
    conversation_id = Column(Integer, ForeignKey('conversations.id'))
    timestamp = Column(DateTime(timezone=True), server_default=func.now())
    message = Column(String)

class Response(Base):
    __tablename__ = 'responses'
    id = Column(Integer, primary_key=True, autoincrement=True)
    message_id = Column(Integer, ForeignKey('messages.id'))
    conversation_id = Column(Integer, ForeignKey('conversations.id'))
    timestamp = Column(DateTime(timezone=True), server_default=func.now())
    message = Column(String)

class Conversation(Base):
    __tablename__ = 'conversations'
    id = Column(Integer, primary_key=True, autoincrement=True)
    timestamp = Column(DateTime(timezone=True), server_default=func.now())
    prompt = Column(String)
    query = Column(String)

