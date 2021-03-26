from discord.enums import AuditLogAction
from discord.ext import commands, tasks, menus
import json
from datetime import datetime
import random
import numpy
import discord

class Confirm(menus.Menu):
    def __init__(self, msg, user):
        super().__init__(timeout=21600.0, delete_message_after=True) # 6 Hour Timeout
        self.msg = msg
        self.user = user
        self.result = None

    async def send_initial_message(self, ctx, channel):
        return await self.user.send(self.msg)

    @menus.button('\N{WHITE HEAVY CHECK MARK}')
    async def do_confirm(self, payload):
        self.result = True
        self.stop()

    @menus.button('\N{CROSS MARK}')
    async def do_deny(self, payload):
        self.result = False
        self.stop()

    async def prompt(self, ctx):
        await self.start(ctx, wait=True)
        return self.result

class ClanCog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    

    with open('./config.json', 'r') as cjson:
        config = json.load(cjson)

    @commands.command(name="clannew")
    async def newClan(self, ctx, *, clanName):
        """Command which creates a new clan"""
        with open('./clan.json', 'r') as cjson:
            clans = json.load(cjson)
        failed = False
        if clans['clans']:
            for i in clans['clans']:
                location = clans['clans'].index(i)
                if i['owner'] == ctx.author.id:
                    await ctx.send('**FAILED TO CREATE NEW CLAN**\n you are already own a clan, please disband your clan!')
                    break
                elif i['name'] == clanName:
                    await ctx.send('**FAILED TO CREATE NEW CLAN**\n this clan name is already in use')
                    break
                elif failed == False:
                    if clans['clans'][location]['members']:
                        for a in clans['clans'][location]['members']:
                            if a == ctx.author.id:
                                await ctx.send('**FAILED TO CREATE NEW CLAN**\n you are already apart of a clan, ask your clan leader to remove you')
                                break
                            else:
                                clans['clans'].append({"name": clanName, "owner": ctx.author.id, "members": []})
                                embed = discord.Embed(title="New clan Created", colour=discord.Colour(0x204d5b), description=f"{ctx.author.display_name} created a new clan {clanName}!")
                                embed.set_author(name=ctx.author.display_name, icon_url=ctx.author.avatar_url)
                                embed.set_footer(text="Bucket", icon_url="https://cdn.discordapp.com/attachments/823828946055200829/823829023536185374/rb_22x.png")
                                await ctx.send(embed=embed)
                                break
                    else:
                        clans['clans'].append({"name": clanName, "owner": ctx.author.id, "members": []})
                        embed = discord.Embed(title="New clan Created", colour=discord.Colour(0x204d5b), description=f"{ctx.author.display_name} created a new clan {clanName}!")
                        embed.set_author(name=ctx.author.display_name, icon_url=ctx.author.avatar_url)
                        embed.set_footer(text="Bucket", icon_url="https://cdn.discordapp.com/attachments/823828946055200829/823829023536185374/rb_22x.png")
                        await ctx.send(embed=embed)
                        break
        elif not clans['clans']:
            clans['clans'].append({"name": clanName, "owner": ctx.author.id, "members": []})
            embed = discord.Embed(title="New clan Created", colour=discord.Colour(0x204d5b), description=f"{ctx.author.display_name} created a new clan {clanName}!")
            embed.set_author(name=ctx.author.display_name, icon_url=ctx.author.avatar_url)
            embed.set_footer(text="Bucket", icon_url="https://cdn.discordapp.com/attachments/823828946055200829/823829023536185374/rb_22x.png")
            await ctx.send(embed=embed)
        with open('./clan.json', 'w') as cjson:
            json.dump(clans, cjson)
    
    @commands.command(name="clanrename")
    async def renameClan(self, ctx, *, clanName):
        """Command which renames a clan"""
        with open('./clan.json', 'r') as cjson:
            clans = json.load(cjson)
            failed = False
        for i in clans['clans']:
            if i['owner'] == ctx.author.id:
                if i['name'] == clanName:
                    await ctx.send('**FAILED TO RENAME CLAN**\n this clan name is already in use')
                    break
                elif failed == False:
                    location = clans['clans'].index(i)
                    clans['clans'].append({"name": clanName, "owner": ctx.author.id, "members": i['members']})
                    clanName2 = clans['clans'][-1]['name']
                    clanNameold = i['name']
                    clans['clans'].pop(location)
                    embed = discord.Embed(title="Clan Renamed", colour=discord.Colour(0x204d5b), description=f"{ctx.author.display_name} renamed clan {clanNameold} to {clanName2}!")
                    embed.set_author(name=ctx.author.display_name, icon_url=ctx.author.avatar_url)
                    embed.set_footer(text="Bucket", icon_url="https://cdn.discordapp.com/attachments/823828946055200829/823829023536185374/rb_22x.png")
                    await ctx.send(embed=embed)

        with open('./clan.json', 'w') as cjson:
            json.dump(clans, cjson)
        
    @commands.command(name="clandisband")
    async def disbandClan(self, ctx):
        """Command which disbands clan"""
        with open('./clan.json', 'r') as cjson:
            clans = json.load(cjson)
        for i in clans['clans']:
            if i['owner'] == ctx.author.id:
                location = clans['clans'].index(i)
                clanName = clans['clans'][location]['name']
                clans['clans'].pop(location)
                embed = discord.Embed(title="Clan Disbanded", colour=discord.Colour(0x204d5b), description=f"{ctx.author.display_name} Disbanded clan {clanName}!")
                embed.set_author(name=ctx.author.display_name, icon_url=ctx.author.avatar_url)
                embed.set_footer(text="Bucket", icon_url="https://cdn.discordapp.com/attachments/823828946055200829/823829023536185374/rb_22x.png")
                await ctx.send(embed=embed)
            else:
                location = clans['clans'].index(i)
                clanName = clans['clans'][location]['name']
                embed = discord.Embed(title="Clan Disband", colour=discord.Colour(0x204d5b), description=f"You cant disband this clan! Your not the owner of clan {clanName}")
                embed.set_author(name=ctx.author.display_name, icon_url=ctx.author.avatar_url)
                embed.set_footer(text="Bucket", icon_url="https://cdn.discordapp.com/attachments/823828946055200829/823829023536185374/rb_22x.png")
                await ctx.send(embed=embed)
        with open('./clan.json', 'w') as cjson:
            json.dump(clans, cjson)
    
    @commands.command(name="clanadduser")
    async def addUserClan(self, ctx, *, user: discord.Member):
        """Command which adds a user to the clan"""

        with open('./clan.json', 'r') as cjson:
            clans = json.load(cjson)
        for i in clans['clans']:
            if i['owner'] == ctx.author.id:
                location = clans['clans'].index(i)
                clanName = clans['clans'][location]['name']                
                confirm_invite = await Confirm(f'Would you like to join {clanName}?', user).prompt(ctx)
                embed = discord.Embed(title="User Requested to join clan", colour=discord.Colour(0x204d5b), description=f"{ctx.author.display_name} requested {user.display_name} to join {clanName}!")
                embed.set_author(name=ctx.author.display_name, icon_url=ctx.author.avatar_url)
                embed.set_footer(text="Bucket", icon_url="https://cdn.discordapp.com/attachments/823828946055200829/823829023536185374/rb_22x.png")
                await ctx.send(embed=embed)
                if confirm_invite:
                    clans['clans'][location]['members'].append(user.id)
                    embed = discord.Embed(title="User Added to clan", colour=discord.Colour(0x204d5b), description=f"{ctx.author.display_name} added user {user.display_name} to {clanName}!")
                    embed.set_author(name=ctx.author.display_name, icon_url=ctx.author.avatar_url)
                    embed.set_footer(text="Bucket", icon_url="https://cdn.discordapp.com/attachments/823828946055200829/823829023536185374/rb_22x.png")
                    await ctx.send(embed=embed)
            else:
                embed = discord.Embed(title="Add User to clan", colour=discord.Colour(0x204d5b), description=f"You cant add a user this clan! Your not the owner of clan {clanName}")
                embed.set_author(name=ctx.author.display_name, icon_url=ctx.author.avatar_url)
                embed.set_footer(text="Bucket", icon_url="https://cdn.discordapp.com/attachments/823828946055200829/823829023536185374/rb_22x.png")
                await ctx.send(embed=embed)
        with open('./clan.json', 'w') as cjson:
            json.dump(clans, cjson)
    
    @commands.command(name="clanremoveuser")
    async def removeUserClan(self, ctx, *, user: discord.Member):
        """Command which removes a user from the clan"""
        with open('./clan.json', 'r') as cjson:
            clans = json.load(cjson)
        for i in clans['clans']:
            if i['owner'] == ctx.author.id:
                location = clans['clans'].index(i)
                clanName = clans['clans'][location]['name']
                userLocation = clans['clans'][location]['members'].index(user.id)
                clans['clans'][location]['members'].pop(userLocation)
                embed = discord.Embed(title="User Removed from clan", colour=discord.Colour(0x204d5b), description=f"{ctx.author.display_name} removed user {user.display_name} from clan {clanName}!")
                embed.set_author(name=ctx.author.display_name, icon_url=ctx.author.avatar_url)
                embed.set_footer(text="Bucket", icon_url="https://cdn.discordapp.com/attachments/823828946055200829/823829023536185374/rb_22x.png")
                await ctx.send(embed=embed)
            else:
                embed = discord.Embed(title="Remove User from clan", colour=discord.Colour(0x204d5b), description=f"You cant remove a user from clan! Your not the owner of clan {clanName}")
                embed.set_author(name=ctx.author.display_name, icon_url=ctx.author.avatar_url)
                embed.set_footer(text="Bucket", icon_url="https://cdn.discordapp.com/attachments/823828946055200829/823829023536185374/rb_22x.png")
                await ctx.send(embed=embed)
        with open('./clan.json', 'w') as cjson:
            json.dump(clans, cjson)
    
    @commands.command(name="clanleave")
    async def leaveClan(self, ctx):
        """Command which leaves a clan"""
        with open('./clan.json', 'r') as cjson:
            clans = json.load(cjson)
        for i in clans['clans']:
            if i['owner'] == ctx.author.id:
                embed = discord.Embed(title="Leave Clan", colour=discord.Colour(0x204d5b), description=f"You cant leave this clan! you are the owner!")
                embed.set_author(name=ctx.author.display_name, icon_url=ctx.author.avatar_url)
                embed.set_footer(text="Bucket", icon_url="https://cdn.discordapp.com/attachments/823828946055200829/823829023536185374/rb_22x.png")
                await ctx.send(embed=embed)
            else:
                location = clans['clans'].index(i)
                location2 = clans['clans'][location]['members'].index(ctx.author.id)
                clans['clans'][location]['members'].pop(location2)
                embed = discord.Embed(title="Left clan", colour=discord.Colour(0x204d5b), description=f"You left the clan!")
                embed.set_author(name=ctx.author.display_name, icon_url=ctx.author.avatar_url)
                embed.set_footer(text="Bucket", icon_url="https://cdn.discordapp.com/attachments/823828946055200829/823829023536185374/rb_22x.png")
                await ctx.send(embed=embed)
        with open('./clan.json', 'w') as cjson:
            json.dump(clans, cjson)


def setup(bot):
    bot.add_cog(ClanCog(bot))