import discord
from discord.ext import commands
from discord import app_commands
import yt_dlp

class MusicBot(commands.Cog):
    def __init__(self, client):
        self.client = client
        self.queue = []
        self.currently_playing = None

    
    # plays the audio when its called
    async def play_next(self, interaction: discord.Interaction):
        if self.queue:
            # works as FIFO
            # first requested music will be played first
            url, title = self.queue.pop(0)
            self.currently_playing = title
            # source request of the audio
            source = await discord.FFmpegOpusAudio.from_probe(url)
            # it plays requested audio and schedules the next audio
            # in the queue
            interaction.guild.voice_client.play(source, after=lambda _: self.client.loop.create_task(self.play_next(interaction)))
            # if request satisfied, acknowledge the requester
            await interaction.followup.send(f'**{title}** oynatılıyor.')
            # if there is no playing audio, set currently playing to none
            # and inform the requester that queue is empty
        elif not interaction.guild.voice_client.is_playing():
            self.currently_playing = None
            await interaction.followup.send('Listede şarkı yok.')

    
    # displays list of audios 
    async def display_queue(self, interaction: discord.Interaction):
        # if there is a audio in the queue
        if self.queue:
            # get both index and title of the audio for every song in the queue (enumerate)
            # assign each of them to index + 1 (more user friendly) and to title
            # join and show them as eg. 1. Rammstein - Mein Hertz Brennt (Official)
            queue_list = "\n".join([f"{index+1}. {title}" for index, (_, title) in enumerate(self.queue)])
            await interaction.followup.send(f'**Şarkı Listesi:**\n{queue_list}')
        else:
            # if the list empty, acknowledge the requester
            await interaction.followup.send('Şarkı listesi boş.')


    # search requested audio in the youtube        
    async def fetch_song(self, search: str):
        # setting options for audio
        yt_dlp_opts = {
            'format': 'bestaudio',
            # do not inform me about searching stuff
            'quiet': True,
            'no_warnings': True,
            # automatically search in youtube if url not provided
            'default_search': 'auto',
            'source_address': '0.0.0.0',
        }
        # create a youtubedl object with options provided
        # with statement handles closing downloader after block runs
        with yt_dlp.YoutubeDL(yt_dlp_opts) as ydl:
            # dont you dare to download and bring searched audio information
            info = ydl.extract_info(f"ytsearch:{search}", download=False)
            # if there is 'entries' in the information
            if 'entries' in info:
                # bring me the first result
                info = info['entries'][0]
            url = info['url']
            title = info['title']
            # return url and title
            return url, title


    # plays an audio after user writes "oynat" in discord chat
    # app_commands handles slash comments (after writing "/", all commands
    # available will be listed for our bot)
    @app_commands.command(name="oynat", description="istenilen şarkıyı oynatır.")
    async def oynat(self, interaction: discord.Interaction, search: str):
        # acknowledge the interaction to avoid timing out
        # discord gives 3 seconds, we need to entend that time a few seconds more
        await interaction.response.defer()  
        # checks whether the requester in the voice channel or not
        voice_channel = interaction.user.voice.channel if interaction.user.voice else None
        if not voice_channel:
            # if not, warn them to hop into one
            return await interaction.followup.send("Bir ses kanalında değilsin.", ephemeral=True)
        # checks whether the bot is connected to a voice channel
        if not interaction.guild.voice_client:
            await voice_channel.connect()
        # fetch the audio and append queue
        url, title = await self.fetch_song(search)
        self.queue.append((url, title))
        # if there is no audio playing, call play_next func
        if not interaction.guild.voice_client.is_playing():
            await self.play_next(interaction)
        # prevent first song to be presented in the list
        if len(self.queue) > 0:
            await interaction.followup.send(f'**{title}** oynatma listesine eklendi.')
            await self.display_queue(interaction)


    # skips audio
    @app_commands.command(name="geç", description="şarkıyı geçer.")
    async def geç(self, interaction: discord.Interaction):
        await interaction.response.defer()
        # checks if the bot both connected to server and playing an audio
        if interaction.guild.voice_client and interaction.guild.voice_client.is_playing():
            # if true, stop the audio and inform the requester
            interaction.guild.voice_client.stop()
            await interaction.followup.send("Şarkı geçildi.")
        else:
            # if false, inform the requester that there are no audio in the queue
            await interaction.followup.send("Oynatılan şarkı yok.")


    # list the queue
    @app_commands.command(name="liste", description="şarkı listesini gösterir.")
    async def liste(self, interaction: discord.Interaction):
        await interaction.response.defer()
        await self.display_queue(interaction)


    # call bot
    @app_commands.command(name="gel", description="Kanala katılır.")
    async def join(self, interaction: discord.Interaction):
        await interaction.response.defer()
        # get the channel of the requester
        channel = interaction.user.voice.channel
        if channel:
            # connect to the channel
            await channel.connect()
            await interaction.followup.send(f'{channel} kanalına katıldım!')
        else:
            # inform the requester to get into a channel
            await interaction.followup.send('Bir ses kanalında değilsin!')

    
    # shoo away the bot
    @app_commands.command(name='git', description='Botu kovalar.')
    async def leave(self, interaction: discord.Interaction):
        await interaction.response.defer()
        # get the bot's voice client in the guild
        voice = discord.utils.get(self.client.voice_clients, guild=interaction.guild)  
        if voice and voice.is_connected():
            # disconnect the bot from the voice channel
            await voice.disconnect()
            # send a follow-up message
            await interaction.followup.send('Bot kanaldan ayrıldı.')  
        else:
            # send a follow-up message if not connected
            await interaction.followup.send('Bot bir kanalda değil.')  


# load this cog to be able to use functionally
async def setup(client):
    await client.add_cog(MusicBot(client))
