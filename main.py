import discord
import os
import requests,json
import random

from server import server
from replit import db



client = discord.Client()

sad_words = ['sad','ds','depressed','unhappy','angry','miserable','depressing']

starter_encouragements =['Cheer up!','Hang in there.','Just keep going','Eat well']

if 'responding' not in db.keys():
  db['responding'] = True


def update_encouragements(encoraging_message):
  if "encouragements" in db.keys():
    encouragements = db["encouragements"]
    encouragements.append(encoraging_message)
    db["encouragements"]=encouragements

  else:
    db['encouragements'] = [encoraging_message]


def delete_encoragement(index):
  encouragements = db["encouragements"]
  if len(encouragements) > index:
    del encouragements[index]
    db["encouragements"] = encouragements


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

      options = starter_encouragements

      if 'encouragements' in db.keys():
        options = options + db['encouragements']
      
      if any(word in msg for word in sad_words):
        await message.channel.send(random.choice(options))

    if msg.startswith('$new'):
      encoraging_message = msg.split('$new',1)[1]
      update_encouragements(encoraging_message)
      await message.channel.send("Added new encoraging message.")

    if msg.startswith('$del'):
      encouragements =[]
      if 'encouragements' in db.keys():
        index= int(msg.split('$del',1)[1])
        delete_encoragement(index)
        encouragements=db['encouragements']
      await message.channel.send(encouragements)

    if msg.startswith('$list'):
      encouragements =[]
      if 'encouragements' in db.keys():
        db["encouragements"] = encouragements
      await message.channel.send(encouragements)

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