import discord
from discord.ext import commands
import gpt_2_simple as gpt2
import tensorflow as tf
from random import choice

user = "scba"

TOKEN = "REDACTED" # Insert your bot token here

bot = commands.Bot(command_prefix = "")

@bot.event
async def on_ready():
    global sess
    sess = gpt2.start_tf_sess()
    gpt2.load_gpt2(sess, reuse = tf.compat.v1.AUTO_REUSE)

    print(f"Thou hath summoned {bot.user}.")
    
@bot.event
async def on_message(message):
    global sess
    if message.author == bot.user:
        return

    m = gpt2.generate(sess,
                      prefix = "<|startoftext|>",
                      truncate = "<|endoftext|>",
                      include_prefix = False,
                      return_as_list = True)

    new_m = m[0].split("<|endoftext|>") # sometimes truncate fails
    
    await message.channel.send(new_m[0])

bot.run(TOKEN)
