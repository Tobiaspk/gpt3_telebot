import logging
from datamodel import User, Conversation, Message, Response

def get_user(session, user_id):
    logging.debug("DM FUNCTIONS: Getting user with id %s", user_id)
    user = session.query(User).filter_by(id=user_id).first()
    if not user:
        logging.debug("DM FUNCTIONS: User with id %s not found" % user_id)
    return user

def start_conversation(session, user, prompt, query):
    """
    Starts a conversation for a user.
    param user: User object
    """
    logging.debug("DM FUNCTIONS: Starting conversation for user %s", user.id)
    new_conversation = Conversation()
    new_conversation.prompt = prompt
    new_conversation.query = query
    session.add(new_conversation)
    session.commit()
    user.current_conversation_id = new_conversation.id
    session.commit()
    return new_conversation

def end_conversation(session, user):
    """
    Ends a conversation for a user.
    param user: User object
    """
    logging.debug("DM FUNCTIONS: Ending conversation for user %s", user.id)
    user.current_conversation_id = None
    session.commit()
    return user

def get_conversation(session, user, new_message, message_prefix="Q: ", response_prefix="A: "):
    logging.debug("DM FUNCTIONS: Getting conversation for user %s", user.id)
    conversation_id = user.current_conversation_id
    if conversation_id == None:
        return ""

    conv = session.query(Conversation).filter_by(id=conversation_id).first()
    prompt = conv.prompt
    query = conv.query
    messages = session.query(Message).filter_by(conversation_id=conversation_id).all()
    responses = session.query(Response).filter_by(conversation_id=conversation_id).all()

    # remove last element, which is "/conv_show" typically
    m = [dict(message=message_prefix + message.message, timestamp=message.timestamp) for message in messages]
    r = [dict(message=response_prefix + response.message, timestamp=response.timestamp) for response in responses]

    conversation_list = m + r
    conversation_list.sort(key=lambda x: x['timestamp'])
    conversation = "\n\n".join([i["message"] for i in conversation_list])
    new_prompt = f"{message_prefix}" + new_message + f"\n\n{response_prefix}"
    conversation_all = f"{query}\n\n{conversation}\n\n{new_prompt}"

    conv = dict(
        conversation_all=conversation_all,
        conversation=conversation,
        new_prompt=new_prompt,
        prompt=prompt,
        query=query,
        conversation_start=conv.timestamp,
        number_of_messages=len(messages),
    )

    return conv

def store_message(session, user, chat_id, message):
    """
    Stores a message for a user in the database.
    param message: A string message from the user
    param user: User object
    param chat_id: The chat id of the user
    """
    user_id = user.id
    conversation_id = user.current_conversation_id
    logging.debug("DM FUNCTIONS: Storing message for user %s", user_id)
    new_message = Message(user_id=user_id, chat_id=chat_id, conversation_id=conversation_id, message=message)
    session.add(new_message)
    session.commit()
    return new_message

def store_response(session, message_id, message, user):
    """
    Stores a response for a message from GPT3 in the database that points to the message id.
    param message: A Message object from the user message
    param response: A string response from GPT3
    """
    logging.debug("DM FUNCTIONS: Storing response for message %s", message_id)
    new_response = Response(message_id=message_id, conversation_id=user.current_conversation_id, message=message)
    session.add(new_response)
    session.commit()
    return new_response

def register_user(session, user_id, username):
    # Use redshift in the future for faster lookup of users and conversations
    user = session.query(User).filter_by(id=user_id).first()
    if user is None:
        logging.debug("DM FUNCTIONS: Registering user %s", user_id)
        new_user = User(id=user_id, username=username)
        session.add(new_user)
        session.commit()
        return new_user
    return user
