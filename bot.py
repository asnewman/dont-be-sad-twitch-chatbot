import os
import requests
from twitchio.ext import commands

channels = os.getenv("INITIAL_CHANNELS").split(',')

bot = commands.Bot(
    irc_token=os.getenv("IRC_TOKEN"),
    client_id=os.getenv("CLIENT_ID"),
    nick=os.getenv("NICK"),
    prefix=os.getenv("PREFIX"),
    initial_channels=channels
)

@bot.event
async def event_ready():
    ws = bot._ws  # this is only needed to send messages within event_ready
    
    for channel in channels:
        await ws.send_privmsg(channel, "I'm alive")

@bot.event
async def event_message(ctx):
    await bot.handle_commands(ctx)

    print("New message came in " + ctx.content)

    if (":(" in ctx.content):
        print("Sad face detected")
        await ctx.channel.send(create_chat_message(ctx.author.name))
    elif (ctx.content == "!sleeping"):
        await ctx.channel.send(f"Good night {ctx.author.name}")
    elif (ctx.content == "!advice"):
        await ctx.channel.send(get_advice())
    elif (ctx.content == "!kanye"):
        await ctx.channel.send(get_kanye())
    elif (ctx.content == "!insult"):
        await ctx.channel.send(get_insult())
    
def get_advice():
    response = requests.get("https://api.adviceslip.com/advice")

    return response.json()["slip"]["advice"]

def get_kanye():
    response = requests.get("https://api.kanye.rest/")

    quote = response.json()["quote"]

    return f"Kanye once said '{quote}'"

def create_chat_message(author_name):
    return f"Be happier {author_name} :) Here's a joke to make you feel better: {get_dadjoke()}"

def get_dadjoke():
    response = requests.get("https://icanhazdadjoke.com", headers={
        "Accept": "text/plain"
    })

    return response.text

def get_insult():
    response = requests.get("https://evilinsult.com/generate_insult.php?lang=en&type=json")

    return response.json()["insult"]


def main():
    # Runs when you run the program
    bot.run()
    # print(get_insult())



if __name__ == "__main__":
    main()
