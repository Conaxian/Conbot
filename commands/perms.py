################################################################

import sys

sys.path.append("..")

import utils
import cembed
import loclib

################################################################

async def perms(ctx):

    if not ctx.args["member"]:
        member = ctx.guild.get_member(ctx.author.id)
    else:
        member_id = utils.mention_id(ctx.args["member"])
        member = ctx.guild.get_member(member_id)
        if not member:
            text = loclib.Loc.member("err_unknown_member", ctx.author)
            text.format(ctx.client.user.mention)
            embed = cembed.get_cembed(ctx.msg, text)
            await ctx.channel.send(embed=embed)
            return

    perms = member.guild_permissions
    fields = {}
    perm_list = ["administrator", "view_channel", "manage_channels", "manage_roles", "manage_emojis", "view_audit_log", "manage_webhooks", "manage_guild"]
    perm_list += ["send_messages", "embed_links", "attach_files", "add_reactions", "external_emojis", "mention_everyone", "manage_messages", "read_message_history", "send_tts_messages", "use_slash_commands"]
    perm_list += ["create_instant_invite", "change_nickname", "manage_nicknames", "kick_members", "ban_members"]
    perm_list += ["connect", "speak", "stream", "use_voice_activation", "priority_speaker", "mute_members", "deafen_members", "move_members"]
    yes = loclib.Loc.member("label_yes", ctx.author)
    no = loclib.Loc.member("label_no", ctx.author)

    for perm in perm_list:
        enabled = f"**[{yes}]" if getattr(perms, perm) else f"**[{no}]"
        enabled += "(https://discord.com/developers/docs/topics/permissions)**"
        name = loclib.Loc.member(f"perm_{perm}", ctx.author)
        fields[name] = enabled

    perms_text = loclib.Loc.member("text_perms_list", ctx.author)
    perms_text.format(member.mention)
    perms_title = loclib.Loc.member("text_perms_title", ctx.author)
    perms_title.format(ctx.guild.name)

    embed = cembed.get_cembed(ctx.msg, perms_text, perms_title, author_name=member.name, author_img=member.avatar_url, fields=fields, inline=True)
    await ctx.channel.send(embed=embed)

################################################################