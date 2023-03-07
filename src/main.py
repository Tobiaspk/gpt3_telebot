import os
from copy import copy 
import datetime
import yaml
import logging
import openai
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

import telebot

import utils
import datamodel as dm
import datamodel_functions as df
import gpt_functions as gf

logging.basicConfig(format='%(asctime)s %(levelname)s %(message)s', level=logging.DEBUG)
DEV = False

# Require keys
keys_required = ["TELEGRAM_API_KEY", "OPENAI_API_KEY"]

if os.path.isfile(".keys.yml"):
    with open(".keys.yml", "r") as f:
        keys = yaml.safe_load(f)
else:
    keys = {
        k: os.environ.get(k) for k in keys_required
    }

for k in keys_required:
    if k not in keys.keys() or keys[k] is None:
        raise ValueError(f"Key '{k}' is missing from the .keys.yml file or the environment variables.")

# Set up the OpenAI API client
openai.api_key = keys["OPENAI_API_KEY"]

# Set the model to use
model_engine = "text-davinci-003"

# Set up the Telegram bot
bot = telebot.TeleBot(keys["TELEGRAM_API_KEY"])

with open("src/prompts.yml", "r") as f:
    prompts = yaml.safe_load(f)

with open("src/prompts_conv.yml", "r") as f:
    prompts_conv = yaml.safe_load(f)

# Connect to the database
if DEV:
    engine = create_engine('sqlite:///db/chat_dev.db')
    dm.Base.metadata.drop_all(engine)
    dm.Base.metadata.create_all(engine)
else:
    engine = create_engine('sqlite:///db/chat.db')
    dm.Base.metadata.create_all(engine)

Session = sessionmaker(bind=engine)
session = Session()

def send_message(message, response, user):
    logging.debug("TELEBOT: Sending message")
    bot.reply_to(message, response)
    mes = df.store_message(session, message=message.text, chat_id=message.chat.id, user=user)
    res = df.store_response(session, message_id=mes.id, message=response, user=user)

def check_user(message):
    user = df.get_user(session, user_id=message.from_user.id)
    if user is None:
        logging.debug("TELEBOT: New user")
        user = df.register_user(session, user_id=message.from_user.id, username=message.from_user.username)
        bot.reply_to(message, "Hello! This is a GPT-3 bot. Start a conversation using /conv_start and end it using /conv_end."
                     " You can also use the commands /help to find more prompts that help you rewrite text.")
    return user

@bot.message_handler(commands=["help"])
def send_help(message):
    logging.debug("TELEBOT: Sending help message")
    response = "Available commands: /" + ", /".join(prompts.keys())
    bot.reply_to(message, response)

@bot.message_handler(commands=["conv_start"])
def conversation_start(message):
    logging.debug("TELEBOT: Starting conversation")
    user = check_user(message)
    conversation = df.start_conversation(session, user=user, prompt="", query="")
    bot.reply_to(message, "New conversation started.")
    if len(message.text.split(" ")) > 1:
        echo_message(message)

@bot.message_handler(commands=["conv_prompt"])
def conversation_start(message):
    logging.debug("TELEBOT: Starting conversation")
    user = check_user(message)

    inputs = message.text.split(" ")
    if len(inputs) != 2:
        bot.reply_to(message, utils.return_list("Please provide exactly one prompt.", prompts_conv.keys()))
        return
    
    prompt = inputs[1]
    if prompt not in prompts_conv.keys():
        bot.reply_to(message, utils.return_list("The prompt is not known.", prompts_conv.keys()))
        return

    query = prompts_conv[prompt]
    conversation = df.start_conversation(session, user=user, prompt=prompt, query=query)
    bot.reply_to(message, f"New conversation about {prompt} started.")

@bot.message_handler(commands=["conv_end"])
def conversation_end(message):
    logging.debug("TELEBOT: Ending conversation")
    user = check_user(message)
    df.end_conversation(session, user=user)
    bot.reply_to(message, "Conversation ended.")

@bot.message_handler(commands=["conv_show"])
def conversation_show(message):
    logging.debug("TELEBOT: Showing conversation")
    user = check_user(message)
    conv = df.get_conversation(session, new_message=message.text, user=user)
    conversation = conv.get("conversation", "")
    if len(conversation) == 0:
        bot.reply_to(message, "No conversation active.")
    else:
        prompt = conv.get("prompt", "")
        if len(prompt) > 0:
            summary = f"Prompt: {prompt}\nQuery: {conv.get('query', '')}\n" \
                      f"No. of messages: {conv.get('number_of_messages', 0)}\n\n" \
                      f"Conversation:\n{conversation}"
            bot.reply_to(message, summary)
        else:
            bot.reply_to(message, conversation)

@bot.message_handler(regexp="^/.*")
def send_command(message):
    logging.debug("TELEBOT: Sending command")
    user = check_user(message)
    if user.current_conversation_id > -1:
        bot.reply_to(message, "Conversation is active. Please /conv_end first before using commands.")
    
    command = message.text.split(" ")[0].replace("/", "")
    if command in prompts.keys():
        prompt = prompts[command] + message.text.replace("/" + command + " ", "") + "\n\n"
        response = gf.run_gpt3(prompt)
        send_message(message, response, user)
    else:
        response = "The command is not known"
        bot.reply_to(message, response)

@bot.message_handler(func=lambda message: True)
def echo_message(message):
    logging.debug("TELEBOT: Handling all other messages")
    user = check_user(message)
    if user.current_conversation_id != -1:
        logging.debug("TELEBOT: Conversation is active")
        conv =df.get_conversation(session, new_message=message.text, user=user)
        entire_message = conv.get("conversation_all", "")
    else:
        logging.debug("TELEBOT: Conversation is not active")
        entire_message = message.text
    response = gf.run_gpt3(prompt=entire_message)
    logging.debug("TELEBOT: Response: " + response)
    send_message(message, response, user)

bot.polling()