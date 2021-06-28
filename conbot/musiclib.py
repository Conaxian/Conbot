### Imports

# Dependencies
from discord import VoiceClient, FFmpegPCMAudio, PCMVolumeTransformer
from youtube_dl import YoutubeDL
from youtubesearchpython.__future__ import VideosSearch

# Conbot Modules
import const
from utils import escape_md
from cmdtools import Context
from cembed import embed, tfooter
from loclib import Loc

### Initialization

# YouTube Downloader Options
ytdl_options = {
    "format": "bestaudio/best",
    "outtmpl": "%(extractor)s-%(id)s-%(title)s.%(ext)s",
    "restrictfilenames": True,
    "noplaylist": True,
    "nocheckcertificate": True,
    "ignoreerrors": False,
    "logtostderr": False,
    "quiet": True,
    "no_warnings": True,
    "default_search": "auto",
    "source_address": "0.0.0.0",
}

# FFmpeg Options
ffmpeg_options = {
    "before_options": "-reconnect 1 -reconnect_streamed 1 \
-reconnect_delay_max 5",
    "options": "-vn",
}

# Youtube Downloader
ytdl = YoutubeDL(ytdl_options)

# Music Queues
queues = {}

### Class Definitions

# Audio
class Audio:
    """
    Represents a YouTube audio stream.
    """

    def __init__(self, ctx: Context):
        self.ctx = ctx
        self.playing = False

    async def init(self, yt_url: str):
        """
        Initializes the audio from a YouTube URL.
        """
        extract_info = lambda: ytdl.extract_info(yt_url,
            download=False)
        self.info = await self.ctx.bot.async_exec(extract_info)
        if self.info["duration"] > const.music_max_length:
            raise AudioDurationError
        self.audio = FFmpegPCMAudio(self.info["url"], **ffmpeg_options)

    def play(self, voice: VoiceClient):
        """
        Plays the audio stream.
        """
        voice.play(self.audio)
        voice.source = PCMVolumeTransformer(voice.source,
            volume=const.player_volume)
        self.playing = True

### Function Definitions

# YouTube Serach
async def yt_search(query: str) -> str:
    """
    Searches a query on YouTube and returns a URL.
    """
    videos = VideosSearch(query, limit=1)
    video = (await videos.next())["result"]
    return f"https://www.youtube.com/watch?v={video[0]['id']}" \
        if video else None

# Player Check
async def player_check(voices: list[VoiceClient]):
    """
    Checks the music player.
    """
    for voice in voices:
        queue = queues.get(voice.guild.id, [])

        if len(voice.channel.members) <= 1:
            await voice.disconnect()
            queue.clear()

        elif not voice.is_playing() and not voice.is_paused():
            if queue and queue[0].playing:
                queue.pop(0)
                if not queue: continue

                queue[0].play(voice)
                name = escape_md(queue[0].info["title"])
                text = Loc("cmd/play/playing").format(name)
                ctx = queue[0].ctx
                embed_ = tfooter(embed(text.cstring(ctx.guild)))
                await ctx.send(embed=embed_)

### Player Errors

class AudioDurationError(Exception):
    """
    Raised when the requested song is too long.
    """
