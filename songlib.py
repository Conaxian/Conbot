################################################################

import discord
import youtube_dl
import youtubesearchpython.__future__ as ytsearch

import const
import cembed
import loclib

################################################################

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
    "source_address": "0.0.0.0"
}

ffmpeg_options = {
    "before_options": "-reconnect 1 -reconnect_streamed 1 -reconnect_delay_max 5",
    "options": "-vn"
}

queues = {}

################################################################

# Search for a song on YouTube and return the link

async def yt_search(name):

    videos = ytsearch.VideosSearch(name, limit=1)
    video = (await videos.next())["result"]
    video_id = video[0]["id"] if video else None
    return f"https://www.youtube.com/watch?v={video_id}" if video_id else None

################################################################

# Get the song from the URL

async def get_song(url, loop):

    with youtube_dl.YoutubeDL(ytdl_options) as ytdl:
        song_info = await loop.run_in_executor(None, lambda: ytdl.extract_info(url, download=False))
        if song_info["duration"] > const.song_max_length:
            return None, None
        song_file = song_info["url"]
        return discord.FFmpegPCMAudio(song_file, **ffmpeg_options), song_info

################################################################

# Play a song in a voice channel

async def play_song(voice, song):

    voice.play(song["song"])
    song["playing"] = True
    voice.source = discord.PCMVolumeTransformer(voice.source)
    voice.source.volume = const.player_volume

################################################################

# Check the music player, if a song has finished playing, remove it from the queue and start playing the next song (if there is any)

async def player_check(voices):

    # Disconnect from empty voice channels

    for voice in voices:
        queue = queues.get(voice.guild.id, [])

        if len(voice.channel.members) <= 1:
            await voice.disconnect()
            queue.clear()

        # Check if the current song has finished playing

        elif not voice.is_playing() and not voice.is_paused():

            # Remove the current song from queue

            if len(queue) >= 1 and queue[0]["playing"]:
                queue.pop(0)

                # If there are more songs in the queue, start playing the next song

                if len(queue) >= 1:
                    song = queue[0]
                    await play_song(voice, song)
                    text = loclib.Loc.server("text_play_playing", voice.guild)
                    text.format(song["info"]["title"])
                    embed = cembed.get_embed(text)
                    await song["context"].channel.send(embed=embed)

################################################################
