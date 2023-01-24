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

cursor.execute("""CREATE TABLE IF NOT EXISTS conversations (
                    user_id INTEGER,
                    chat_id INTEGER,
                    timestamp DATETIME,
                    conversation BOOLEAN
                )""")

def conversation_active(message):
    convs_open = cursor.execute("SELECT conversation FROM conversations WHERE chat_id = ? ORDER BY timestamp DESC LIMIT 1", (message.chat.id,))
    convs_open = convs_open.fetchall()
    return len(convs_open) > 0 and convs_open[0][0] == 1


def register_conversation_start(message):
    cursor.execute("INSERT INTO conversations (user_id, chat_id, timestamp, conversation) VALUES (?,?,?,?)", (message.from_user.id, message.chat.id, datetime.datetime.now(), 1))

def register_conversation_end(message):
    cursor.execute("INSERT INTO conversations (user_id, chat_id, timestamp, conversation) VALUES (?,?,?,?)", (message.from_user.id, message.chat.id, datetime.datetime.now(), 0))

def get_conversation(message):
    conv_active = conversation_active(message)
    if not conv_active:
        register_conversation_start(message)
        return []
    else:
        convs = cursor.execute("SELECT prompt, response FROM messages WHERE chat_id = ? and timestamp > (SELECT timestamp FROM conversations WHERE chat_id = ? ORDER BY timestamp DESC LIMIT 1) ORDER BY timestamp DESC LIMIT 1", (message.chat.id, message.chat.id))
        convs = convs.fetchall()
        return convs

def init_conversation(message):
    prompt = message.text.replace("/conv", "")
    if prompt == "":
        chat = "This is a conversation with GPT-3. Please keep your answers short."\
            "Be precise, funny and scientific. You can you markdown to structure responses.\n\n"
    else:
        chat = prompt + "\n\n"
    return chat

# add a message handler to telegram
@bot.message_handler(commands=["start"])
def send_welcome(message):
    bot.reply_to(message, "Hello! This is a GPT-3 bot. Send me a prompt and I will try to generate a response using the GPT-3 API.")

@bot.message_handler(commands=["help"])
def send_help(message):
    response = "Available commands: /" + ", /".join(prompts.keys())
    bot.reply_to(message, response)

@bot.message_handler(commands=["conv_start"])
def conversation_start(message):
    register_conversation_start(message)
    print("Conversation started.")
    bot.reply_to(message, "New conversation started.")

@bot.message_handler(commands=["conv_stop"])
def conversation_stop(message):
    register_conversation_end(message)
    print("Conversation ended.")
    bot.reply_to(message, "Conversation ended.")

@bot.message_handler(commands=["conv"])
def conversation(message):
    convs = get_conversation(message)

    prompt = message.text.replace("/conv", "")

    # Initialise the conversation
    if len(convs) > 0:
        chat = convs[0][0] + convs[0][1]
    else:
        if prompt == "":
            chat = "This is a conversation with GPT-3. Please keep your answers short."\
                "Be precise, funny and scientific. You can you markdown to structure responses.\n\n"
        else:
            chat = prompt + "\n\n"
    
    # Add the new message to the conversation
    message.text = f"{chat}\n\nQ: {prompt}\n\nA: "

    # Log outputs
    print("\n\n\n----------", str(datetime.datetime.now()), "----------\n")
    print(message.text)
    text_function = lambda x: "_Continuing conversation..._" + x
    run_gpt3(message, text_function=text_function)

@bot.message_handler(commands=["conv_show"])
def conversation_show(message):
    convs = get_conversation(message)
    if len(convs) == 0:
        bot.reply_to(message, "No conversation active.")
    else:
        bot.reply_to(message, convs[0][0] + convs[0][1])

@bot.message_handler(regexp="^/.*")
def send_command(message):
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
    if conversation_active(message): 
        conversation(message)
    else:
        run_gpt3(message)

def run_gpt3(message, text_function=lambda x: x):
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
    bot.reply_to(message, text_function(response), parse_mode="Markdown")

bot.polling()
