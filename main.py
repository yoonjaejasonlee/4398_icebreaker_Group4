import requests
import discord
from discord.ext import commands

from config import BOT_TOKEN, AUTH_KEY, PIC

intents = discord.Intents.all()

client = commands.Bot(command_prefix='!', intents=intents)

bot_token = BOT_TOKEN

api_url = "https://courses.ianapplebaum.com/api/syllabus/1"
headers = {
    "Authorization": AUTH_KEY,
    "Content-Type": "application/json",
    "Accept": "application/json",
}

response = requests.get(api_url, headers=headers)

data = response.json()

text = ""

for i in range(len(data['events'])):
    line = f"({data['events'][i]['event_date']}) {data['events'][i]['event_name']}\n\n"
    text += line

@client.event
async def on_ready():
    print("Logged in as ")
    print(client.user.name)
    print(client.user.id)
    print("===========")

    await client.change_presence(activity=discord.Activity(type=discord.ActivityType.watching, name="For Love"))


@client.command(name='schedule')  # Triggers once it detects !schedule
async def on_message(message):

    embed = discord.Embed(title="Full Schedule", description="CIS 4398 - Fall 2023", color=0xA71313)
    embed.set_footer(text="CIS 4398 - Icebreaker Group 4", icon_url= PIC)
    embed.description = f"**{text}**"

    await message.send(embed=embed)


client.run(bot_token)