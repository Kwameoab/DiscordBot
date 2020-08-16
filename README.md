﻿# DiscordBot

This is a personal project to create a Discord bot for the server I have with my friends for playing League of Legends. This bot has the basic commands most bots have such as ban, kick, and unban. 

The unique commands this bot has access to is that it is able to web scrape a website [https://na.op.gg/] that provides valuable information for playing League of Legends. The bot is able to take a screenshot of the webpage as well as provide text for the information that was scraped from the website.

## How to locally host

In order to locally host this bot for your own discord server you will need: discord.py [information can be found at https://github.com/Rapptz/discord.py], Beautiful Soup 4, and Selenium with the webdriver

## Alternatives for this project

- Use PyQt5 instead of Selenium for being able to dynamically scrape off information from a website; however, if I use PyQt5 instead of Selenium I would not be able to take a screenshot of the webpage

- Get the information I scraped from the webpage directly from the Riot Games API(creators of League of Legends), but I believe the effort for that is not worth the results

- Fully deploy this bot on a server so it has 24/7 uptime

