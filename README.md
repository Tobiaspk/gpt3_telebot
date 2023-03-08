# GPT3 Telebot

Make your life easier by letting a bot do the work for you.

Find more docs on [ReadTheDocs](https://gpt3-telebot.readthedocs.io/en/latest/)

## Hosted in 2 minutes

... or 5 minutes if this is your first time using Railway.

1. Simply connect this repo (or a fork) with railway.app. 
2. Set the variables `OPENAI_API_KEY` and `TELEGRAM_API_KEY` 
3. Set as start command `source start`

Done. The bot should be available in a minute.

**Host DB**: In order to persist the database, host a postgresql(!) database in the same project. The script automatically retrieves the connection credentials and will automatically use the railway postgres database.

## Locally

Clone the repo and run the following command.

```
source start
```

Set the `.keys.yml`. Done, you're set.

# Functions

## Topics

The command `/conv_prompt` allows you to directly jump into a topic. For example, if you have some questions about the terminal, you can simply send the following message to the bot:

```
/conv_prompt terminal
```

The bot will then start a conversation about the terminal, no need to set the context. You can end the conversation by sending the `/conv_end` command.

## Conversations

Added a conversation function that remembers the context of previous messages. Start a conversation with /conv_start and begin typing. At the end, use /conv_end. Calling /conv_start during an active conversation will start a new conversation.

Easy example to test conversation:

```
Q: /conv_start
A: New conversation started.
Q: Hi my name is Tobi.
A: Continuing conversation... Nice to meet you, Tobi.
Q: Who am I?
A: Continuing conversation... You are Tobi.
Q: /conv_stop
A: Conversation ended.
Q: Who am I?
A: You are the person asking this question.
```

I like to use this function for answer programming questions and tasks. No need to reintroduce the entire concept everytime. It works quite similar to chatGPT in this regard. However, this is not tested on long chats, in which case higher costs and lower performance may be the consequence.

I hope that sloppy implementation of the conversation function is to everyones liking :) 

## Setup python

Create a virtual environment with all required packages. Depends on an executable `python3`. The setup happens as part of the bot activation.

## Setup keys

You'll need the following keys

* [OpenAI API Key](https://beta.openai.com/account/api-keys)
* BotFather API key

Register your keys using the `scripts/register_keys` script. 

## Start server

This will start polling messages.

```start```

## Get some history

```
bot size
bot show --n 1
```

