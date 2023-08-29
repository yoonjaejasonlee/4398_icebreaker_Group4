import requests
import discord
import pickle
import os
from discord.ext import commands, tasks
from config import BOT_TOKEN, AUTH_KEY, PIC

from datetime import datetime, timedelta
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

subscription_list = []
events = {}


for i in range(len(data['events'])):
    line = f"({data['events'][i]['event_date']}) {data['events'][i]['event_name']}\n\n"
    text += line

    events[data['events'][i]['event_date']] = f"{data['events'][i]['event_name']}\n{data['events'][i]['event_description']}\n\nhttps://temple.zoom.us/j/99844332204"

    year, month, day = map(int, data['events'][i]['event_date'].split("-"))
    date2 = datetime(year, month, day)
    date_difference = date2 - date1
    if 0 <= date_difference.days <= 7:
        this_week += line

    class_type = data['events'][i]['class_type']
    if class_type == "Lecture" and date_difference.days / 24.0 >= 0 and not next_class:
        line2 = f"{data['events'][i]['event_name']}\n{data['events'][i]['event_description']}\n\nhttps://temple.zoom.us/j/99844332204"
        next_class += line2



if (os.path.isfile("subscriptions")):
    subscription_file = open('subscriptions','rb')
    subscription_list = pickle.load(subscription_file)
    subscription_file.close()


def save_subscriptions():
    subscription_file = open('subscriptions', 'ab')
    pickle.dump(subscription_list,subscription_file)
    subscription_file.close()



@tasks.loop(hours=24)
async def send_reminders():
    tomorrow = date1.date() + timedelta(days=1)
    if str(tomorrow) in events:
        embed = discord.Embed(title="Upcoming Event Reminder", description="CIS 4398", color=0xA71313)
        embed.set_footer(text="CIS 4398 - Icebreaker Group 4", icon_url=PIC)
        embed.description = events[f"{tomorrow}"]
        for ID in subscription_list:
            member = client.get_user(ID)
            await member.send(embed=embed)


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

@client.command(name='subscribe')
async def on_message(message):
    embed = discord.Embed(title="Event Reminders", description="CIS 4398", color=0xA71313)
    embed.set_footer(text="CIS 4398 - Icebreaker Group 4", icon_url=PIC)

    if message.author.id not in subscription_list:
        subscription_list.append(message.author.id)
        save_subscriptions()

        embed.description = f"{message.author.name} has subscribed to reminders"
    else:
        embed.description = f"{message.author.name} is already subscribed to reminders!"

    await message.send(embed=embed)

@client.command(name='unsubscribe')
async def on_message(message):
    embed = discord.Embed(title="Event Reminder Unsubscription", description="CIS 4398", color=0xA71313)
    embed.set_footer(text="CIS 4398 - Icebreaker Group 4", icon_url=PIC)

    if message.author.id not in subscription_list:

        save_subscriptions()

        embed.description = f"{message.author.name} has not subscribed to reminders!"
    else:
        subscription_list.remove(message.author.id)
        embed.description = f"{message.author.name} has unsubscribed from reminders"

    await message.send(embed=embed)

send_reminders.start()

client.run(bot_token)

