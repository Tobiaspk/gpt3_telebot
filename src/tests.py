# import functions from datamodel
import logging
from sqlalchemy.orm import sessionmaker
from sqlalchemy import create_engine
from pprint import pprint
import datamodel_functions as df
import datamodel as dm

logging.basicConfig(format='%(asctime)s %(levelname)s %(message)s', level=logging.DEBUG)

# If the database doesn't exist, create it
logging.debug("Creating database")
engine = create_engine('sqlite:///db/chat_tests.db')

# overwrite the database
dm.Base.metadata.drop_all(engine)
dm.Base.metadata.create_all(engine)
Session = sessionmaker(bind=engine)
session = Session()

mes = session.query(dm.Message).all()
mes[0].conversation_id
m = mes[0]
m.conversation_id = 5

logging.debug("---- proper workflow ----")
user_id = 1
chat_id = 1
logging.debug("registering user")
df.register_user(session, user_id, "user1")
logging.debug("starting conversation")
conv = df.start_conversation(session, user_id)
logging.debug("storing message")
mes = df.store_message(session, user_id, chat_id, "message1")
logging.debug("storing response")
df.store_response(session, mes.id, "response1")
logging.debug("getting conversation")
print(df.get_conversation(session, user_id))
logging.debug("ending conversation")
df.end_conversation(session, user_id)
logging.debug("done")

logging.debug("---- proper workflow ----")
user_id = 2
chat_id = 2
logging.debug("ending conversation")
try:
    df.end_conversation(session, user_id)
except:
    logging.debug("No conversation to end error caught")
logging.debug("getting conversation")
try:
    print(df.get_conversation(session, user_id))
except:
    logging.debug("No conversation to end error caught")
logging.debug("storing response")
df.store_response(session, mes.id, "response1")
logging.debug("storing message")
try:
    mes = df.store_message(session, user_id, chat_id, "message1")
except:
    logging.debug("No conversation to end error caught")
logging.debug("starting conversation")
try:
    conv = df.start_conversation(session, user_id)
except:
    logging.debug("No conversation to end error caught")
logging.debug("registering user")
df.register_user(session, user_id, "user1")
