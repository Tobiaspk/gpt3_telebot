from copy import copy 
import datetime
import yaml
import openai
import sqlite3
import telebot

# read the keys from .keys.yml
with open(".keys.yml", "r") as f:
    keys = yaml.safe_load(f)

# Set up the OpenAI API client
openai.api_key = keys["openai"]

# Set the model to use
model_engine = "text-davinci-003"

# Set up the Telegram bot
bot = telebot.TeleBot(keys["telegram"])

# Connect to the database
conn = sqlite3.connect("db/messages.db", check_same_thread=False)
cursor = conn.cursor()

with open("src/prompts.yml", "r") as f:
    prompts = yaml.safe_load(f)

# Create the table if it doesn't exist
cursor.execute("""CREATE TABLE IF NOT EXISTS messages (
                    user_id INTEGER,
                    chat_id INTEGER,
                    username TEXT,
                    prompt TEXT,
                    response TEXT,
                    timestamp DATETIME
                )""")

# add a message handler to telegram
@bot.message_handler(commands=["start"])
def send_welcome(message):
    bot.reply_to(message, "Hello! This is a GPT-3 bot. Send me a prompt and I will try to generate a response using the GPT-3 API.")

# add a handler that shows all available prompts
@bot.message_handler(commands=["help"])
def send_help(message):
    response = "Available commands: /" + ", /".join(prompts.keys())
    bot.reply_to(message, response)

@bot.message_handler(regexp="^/.*")
def send_unknown(message):
    command = message.text.split(" ")[0].replace("/", "")
    if command in prompts.keys():
        print("Running prompt: " + command)
        message.text = prompts[command] + message.text.replace("/" + command + " ", "") + "\n\n"
        run_gpt3(message)
    else:
        response = "The command is not known"
        bot.reply_to(message, response)

@bot.message_handler(func=lambda message: True)
def echo_message(message):
    run_gpt3(message)

def run_gpt3(message):
    # Run the prompt
    prompt = message.text
    completions = openai.Completion.create(
        engine=model_engine,
        prompt=prompt,
        max_tokens=210,
        n=1,
        stop=None,
        temperature=0.5,
    )

    # Get the response
    response = completions.choices[0].text

    # Store the message in the database
    user_id = message.from_user.id
    username = message.from_user.username
    chat_id = message.chat.id
    timestamp = datetime.datetime.now()
    cursor.execute("INSERT INTO messages (user_id, chat_id, username, prompt, response, timestamp) VALUES (?,?,?,?,?,?)", (user_id, chat_id, username, prompt, response, timestamp))
    conn.commit()

    # Send the response to the user
    bot.reply_to(message, response)

bot.polling()
