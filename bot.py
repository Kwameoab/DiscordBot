import discord
from discord.ext import commands
import random
import asyncio
from datetime import date
from bs4 import BeautifulSoup as soup
import requests
from selenium import webdriver
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
async def champ(ctx, *, champion):
    global request
    request += 1
    champion = champion.split()
    name = champion[0]

    role = ""
    roleString = "For their most popular role"
    if (len(champion) > 1):
        role = champion[1]
        roleString = f"For the {role} role"

    takeScreenshot = False
    if (len(champion) > 2):
        if(champion[2].lower() == "true"):
            takeScreenshot = True

    if os.path.exists(getImageLocation()):
        os.remove(getImageLocation())

    options = webdriver.ChromeOptions()
    options.add_argument('--ignore-certificate-errors')
    options.add_argument('--ignore-ssl-errors')
    options.add_argument('--start-maximized')
    options.add_argument('--start-fullscreen')

    driver = webdriver.Chrome(getDriverLocation(), options=options)
    driver.get(
        f"https://na.op.gg/champion/{name.lower()}/statistics/{role.lower()}")

    res = driver.execute_script("return document.documentElement.outerHTML")

    pageSoup = soup(res, 'html.parser')

    keystone = pageSoup.find("div", {
                             "class": "perk-page__item perk-page__item--keystone perk-page__item--active"}).find("img").get('alt', '')
    embed = discord.Embed(
        title=f"This is the recommended runes for {name.lower().capitalize()}", description=roleString)

    runeString = ""
    runes = pageSoup.find_all(
        "div", {"class": "perk-page__item perk-page__item--active"})
    secondRuneString = ""
    size = 0
    for i in runes:
        for j in i.find_all("img"):
            if size >= 3:
                secondRuneString += (j.get('alt', '')) + "\n"
            else:
                runeString += (j.get('alt', '')) + "\n"
            size += 1

        if size >= 5:
            break

    embed.add_field(name=keystone, value=runeString)
    embed.add_field(name="Secondary", value=secondRuneString)
    await ctx.send(content=None, embed=embed)

    if (takeScreenshot):
        driver.execute_script(
            "window.scrollTo(0, document.body.scrollHeight);")
        driver.get_screenshot_as_file(getImageLocation())
        await ctx.send(file=discord.File(getImageLocation()))
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
    if 'ping' in message.content:
        await message.channel.send('pong')
    await client.process_commands(message)


async def update_stats():
    await client.wait_until_ready()
    global request, messages

    while (not client.is_closed()):
        try:
            with open("stats.txt", "a") as f:
                f.write(
                    f"Date: {date.today()}, Requests: {request}, Messages: {messages}\n")

            request = messages = 0

            await asyncio.sleep(60)

        except Exception as e:
            print(f"Something went wrong. Error: {e}")
            await asyncio.sleep(60)

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
