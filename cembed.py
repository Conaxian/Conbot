################################################################

import discord

import constants
import utils

################################################################

# Creates an embed

def get_embed(text, title=None, url=None, author_name=None, author_img=None, timestamp=None, fields={}, inline=False, footer=True, color=None):

    color = color if color else constants.default_embed_color
    embed = discord.Embed(description=str(text), colour=color)

    if title:
        embed.title = str(title)

    if url:
        embed.url = url

    if author_name and author_img:
        embed.set_author(name=author_name, icon_url=str(author_img))

    if timestamp:
        embed.timestamp = timestamp

    for field in fields.items():
        field = list(field)
        field[0] = "\u200b" if str(field[0]).isspace() else str(field[0])
        field[1] = "\u200b" if str(field[1]).isspace() else str(field[1])
        embed.add_field(name=field[0], value=field[1], inline=inline)

    if footer:
        embed.set_footer(text=f"{utils.time()} UTC", icon_url="http://conax.cz/conbot/embed_clock.png")

    return embed

################################################################

# Creates an embed using information obtained from the message

def get_cembed(msg, text, title=None, url=None, author_name=None, author_img=None, timestamp=None, fields={}, inline=False,  footer=True):

    return get_embed(text, title, url, author_name, author_img, timestamp, fields, inline, footer, msg.author.color)

################################################################