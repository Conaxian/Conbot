### Imports

# Dependencies
from typing import Union
from discord import Embed, Message
Empty = Embed.Empty

# Conbot Modules
import const
from utils import time
from cmdtools import Context
from loclib import Loc

### Function Definitions

# Embed Factory
def embed(text: str="", **options) -> Embed:
    """
    Creates a Discord embed.

    ### Valid options:

    title: `str`
        The title of the embed.
        Default: `Empty`
    type: `str`
        The type of the embed.
        Default: `"rich"`
    url: `str`
        The URL of the embed.
        Default: `Empty`
    color: Union[`discord.Colour`, `int`]
        The hexadecimal color of the embed.
        Default: `const.embed_color`
    timestamp: `datetime.datetime`
        The timestamp of the embed.
        Default: `Empty`
    image: `str`
        The URL of the embed image.
        Default: `Empty`
    thumbnail: `str`
        The URL of the embed thumbnail.
        Default: `Empty`
    footer: `str`
        The name of the embed footer.
        Default: `Empty`
    footer_icon: `str`
        The URL of the embed footer's icon.
        Default: `Empty`
    author: `dict`
        Information about the embed author.
        Default: `{}`

        The dictionary can contain the following keys:
        name: `str`
            The name of the embed author.
            This value is mandatory when you specify an author.
        url: `str`
            The URL of the embed author.
            Default: `Empty`
        icon: `str`
            The URL of the embed author's icon.
            Default: `Empty`

    fields: Union[`dict`, `list`, `tuple`]
        A dictionary, a list or a tuple containing pairs
        of field names and values.
        Default: `{}`
    inline: `bool`
        Whether the embed fields are inline or not.
        Ignored when no fields are specified.
        Default: `False`
    """
    embed_ = Embed(
        description=text,
        title=options.get("title", Empty),
        type=options.get("type", "rich"),
        url=options.get("url", Empty),
        color=options.get("color", const.embed_color),
        timestamp=options.get("timestamp", Empty),
    )

    embed_ \
    .set_image(url=options.get("image", Empty)) \
    .set_thumbnail(url=options.get("thumbnail", Empty)) \
    .set_footer(
        text=options.get("footer", Empty),
        icon_url=options.get("footer_icon", Empty),
    )

    author = options.get("author", {})
    if author:
        embed_.set_author(
            name=author["name"],
            url=author.get("url", Empty),
            icon_url=author.get("icon", Empty),
        )

    fields = options.get("fields", {})
    if isinstance(fields, dict): fields = fields.items()
    for name, value in fields:
        embed_.add_field(
            name=name,
            value=value,
            inline=options.get("inline", False),
        )

    return embed_

# Embed Factory (from Context)
def cembed(
    ctx: Union[Context, Message],
    text: Union[str, Loc]="",
    **options
) -> Embed:
    """
    Creates a Discord embed from a Context.

    ### Valid options:

    title: Union[`str`, `loclib.Loc`]
        The title of the embed.
        Default: `Empty`
    type: `str`
        The type of the embed.
        Default: `"rich"`
    url: `str`
        The URL of the embed.
        Default: `Empty`
    timestamp: `datetime.datetime`
        The timestamp of the embed.
        Default: `Empty`
    image: `str`
        The URL of the embed image.
        Default: `Empty`
    thumbnail: `str`
        The URL of the embed thumbnail.
        Default: `Empty`
    footer: `str`
        The name of the embed footer.
        Default: `const.footer_text`
    footer_icon: `str`
        The URL of the embed footer's icon.
        Default: `const.footer_icon`
    author: `dict`
        Information about the embed author.
        Default: `{}`

        The dictionary can contain the following keys:
        name: Union[`str`, `loclib.Loc`]
            The name of the embed author.
            This value is mandatory when you specify an author.
        url: `str`
            The URL of the embed author.
            Default: `Empty`
        icon: `str`
            The URL of the embed author's icon.
            Default: `Empty`

    fields: Union[`dict`, `list`, `tuple`]
        A dictionary, a list or a tuple containing pairs
        of field names and values.
        Default: `{}`
    inline: `bool`
        Whether the embed fields are inline or not.
        Ignored when no fields are specified.
        Default: `False`
    """
    if isinstance(text, Loc): text = text.cstring(ctx)
    if isinstance(options.get("title", None), Loc):
        options["title"] = options["title"].cstring(ctx)

    if not options.get("footer", None):
        options["footer"] = const.footer_text.replace("$TIME", time())
    if not options.get("footer_icon", None):
        options["footer_icon"] = const.footer_icon

    author = options.get("author", {"name": None})
    if isinstance(author["name"], Loc):
        author["name"] = author["name"].cstring(ctx)

    fields = options.get("fields", {})
    if isinstance(fields, dict): fields = fields.items()
    loc_fields = []
    for name, value in fields:
        if isinstance(name, Loc): name = name.cstring(ctx)
        if isinstance(value, Loc): value = value.cstring(ctx)
        loc_fields.append([name, value])
    options["fields"] = loc_fields

    embed_ = embed(
        text,
        color=ctx.author.color,
        **options,
    )

    return embed_

# Footer
def tfooter(embed_: Embed) -> Embed:
    """
    Adds the time footer to an existing embed.
    """
    embed_.set_footer(
        text=const.footer_text.replace("$TIME", time()),
        icon_url=const.footer_icon,
    )
    return embed_
