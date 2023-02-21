# gpt3_telebot

Find more docs on (ReadTheDocs)[https://gpt3-telebot.readthedocs.io/en/latest/]

# Setup

Hey there! If you're just getting started with this bot, don't worry - we've got you covered! Just follow the steps below and you'll be up and running in no time!

1. Setup Python environment, path and executables with `source activate_bot`
2. Start bot with `start`

'activate_bot' automatically recognises if keys are registered and if not, will prompt to register.

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

