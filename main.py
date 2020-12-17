import discord
import os
import requests,json
import random

from server import server
from replit import db



client = discord.Client()

sad_words = ['sad','ds','depressed','unhappy','angry','miserable','depressing']

starter_encoragements =['Cheer up!','Hang in there.','Just keep going','Eat well']

if 'responding' not in db.keys():
  db['responding'] = True


def update_encoragements(encoraging_message):
  if "encoragements" in db.keys():
    encoragements = db["encoragements"]
    encoragements.append(encoraging_message)
    db["encoragements"]=encoragements

  else:
    db['encoragements'] = [encoraging_message]


def delete_encoragement(index):
  encoragements = db["encoragements"]
  if len(encoragements) > index:
    del encoragements[index]
    db["encoragements"] = encoragements


def get_quote():
    response = requests.get("https://zenquotes.io/api/random")
    json_data = json.loads(response.text)
    quote = json_data[0]['q'] + '--' + json_data[0]['a']

    return(quote)

@client.event
async def on_ready():
    print('We have logged in as {0.user}'.format(client))


@client.event
async def on_message(message):


    if message.author == client.user:
        return
    msg = message.content

    if msg.startswith('inspire'):
        quote=get_quote()
        await message.channel.send(quote)    

    if db['responding']:

      options = starter_encoragements

      if 'encoragements' in db.keys():
        options+= db['encoragements']
      
      if any(word in msg for word in sad_words):
        await message.channel.send(random.choice(starter_encoragements))

    if msg.startswith('$new'):
      encoraging_message = msg.split('$new',1)[1]
      update_encoragements(encoraging_message)
      await message.channel.send("Added new encoraging message.")

    if msg.startswith('$del'):
      encoragements =[]
      if 'encoragements' in db.keys():
        index= int(msg.split('$del',1)[1])
        delete_encoragement(index)
        encoragements=db['encoragements']
      await message.channel.send(encoragements)

    if msg.startswith('$list'):
      encoragements =[]
      if 'encoragements' in db.keys():
        db["encoragements"] = encoragements
      await message.channel.send(encoragements)

    if msg.startswith('$responding'):
      value = msg.split('$responding ',1)[1]

      if value.lower() =='true':
        db['responding'] = True
        await message.channel.send('Responding is on.')
      else:
        db['responding'] = False
        await message.channel.send('Responding is off.')

server()
client.run(os.getenv('TOKEN'))