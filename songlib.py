################################################################

import os
import urllib
import re
import youtube_dl

import constants

################################################################

play_text_output = {}

################################################################

# Gets the amount of songs in the queue

def queue_length(guild):

    try:
        path = f"{constants.song_dir}/{guild.id}"
        return len(os.listdir(path))
    except FileNotFoundError:
        return 0

################################################################

# Gets the path of the song in the specified position

def get_song_path(guild, position):

    path = f"{constants.song_dir}/{guild.id}"
    songs = os.listdir(path)
    for song in songs:
        song_position = song.split("$<|sep;|>")[0]
        if int(song_position) == position:
            return f"{path}/{song}"

################################################################

# Downloads a song from YouTube and saves it the specified path

async def download_song(guild, name, position):

    name = urllib.parse.quote(name, safe="")
    search_url = f"https://www.youtube.com/results?search_query={name}"
    html = urllib.request.urlopen(search_url)
    html = html.read().decode()
    videos = re.findall(r"watch\?v=(\S{11})", html)
    if len(videos) < 1:
        return 1
    url = f"https://www.youtube.com/watch?v={videos[0]}"

    path = f"{constants.song_dir}/{guild.id}/{position}$<|sep;|>%(title)s.%(ext)s"

    ydl_options = {
        "format": "bestaudio/best",
        "outtmpl": path,
        "postprocessors": [{
                "key": "FFmpegExtractAudio",
                "preferredcodec": "mp3",
                "preferredquality": "192",
        }]
    }

    with youtube_dl.YoutubeDL(ydl_options) as ytdl:
        file_info = ytdl.extract_info(url, download=False)
        file_size = file_info["formats"][0]["filesize"]
        file_length = file_info["duration"]
        if file_size > constants.song_max_size or file_length > constants.song_max_length:
            return 2
        ytdl.download([url])
    
    return 0

################################################################

# Deletes the first song in the queue and shifts the queue

async def shift_queue(guild):

    path = f"{constants.song_dir}/{guild.id}"
    song_amount = queue_length(guild)
    if song_amount <= 1:
        os.system(f"rm -rf {path}")
        os.mkdir(f"{path}")

    else:
        os.remove(get_song_path(guild, 1))
        for i in range(2, song_amount + 1):
            path = get_song_path(guild, i)
            song_name = path.split("$<|sep;|>")[1]
            song_name = f"$<|sep;|>{song_name}"
            path = f"{constants.song_dir}/{guild.id}/"
            os.rename(f"{path}{i}{song_name}", f"{path}{i - 1}{song_name}")

################################################################