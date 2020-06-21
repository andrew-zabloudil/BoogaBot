import asyncio
import discord
from discord.ext import commands
from discord.utils import get

import youtube_dl


youtube_dl.utils.bug_reports_message = lambda: ''

ytdl_format_options = {
    'format': 'bestaudio/best',
    'outtmpl': '%(extractor)s-%(id)s-%(title)s.%(ext)s',
    'restrictfilenames': True,
    'noplaylist': True,
    'nocheckcertificate': True,
    'ignoreerrors': False,
    'logtostderr': False,
    'quiet': True,
    'no_warnings': True,
    'default_search': 'auto',
    # bind to ipv4 since ipv6 addresses cause issues sometimes
    'source_address': '0.0.0.0'
}

ffmpeg_options = {
    'options': '-vn'
}

ytdl = youtube_dl.YoutubeDL(ytdl_format_options)


class Music(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.voice = None

    @commands.command(name='join', help='Summons BoogaBot to the current voice channel.')
    async def join(self, ctx):
        channel = ctx.author.voice.channel
        if self.voice != None:
            await self.voice.move_to(channel)
        else:
            if ctx.author.voice.channel:
                self.voice = await channel.connect()
            else:
                await ctx.send('You are not currently in a voice channel.')

    @commands.command(name='leave', help='Summons BoogaBot to the current voice channel.')
    async def leave(self, ctx):
        if ctx.author.voice.channel != self.voice.channel:
            await ctx.send('You must be in the same voice channel as me to use that command.')
        else:
            if self.voice != None:
                await self.voice.disconnect()

    @commands.command(name='yt', help='Plays audio from a youtube URL.')
    async def play_youtube(self, ctx, url):
        # if self.voice != None:
        #     if ctx.author.voice.channel != self.voice.channel:
        #         await ctx.send('You must be in the same voice channel as me to use that command.')
        #     else:
        #         source = ytdl.extract_info(url, download=False)
        #         await ctx.send("Playing")
        #         ctx.voice_client.play(discord.FFmpegPCMAudio(source))
        # else:
        #     await ctx.send('Call me to a voice channel with !join to use that command.')
        async with ctx.typing():
            player = await YTDLSource.from_url(url, loop=self.bot.loop)
            ctx.voice_client.play(player, after=lambda e: print(
                'Player error: %s' % e) if e else None)

        await ctx.send('Now playing: {}'.format(player.title))


class YTDLSource(discord.PCMVolumeTransformer):
    def __init__(self, source, *, data, volume=0.5):
        super().__init__(source, volume)

        self.data = data

        self.title = data.get('title')
        self.url = data.get('url')

    @classmethod
    async def from_url(cls, url, *, loop=None, stream=False):
        loop = loop or asyncio.get_event_loop()
        data = await loop.run_in_executor(None, lambda: ytdl.extract_info(url, download=not stream))

        if 'entries' in data:
            # take first item from a playlist
            data = data['entries'][0]

        filename = data['url'] if stream else ytdl.prepare_filename(data)
        return cls(discord.FFmpegPCMAudio(filename, **ffmpeg_options), data=data)
