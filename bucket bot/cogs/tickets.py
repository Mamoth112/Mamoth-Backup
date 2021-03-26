import discord
from discord.ext import commands
import ticket
import json
from datetime import datetime
import toml


class TicketsCog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
      
    intents = discord.Intents.all()
    with open('config.toml', 'r') as ctoml:
        config = toml.load(ctoml)

    with open('./tickets.json', 'r') as cjson:
        ticketss = json.load(cjson)

    @commands.command(name="addUser")
    @commands.has_any_role(config['roles']['moderator'], config['roles']['staff'])
    async def addUser(self, ctx, *, args):
        """command which adds a user to a ticket
        member must be pinged"""
        if ctx.message.mentions:
          member =  discord.utils.get(ctx.guild.members, name=ctx.message.mentions[0].name)
          message = ctx.message
          await ticket.addUser(message, member)
        else:
          embed = discord.Embed(title="NO USER SPECIFIED", description="PLEASE SPECIFY A USER TO ADD", colour=ctx.message.author.colour)
          await ctx.channel.send(embed=embed)
        
    @commands.command(name="removeUser")
    @commands.has_any_role(config['roles']['moderator'], config['roles']['staff'])
    async def removeUser(self, ctx, *, args):
        """command which removes a user from a ticket
        member must be pinged"""
        if ctx.message.mentions:
          member =  discord.utils.get(ctx.guild.members, name=ctx.message.mentions[0].name)
          message = ctx.message
          await ticket.removeUser(message, member)
        else:
          embed = discord.Embed(title="NO USER SPECIFIED", description="PLEASE SPECIFY A USER TO ADD", colour=ctx.message.author.colour)
          await ctx.channel.send(embed=embed)
    
    @commands.command(name="claimticket", hidden=True)
    @commands.has_any_role(config['roles']['moderator'], config['roles']['staff'])
    async def claimTicket(self, ctx):
        """command which claims a ticket"""
        embed = discord.Embed(title="TICKET CLAIMED", description=f"ticket has been claimed by {ctx.author.display_name}", colour=ctx.message.author.colour)
        await ctx.channel.send(embed=embed)
    
    @commands.command(name="elevateTicket", hidden=True)
    @commands.has_any_role(config['roles']['moderator'], config['roles']['staff'])
    async def elevateTicket(self, ctx):
        """command which Elevates a ticket to the admins"""
        with open('tickets.json', 'r') as cjson:
          config = json.load(cjson)
        message = ctx.message
        embed = discord.Embed(title="TICKET ELEVATED", description=f"ticket has been elevated by {ctx.author.display_name},\nAdmins will be with your shortly!", colour=ctx.message.author.colour)
        await ctx.channel.send(embed=embed)
        channel = ctx.channel
        supportRoleId = config['supportRoleID']
        SupportRole = ctx.guild.get_role(supportRoleId)
        user = await ctx.guild.fetch_member(ctx.author.id)
        overwrites={
          message.guild.default_role: discord.PermissionOverwrite(read_messages=False),
          message.guild.me: discord.PermissionOverwrite(read_messages=True),
          SupportRole: discord.PermissionOverwrite(read_messages=False),
          SupportRole: discord.PermissionOverwrite(view_channel=False),
          user: discord.PermissionOverwrite(read_messages=True)
        }
        await channel.edit(overwrites=overwrites)
    
    @commands.command(name="closeTicket", hidden=True)
    async def closeTicket(self, ctx):
        """command which closes a ticket"""
        await ticket.close(self.bot, ctx.message)

    @commands.command(name="createPanel", hidden=True)
    @commands.has_any_role(config['roles']['staff'])
    async def createPanel(self, ctx):
      """command which creates a reaction ticket panel"""
      bot = self.bot
      app_info = await bot.application_info()
      embed = discord.Embed(title="Create a Ticket", colour=discord.Colour(0x1869f), description="React to create a ticket!")
      embed.set_thumbnail (url=app_info.icon_url)
      embed.set_author(name="Bucket Bot",   icon_url=app_info.icon_url)
      embed.set_footer(text="Bucket Bot", icon_url=app_info.icon_url)
      message = await ctx.message.channel.send(embed=embed)
      await message.add_reaction('📑')
      self.ticketss['panelID'] = message.id
      with open('./tickets.json', 'w') as jsonfile:
        json.dump(self.ticketss, jsonfile)
def setup(bot):
    bot.add_cog(TicketsCog(bot))