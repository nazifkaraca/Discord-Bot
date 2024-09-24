import discord
from discord.ext import commands
from discord import app_commands
from utils import get_quote
from database import update_encouragements, delete_encouragement

class Commands(commands.Cog):
    def __init__(self, client):
        self.client = client

    @commands.Cog.listener()
    async def on_message(self, message):
        if message.author == self.client.user:
            return

        msg = message.content

        if msg.startswith('.inspire'):
            quote = get_quote()
            await message.channel.send(quote)

        if db["responding"]:
            options = starter_encouragements
            if "encouragements" in db.keys():
                options = options + list(db["encouragements"])

            if any(word in msg for word in sad_words):
                await message.channel.send(random.choice(options))

        if msg.startswith(".new"):
            encouraging_message = msg.split("$new ", 1)[1]
            update_encouragements(encouraging_message)
            await message.channel.send("New encouraging message added.")

        if msg.startswith(".del"):
            if "encouragements" in db.keys():
                encouragements = list(db["encouragements"])
                index = int(msg.split("$del", 1)[1])
                delete_encouragement(index)
                encouragements = list(db["encouragements"])
                await message.channel.send(encouragements)
            else:
                await message.channel.send([])

        if msg.startswith(".inspirelist"):
            encouragements = []
            if "encouragements" in db.keys():
                encouragements = db["encouragements"]
            await message.channel.send(encouragements)

        if msg.startswith(".responding"):
            value = msg.split("$responding ", 1)[1]

            if value.lower() == "true":
                db["responding"] = True
                await message.channel.send("Responding is on.")
            else:
                db["responding"] = False
                await message.channel.send("Responding is off.")

        await self.client.process_commands(message)

async def setup(client):
    await client.add_cog(Commands(client))
