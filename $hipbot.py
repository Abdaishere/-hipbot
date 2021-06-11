from asyncio import tasks
import requests
from bs4 import BeautifulSoup
import discord
from discord.ext import tasks
import os
import json

Client = discord.Client()

@Client.event
async def on_ready():
    print('working {0.user}'.format(Client))
    check.start()


URL = 'https://codeforces.com/problemset?order=BY_RATING_ASC&tags=1100-'
header = {"User-Agent": 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/90.0.4430.212 Safari/537.36'}
page = requests.get(URL, headers=header)
soup = BeautifulSoup(page.content, 'html.parser')
old_status = soup.find_all("span", {"class": "contest-state-phase"})[0].get_text()

@tasks.loop(minutes=10)
async def check():
    global old_status
    URL = 'https://codeforces.com/problemset?order=BY_RATING_ASC&tags=1100-'
    header = {"User-Agent": 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/90.0.4430.212 Safari/537.36'}
    page = requests.get(URL, headers=header)
    soup = BeautifulSoup(page.content, 'html.parser')
    new_status = soup.find_all("span", {"class": "contest-state-phase"})[0].get_text()
    print(old_status != new_status)
    if old_status != new_status:
        channel = Client.get_channel(848191052555878442)
        await channel.send("check out the new contest available at codefrces" + "https://codeforces.com/")
    old_status = new_status

@Client.event
async def on_message(message):
  if message.content.lower() == "good bot":
    await message.channel.send("Thanks :)")
  if message.content.startswith('$E '):
    response = requests.get('https://aurdyter.sirv.com/Images/albert-einstein-1933340-1920_ver_1.jpg?q=100&text.0.text=%22'+ message.content[3::] +'%22&text.0.position.gravity=east&text.0.position.x=-10%25&text.0.align=left&text.0.size=24&text.0.font.family=Philosopher&text.1.text=%E2%80%95%20Albert%20Einstein&text.1.position.gravity=east&text.1.position.y=10%25&text.1.size=20&text.1.font.family=Yellowtai')
    file = open("image.jpg", "wb")
    file.write(response.content)
    file.close()
    await message.channel.send(file=discord.File(file.name))
  if message.content.lower() == '$send meme' or message.content.lower() == '$send memes':
    obj = json.loads(requests.get('https://meme-api.herokuapp.com/gimme/wholesomememes').content)
    if obj["nsfw"] == True:
        await message.channel.send("it is nsfw")
    else:
        url = requests.get(obj["url"])
        file = open("meme.jpg", "wb")
        file.write(url.content)
        file.close()
        await message.channel.send("here is a meme {0.author.mention}".format(message))
        await message.channel.send(file=discord.File(file.name))


# Client.run(NULL)
        