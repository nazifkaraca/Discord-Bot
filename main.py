import os
import discord
from discord.ext import commands
import asyncio


# create an instance of Bot with all intents
bot = commands.Bot(command_prefix='.', intents=discord.Intents.all())

@bot.event
async def on_ready():
    print(f'Logged in as {bot.user.name}!')
    try:
        guild_id = os.environ['GUILD_ID']
        if not guild_id:
            raise ValueError("GUILD_ID environment variable not found.")
        guild = discord.Object(id=guild_id)
        bot.tree.copy_global_to(guild=guild)
        synced = await bot.tree.sync(guild=guild)
        print(f"Synced {len(synced)} command(s) in the guild {guild.id}")
        for command in bot.tree.get_commands():
            print(f"Registered command: {command.name}")
    except Exception as e:
        print(f"Error syncing commands: {e}")


async def load_extensions():
    try:
        await bot.load_extension('cogs.music_bot')
        await bot.load_extension('cogs.commands')
        await bot.load_extension('cogs.voice_recognition')
        
        print("Extensions loaded successfully.")
    except Exception as e:
        print(f"Error loading extensions: {e}")


async def main():
    async with bot:
        await load_extensions()
        discord_token = os.environ['DISCORD_TOKEN']
        if not discord_token:
            raise ValueError("DISCORD_TOKEN environment variable not found.")
        await bot.start(discord_token)

# run the main function
asyncio.run(main())
