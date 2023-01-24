from sqlalchemy import Column, Integer, String, ForeignKey, TIMESTAMP
from sqlalchemy.orm import declarative_base

Base = declarative_base()

class User(Base):
    __tablename__ = 'users'
    id = Column(Integer, primary_key=True)
    username = Column(String)
    current_conversation_id = Column(Integer, default=-1)

class Message(Base):
    __tablename__ = 'messages'
    id = Column(Integer, primary_key=True, autoincrement=True)
    user_id = Column(Integer, ForeignKey('users.id'))
    chat_id = Column(Integer)
    conversation_id = Column(Integer, ForeignKey('conversations.id'))
    timestamp = Column(TIMESTAMP)
    message = Column(String)

class Response(Base):
    __tablename__ = 'responses'
    id = Column(Integer, primary_key=True, autoincrement=True)
    generator_id = Column(Integer)
    message_id = Column(Integer, ForeignKey('messages.id'))
    timestamp = Column(TIMESTAMP)
    message = Column(String)

class Conversation(Base):
    __tablename__ = 'conversations'
    id = Column(Integer, primary_key=True, autoincrement=True)

