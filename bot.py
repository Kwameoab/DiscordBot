import discord
from discord.ext import commands
import random
import time 
import asyncio
from datetime import date

request = messages = 0

client = commands.Bot(command_prefix='>')
client.remove_command('help')

@client.event
async def on_ready():
    await client.change_presence(status=discord.Status.online, activity=discord.Game("Providing Great Service"))
    print("This client is ready.")

@client.command()
async def ping(ctx):
    global request
    request += 1
    await ctx.send(f'Pong! It took {round(client.latency * 1000)}ms to deliver this message')

@client.command(aliases=["rand#","random#","#rand"])
async def randNum(ctx,num="10"):
    if (not num.isdigit()):
        await ctx.send("Please input in a postive number as you response")
        return
    global request
    request += 1
    num = int(num)
    numRange = range(1,num + 1)
    await ctx.send(f"Your random number from 1 to {num} is {random.choice(numRange)}")

@client.command()
async def stats(ctx):
    global request
    request += 1
    for line in reversed(list(open("stats.txt"))):
        break
    await ctx.send(f"That stats from the last time I updated is:\n{line}")

@client.command()
async def help(ctx):
    embed = discord.Embed(title="This help section is to help everyone use this bot", description="Theses are commands that this bot has access to")
    embed.add_field(name="stats", value="Prints the most recent stats from bot")
    embed.add_field(name="randNum", value="Give the bot a number and it will return a random number from 1 to that number")
    embed.add_field(name="ping", value="Tells the user how long it took the bot to response to their command")
    await ctx.send(content=None, embed=embed)



@client.event
async def on_message(message):
    global messages
    messages += 1
    if message.content == 'ping':
        await message.channel.send('pong')
    await client.process_commands(message)

async def update_stats():
    await client.wait_until_ready()
    global request, messages

    while (not client.is_closed()):
        try:
            with open("stats.txt","a") as f:
                f.write(f"Date: {date.today()}, Requests: {request}, Messages: {messages}\n")
            
            request = messages = 0

            await asyncio.sleep(5)
        
        except Exception as e:
            print(f"Something went wrong. Error: {e}")
            await asyncio.sleep(5)

client.loop.create_task(update_stats())

def getToken():
    with open("token.txt","r") as f:
        lines = f.readlines()
        return lines[0]

client.run(getToken())