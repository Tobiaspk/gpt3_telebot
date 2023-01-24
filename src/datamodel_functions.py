from datamodel import User, Conversation, Message, Response

def check_conversation(session, user_id):
    user = session.query(User).filter_by(id=user_id).first()
    if user.current_conversation_id == -1:
        return False
    else:
        return True

def start_conversation(session, user_id):
    new_conversation = Conversation()
    session.add(new_conversation)
    session.commit()
    user = session.query(User).filter_by(id=user_id).first()
    user.current_conversation_id = new_conversation.id
    session.commit()

def store_message(session, user_id, chat_id, message):
    new_message = Message(user_id=user_id, chat_id=chat_id, conversation_id=user.current_conversation_id, message=message)
    session.add(new_message)
    session.commit()

def store_response(session, generator_id, message_id, message):
    new_response = Response(generator_id=generator_id, message_id=message_id, message=message)
    session.add(new_response)
    session.commit()

def register_user(session, user_id, username):
    # Use redshift in the future for faster lookup of users and conversations
    user = session.query(User).filter_by(id=user_id).first()
    if user is None:
        new_user = User(id=user_id, username=username)
        session.add(new_user)
        session.commit()