import requests
import discord
from discord.ext import commands
from config import BOT_TOKEN, AUTH_KEY, PIC
from datetime import datetime
from datetime import date

today_year = date.today().year
today_month = date.today().month
today_day = date.today().day
date1 = datetime(today_year, today_month, today_day)
intents = discord.Intents.all()

client = commands.Bot(command_prefix='!', intents=intents)

bot_token = BOT_TOKEN

api_url = "https://courses.ianapplebaum.com/api/syllabus/4"
headers = {
    "Authorization": AUTH_KEY,
    "Content-Type": "application/json",
    "Accept": "application/json",
}

response = requests.get(api_url, headers=headers)

data = response.json()

text = ""
this_week = ""
next_class = ""
next_lab = ""

for i in range(len(data['events'])):
    line = f"({data['events'][i]['event_date']}) {data['events'][i]['event_name']}\n\n"
    text += line

    year, month, day = map(int, data['events'][i]['event_date'].split("-"))
    date2 = datetime(year, month, day)
    date_difference = date2 - date1
    if 0 <= date_difference.days <= 7:
        this_week += line

    class_type = data['events'][i]['class_type']
    if class_type == "Lecture" and date_difference.days / 24.0 >= 0 and not next_class:
        line2 = f"{data['events'][i]['event_name']}\n{data['events'][i]['event_description']}\n\nhttps://temple.zoom.us/j/99844332204"


@client.event
async def on_ready():
    print("Logged in as ")
    print(client.user.name)
    print(client.user.id)
    print("===========")

    await client.change_presence(activity=discord.Activity(type=discord.ActivityType.watching, name="For Love"))


@client.command(name='schedule')  # Triggers once it detects !schedule
async def on_message(message):

    embed = discord.Embed(title="Full Schedule - Fall 2023", description="CIS 4398", color=0xA71313)
    embed.set_footer(text="CIS 4398 - Icebreaker Group 4", icon_url= PIC)
    embed.description = f"{text}"

    await message.send(embed=embed)

@client.command(name='thisweek')
async def on_message(message):
    embed = discord.Embed(title="What's coming in the next 7 Days?", description="CIS 4398", color=0xA71313)
    embed.set_footer(text="CIS 4398 - Icebreaker Group 4", icon_url= PIC)
    embed.description = f"{this_week}"

    await message.send(embed=embed)

@client.command(name='nextclass')
async def on_message(message):
    embed = discord.Embed(title="Next Class", description="CIS 4398", color=0xA71313)
    embed.set_footer(text="CIS 4398 - Icebreaker Group 4", icon_url= PIC)
    embed.description = f"{next_class}"

    await message.send(embed=embed)

client.run(bot_token)