import json
import markovify
import discord
from discord.ext import commands

user = "scba"

TOKEN = "REDACTED" # Insert your bot token here

bot = commands.Bot(command_prefix = "")

@bot.event
async def on_ready():
    global text_model
    with open(f"{user}_model.json", "r", encoding = "utf8") as f:
        text_model = markovify.Text.from_json(json.loads(f.read()))
        f.close()

    print(f"Thou hath summoned {bot.user}.")
    
@bot.event
async def on_message(message):
    if message.author == bot.user:
        return
    
    await message.channel.send(text_model.make_sentence())

bot.run(TOKEN)
