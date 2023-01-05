import datetime
import yaml
import openai
import telebot
import sqlite3

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

@bot.message_handler(commands=["scientific"])
def send_scientific(message):
    pre = "Rewrite the following sentence, declutter and articulate with professional and scientific expressions: "
    message.text = pre + message.text.replace("/scientific ", "")
    run_gpt3(message)

@bot.message_handler(commands=["professional"])
def send_scientific(message):
    pre = "Rewrite the following sentenceto an overly correct, business appropriate, inclusive statement: "
    message.text = pre + message.text.replace("/scientific ", "")
    run_gpt3(message)

@bot.message_handler(commands=["mail"])
def send_scientific(message):
    pre = "Write a friendly and professional mail out of the following keywords: "
    message.text = pre + message.text.replace("/mail ", "")
    run_gpt3(message)

@bot.message_handler(commands=["mail_homies"])
def send_scientific(message):
    pre = "Write a very personal mail to my homies and make fun of them, use the following keywords: "
    message.text = pre + message.text.replace("/mail ", "")
    run_gpt3(message)

@bot.message_handler(commands=["send_gaudi_message"])
def send_scientific(message):
    pre = "Insult my homies using the following keywords and be really inappropriate but still funny: "
    message.text = pre + message.text.replace("/mail ", "")
    run_gpt3(message)

# filter all unknown commands starting with / using a regular expressions
@bot.message_handler(regexp="^/.*")
def send_unknown(message):
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
