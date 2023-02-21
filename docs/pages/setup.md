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

## Setup the bot

After cloning the repository you need:

* Store the API keys
* Install the dependencies
* Run the bot

This can be easily done by running the following command and following the instructions:

```zsh
source activate_bot
```

This will ask you for the two api keys and install all required dependencies.

## Start the bot

After the setup is complete, you can start the bot by running the following command:

```zsh
start
```