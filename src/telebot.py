# import functions from datamodel
from sqlalchemy.orm import sessionmaker
from sqlalchemy import create_engine
from pprint import pprint
import datamodel_functions as df
import datamodel as dm

# If the database doesn't exist, create it
engine = create_engine('sqlite:///db/chat.db')
dm.Base.metadata.create_all(engine)



Session = sessionmaker(bind=engine)
session = Session()

pprint([i.__dict__ for i in session.query(dm.User).all()])

