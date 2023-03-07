# Installation

## API Key

Before you start setting up the GPT3 Telegram Bot, you require two tokens:

1. An account and API key from [OpenAI](https://beta.openai.com/)
    * You can find the API keys in the [OpenAI Dashboard](https://beta.openai.com/account/api-keys)
2. A bot token from [BotFather](https://t.me/botfather)
    * A bot can be create by sending `/newbot` to the BotFather on Telegram

## Clone this repository

```zsh
git clone https://github.com/Tobiaspk/gpt3_telebot.git
cd gpt3_telebot
```

## Setup the bot on Railway

The command `/conv_prompt` allows you to directly jump into a topic. For example, if you have some questions about the terminal, you can simply send the following message to the bot:

```
/conv_prompt terminal
```

The bot will then start a conversation about the terminal, no need to set the context. You can end the conversation by sending the `/conv_end` command.


## Setup the bot locally

After cloning the repository you need:

* Store the API keys in `.keys.yml` or in the environment
* Install the dependencies
* Run the bot

This can be easily done by running the following command and following the instructions:

```zsh
source start
```
