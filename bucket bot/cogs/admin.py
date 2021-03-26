from discord.ext import commands
import discord
from discord import File
import json
import toml
import asyncio
from datetime import timedelta


class AdminCog(commands.Cog):

    def __init__(self, bot):
        self.bot = bot

    with open('./config.json', 'r') as cjson:
        config = json.load(cjson)
    with open('config.toml', 'r') as ctoml:
        config2 = toml.load(ctoml)


    UNITS = {"s": "seconds", "m": "minutes", "h": "hours", "d": "days", "w": "weeks"}

    def convert_time_to_seconds(self, s):
        count = int(s[:-1])
        unit = self.UNITS[s[-1]]
        td = timedelta(**{unit: count})
        return td.seconds + 60 * 60 * 24 * td.days

    @commands.command(name='ban', hidden=True)
    @commands.has_any_role(config2['roles']['moderator'], config2['roles']['staff'])
    async def banuser(self, ctx, *, member):
        """Command which bans a user. e.g: [p]ban @user"""
        try:
            user = ctx.message.mentions[1]
            await ctx.guild.ban(user)
        except Exception as e:
            print(f'**`ERROR:`** {type(e).__name__} - {e}')
            await ctx.send(f'**`ERROR:`** FAILED TO BAN USER, CHECK LOGS FOR MORE DETAILS')
        else:
            await ctx.send(f'**Bucket banned {user.display_name}**')

    @commands.command(name='kick', hidden=True)
    @commands.has_any_role(config2['roles']['moderator'], config2['roles']['staff'])
    async def kickuser(self, ctx, *, member):
        """Command which kicks a user. e.g: [p]ban @user"""
        try:
            user = ctx.message.mentions[1]
            await ctx.guild.kick(user)
        except Exception as e:
            print(f'**`ERROR:`** {type(e).__name__} - {e}')
            await ctx.send(f'**`ERROR:`** FAILED TO KICK USER, CHECK LOGS FOR MORE DETAILS')
        else:
            await ctx.send(f'**Bucket 🦵 {user.display_name}**')


    @commands.command(name='unban', hidden=True)
    @commands.has_any_role(config2['roles']['moderator'], config2['roles']['staff'])
    async def unbanuser(self, ctx, *, member):
        """Command which unbans a user e.g: [p]unban [username]"""
        try:
            banned_users = await ctx.guild.bans()
            member_name, member_discriminator = member.split('#')
            for ban_entry in banned_users:
                user = ban_entry.user
                if (user.name, user.discriminator) == (member_name, member_discriminator):
                    await ctx.guild.unban(user)
        except Exception as e:
            print(f'**`ERROR:`** {type(e).__name__} - {e}')
            await ctx.send(f'**`ERROR:`** FAILED TO UNBAN USER, CHECK LOGS FOR MORE DETAILS')
        else:
            await ctx.send(f'**Bucket unbanned {user.display_name}**')

    @commands.command(name='mute', hidden=True)
    @commands.has_any_role(config2['roles']['moderator'], config2['roles']['staff'])
    async def muteuser(self, ctx, *args):
        """Command which temp mutes a user. e.g: [p]mute @user 1s 1h 1d"""
        try:
            user = ctx.message.mentions[1]
            time = 0
            print(args[0])
            print(args[1:])
            await user.add_roles(self.bot.guilds[0].get_role(self.config["muterole"]))
            for a in args[1:]:
                time = time + self.convert_time_to_seconds(a)
                print(time)
            await ctx.send(f'**USER {ctx.message.mentions[1].mention} WAS MUTED FOR {time} SECONDS**')
            await asyncio.sleep(time)
            await user.remove_roles(self.bot.guilds[0].get_role(self.config["muterole"]))
        except Exception as e:
            print(f'**`ERROR:`** {type(e).__name__} - {e}')
            await ctx.send(f'**`ERROR:`** FAILED TO MUTE USER, CHECK LOGS FOR MORE DETAILS')

    @commands.command(name='logs', hidden=True)
    @commands.has_any_role(config2['roles']['staff'])
    async def send_logs(self, ctx,):
        """Command which send the log to the user e.g: [p]logs"""
        try:
            user = ctx.author
            await user.send(content="Logs for Rust Bucket:", file=File('./discord.log'))
        except Exception as e:
            print(f'**`ERROR:`** {type(e).__name__} - {e}')
            await ctx.send('**`ERROR:`** FAILED TO SEND LOGS, CHECK LOGS FOR MORE DETAILS')
        else:
            pass


def setup(bot):
    bot.add_cog(AdminCog(bot))
