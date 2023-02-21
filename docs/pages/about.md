# GPT3 Telebot

Make your life easier by letting a bot do the work for you.

I often know what I want to say, but it is difficult to find the right words. This is where the GPT3 Telebot comes in. It can help you write emails, letters, but most importantly rewrite your text to make it sound better. Like this one.

## Easy to use

Once the bot is setup, you can start it by running the following command:

```zsh
start
```

## Make your text sound better

Then you can write some prompts, decide **how** the text should be rewritten and simply send them to the bot from any device and from anywhere. The bot will then reply with a rewritten version of your text. 

For example, if you write the following prompt:

```
/professional This bot is really cool in making your sentences sound better.
```

The bot will reply with a rewritten version of the text:

```
This bot is an amazing tool for improving the quality of your sentences.
```

*This mode does not remember previous messages. Check details on conversations below.*

## Add more prompts

You can add more prompts by simply adding them to the `src/prompts.yml` file. The bot will then use these prompts to rewrite your text - no restart required.

## Make Conversations

You can also make conversations with the bot. Simply send a message using the `/conv_start` which will enter a chatGPT like conversation. The bot will use previous messages to generate the next message in a conversation. A conversation can be ended by sending the `/conv_end` command.

Try this feature by sending the following message to the bot:

```
/conv_start
```

Introduce yourself:

```
Hi, I'm Tobias
```

And then just ask the name again:

```
What's my name?
```

Note that prompts and conversations are mutually exclusive. You cannot use both at the same time.

## Saving messages

All messages are stored in an sqlite database.

## Pitfalls(!)

The bot is still in development and there are some pitfalls to be aware of:

* There is no limit of how many messages will be used for a conversation. I have not tested the conversation function on longer conversations. Message histories that are too long may cause problems with the API and increase the costs
* **Costs(!)**: Now that I have your attention - costs have never been a problem to me. Even through extensive use my monthly bill has never exceeded 0.50$. Still, use at your own risk. 