import discord
from discord.ext import commands
import random
import asyncio
import datetime
from bs4 import BeautifulSoup as soup
import requests
from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
import os


request = messages = 0

client = commands.Bot(command_prefix='!')
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


@client.command(aliases=["rand#", "random#", "#rand"])
async def randNum(ctx, num="10"):
    if (not num.isdigit()):
        await ctx.send("Please input in a postive number as you response")
        return
    global request
    request += 1
    num = int(num)
    numRange = range(1, num + 1)
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
    global request
    request += 1
    embed = discord.Embed(title="This help section is to help everyone use this bot",
                          description="Theses are commands that this bot has access to")
    embed.add_field(
        name="stats", value="Prints the most recent stats from bot")
    embed.add_field(
        name="randNum", value="Give the bot a number and it will return a random number from 1 to that number")
    embed.add_field(
        name="ping", value="Tells the user how long it took the bot to response to their command")
    embed.add_field(
        name="champ", value="Input in a champion's name[required], what lane[optional], and true if you want" +
        " a screenshot[optional] to get the recommended runes for that champion scraped from OP.GG")
    embed.add_field(
        name="ban", value="Ban a user from the server, optional to give a reason")
    embed.add_field(
        name="kick", value="Kick a user from the server, optional to give a reason")
    embed.add_field(
        name="unban", value="Unban a user from the server ban list")
    embed.add_field(
        name="role", value="Returns a random role the user can play")
    await ctx.send(content=None, embed=embed)


@client.command()
async def op(ctx, *, input):
    global request
    request += 1
    input = input.split()
    name = input[0]
    if name.lower() == 'wukong':
        name = 'monkeyking'     # Do know why but in op.gg wukong is moneky king

    role = ""
    if len(input) > 1:
        role = input[1]

    type = ""
    if len(input) > 2:
        type = input[2]

    if os.path.exists(imageLoc := getImageLocation()):
        os.remove(imageLoc)

    options = webdriver.ChromeOptions()
    options.add_argument('--ignore-certificate-errors')
    options.add_argument('--ignore-ssl-errors')
    options.add_argument('--start-maximized')
    options.add_argument('--start-fullscreen')

    driver = webdriver.Chrome(ChromeDriverManager().install(), options=options)
    link = ""
    if role == "":
        link = f"https://na.op.gg/champions/{name.lower()}/"
        driver.get(link)
        driver.execute_script(
            "window.scrollTo(0, document.body.scrollHeight);")
    elif type == "":
        link = f"https://na.op.gg/champions/{name.lower()}/{role.lower()}/"
        driver.get(link)
        driver.execute_script(
            "window.scrollTo(0, document.body.scrollHeight);")
    else:
        link = f"https://na.op.gg/champions/{name.lower()}/{role.lower()}/{type.lower()}"
        driver.get(link)
        driver.execute_script(
            "window.scrollTo(0, 740);")

    driver.get_screenshot_as_file(imageLoc)
    await ctx.send(file=discord.File(imageLoc))
    await ctx.send(content=None, embed=discord.Embed(description=f"[link]({link})"))
    driver.close()


@client.command(aliases=["u"])
async def ugg(ctx, *, input):
    global request
    request += 1
    input = input.split()
    name = input[0]

    role = ""
    if len(input) > 1:
        role = input[1]
        if role.lower() == 'mid':
            role = 'middle'

    type = ""
    if len(input) > 2:
        type = input[2]

    rank = ""
    if len(input) > 3:
        rank = input[3]

    if os.path.exists(imageLoc := getImageLocation()):
        os.remove(imageLoc)

    options = webdriver.ChromeOptions()
    options.add_argument('--ignore-certificate-errors')
    options.add_argument('--ignore-ssl-errors')
    options.add_argument('--start-maximized')
    options.add_argument('--start-fullscreen')

    driver = webdriver.Chrome(ChromeDriverManager().install(), options=options)
    link = ""
    if role == "":
        link = f"https://u.gg/lol/champions/{name.lower()}/"
        driver.get(link)
        driver.execute_script(
            "window.scrollTo(0, 300);")
    elif type == "":
        link = f"https://u.gg/lol/champions/{name.lower()}/build?role={role.lower()}"
        driver.get(link)
        driver.execute_script(
            "window.scrollTo(0, 300);")
    elif rank == "":
        link = f"https://u.gg/lol/champions/{name.lower()}/{type.lower()}?role={role.lower()}"
        driver.get(link)
        driver.execute_script(
            "window.scrollTo(0, 300);")
    else:
        link = f"https://u.gg/lol/champions/{name.lower()}/{type.lower()}?role={role.lower()}&rank={rank.lower()}"
        driver.get(link)
        driver.execute_script(
            "window.scrollTo(0, 300);")

    driver.get_screenshot_as_file(imageLoc)
    await ctx.send(file=discord.File(imageLoc))
    await ctx.send(content=None, embed=discord.Embed(description=f"[link]({link})"))
    driver.close()


@client.command()
async def kick(ctx, member: discord.Member, *, reason=None):
    global request
    request += 1
    await member.kick(reason=reason)
    await ctx.send(f"Kicked {member.mention}")


@client.command()
async def ban(ctx, member: discord.Member, *, reason=None):
    global request
    request += 1
    await member.ban(reason=reason)
    await ctx.send(f"Banned {member.mention}")


@client.command()
async def unban(ctx, *, member):
    global request
    request += 1
    bannedUsers = await ctx.guild.bans()
    memberName, memberDiscriminator = member.split("#")

    for bans in bannedUsers:
        user = bans.user

        if(user.name, user.discriminator) == (memberName, memberDiscriminator):
            await ctx.guild.unban(user)
            await ctx.send(f"Unbanned {user.mention}")
            return


@client.command()
async def role(ctx):
    global request
    request += 1
    randRole = ("Top", "Jungle", "Mid", "Bot", "Support")
    await ctx.send(f"You should go {random.choice(randRole)}")


@client.event
async def on_message(message):
    global messages
    messages += 1
    await client.process_commands(message)


async def update_stats():
    await client.wait_until_ready()
    global request, messages

    while not client.is_closed():
        try:
            with open("stats.txt", "a") as f:
                f.write(
                    f"Date: {datetime.datetime.now()}, Requests: {request}, Messages: {messages}\n")

            request = messages = 0

            await asyncio.sleep(60 * 5)

        except Exception as e:
            print(f"Something went wrong. Error: {e}")
            await asyncio.sleep(60 * 5)

client.loop.create_task(update_stats())


def getDriverLocation():
    with open("driverLoc.txt", "r") as f:
        lines = f.readlines()
        return lines[0]


def getImageLocation():
    with open("imageLoc.txt", "r") as f:
        lines = f.readlines()
        return lines[0]


def getToken():
    with open("token.txt", "r") as f:
        lines = f.readlines()
        return lines[0]


client.run(getToken())
