### Imports

# Standard Library
import sys

# Conbot Modules
sys.path.append("..")
import const
import utils
from cmdtools import Arg, CmdError
from cembed import embed, cembed, tfooter
from loclib import Loc
from musiclib import queues, yt_search, Audio, AudioDurationError

### Command

# Command Meta
meta = {
    "name": "play",
    "aliases": [
        "p",
        "song",
        "music",
        "youtube",
        "yt",
    ],
    "category": "music",
    "index": 2,
    "args": [
        Arg("<query>", "inf_str"),
    ],
}

# Command Call
async def call(ctx):
    author_voice = ctx.author.voice
    if not author_voice:
        raise CmdError("cmd/join/no_voice")

    voice = utils.get(ctx.bot.voice_clients, guild=ctx.guild)
    if not voice:
        voice = await author_voice.channel.connect()
        channel_name = utils.escape_md(str(author_voice.channel))
        text = Loc("cmd/join/success").format(channel_name)
        embed_ = cembed(ctx, text)
        await ctx.reply(embed=embed_)

    if len(queues.get(ctx.guild.id, [])) >= const.music_queue_limit:
        raise CmdError("cmd/play/max_queue", const.music_queue_limit)

    audio_url = await yt_search(ctx.args["query"])
    if not audio_url:
        raise CmdError("cmd/play/not_found")

    try:
        audio = Audio(ctx)
        await audio.init(audio_url)
    except AudioDurationError:
        max_length = str(round(const.music_max_length / 60, 2)) \
            .rstrip("0").rstrip(".")
        raise CmdError("cmd/play/too_long", max_length)

    queue = queues.get(ctx.guild.id, [])
    if not queue:
        queues[ctx.guild.id] = [audio]
        audio.play(voice)
        text = Loc("cmd/play/playing")
    else:
        queue.append(audio)
        text = Loc("cmd/play/add_queue")

    name = utils.escape_md(audio.info["title"])
    text.format(name)
    embed_ = tfooter(embed(text.cstring(ctx.guild)))
    await ctx.send(embed=embed_)
