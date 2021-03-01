import urllib.request
import xml.etree.ElementTree as ET
import datetime 
import sys

assert(len(sys.argv) == 2)
xml_file = urllib.request.urlopen('http://www.max-manager.de/daten-extern/seezeit/xml/mensa_giessberg/speiseplan.xml')

data = xml_file.read()
xml_file.close()

root = ET.fromstring(data)
assert(root.tag == 'speiseplan')

today = datetime.date.today()

today_root = None
for child in root:
    child_timestamp = child.attrib['timestamp']
    child_timestamp_ = datetime.datetime.fromtimestamp(int(child_timestamp)+6000).date()
    if child_timestamp_ == today:
        today_root = child
        break
    
closed_strings = ["Aufgrund der aktuellen Situation bis auf Weiteres geschlossen.", "geschlossen",
                  "Aufgrund der aktuellen Situation bieten wir bis auf Weiteres nur to-go Speisen & Gerichte auf K5 an. | Unser aktuelles Angebot finden Sie auch unter seezeit.com/coronavirus/hg."]

message = ""
for item in today_root:
    category = item.find('category').text
    title = item.find('title').text
    if title not in closed_strings:
        message = message + "***"+category+"***" + '\n' + title + '\n'
        print(message)
        

if message == "":
    exit()


import discord
 
CHANNEL = "mensa-bot"
client = discord.Client()
TOKEN = sys.argv[1]

@client.event
async def on_ready():
    for channel in client.get_all_channels():
        if channel.name == CHANNEL:
            await channel.send(message)
    await client.close()

try:            
    client.run(TOKEN)
except:
    print("Error")
    exit(0)
    