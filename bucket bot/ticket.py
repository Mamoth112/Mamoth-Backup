import discord
from discord.ext import commands
from datetime import datetime
import json

async def create(bot, user, type, message):
  with open('tickets.json', 'r') as cjson:
    config = json.load(cjson)
  guild = message.guild
  supportRoleId = config['supportRoleID']
  SupportRole = guild.get_role(supportRoleId)
  user = await guild.fetch_member(user.user_id)
  category = discord.utils.get(message.guild.channels, name="open-tickets")
  overwrites={
    message.guild.default_role: discord.PermissionOverwrite(read_messages=False),
    message.guild.me: discord.PermissionOverwrite(read_messages=True),
    SupportRole: discord.PermissionOverwrite(read_messages=True),
    user: discord.PermissionOverwrite(read_messages=True)
  }
  await user.guild.create_text_channel(user.display_name + " - " + type, overwrites=overwrites, category=category)

async def addUser(message, user):
  ch = message.channel
  user = discord.utils.get(message.guild.members, id=user.id)
  await ch.set_permissions(user, read_messages=True, send_messages=True, read_message_history=True)
  embed = discord.Embed(title="Member Added to Ticket", colour=discord.Colour(0x1869f), description="Member: "+user.display_name)
  embed.set_thumbnail (url=user.avatar_url)
  embed.set_author(name="Bucket Bot",   icon_url=user.avatar_url)
  embed.set_footer(text=user.display_name, icon_url=user.avatar_url)
  await message.channel.send(embed=embed)

async def removeUser(message, user):
  ch = message.channel
  user = discord.utils.get(message.guild.members, id=user.id)
  await ch.set_permissions(user, overwrite=None)
  embed = discord.Embed(title="Member Removed from Ticket", colour=discord.Colour(0x1869f), description="Member: "+user.display_name)
  embed.set_thumbnail (url=user.avatar_url)
  embed.set_author(name="Bucket Bot",   icon_url=user.avatar_url)
  embed.set_footer(text=user.display_name, icon_url=user.avatar_url)
  await message.channel.send(embed=embed)


async def close(bot, message):
  with open('tickets.json', 'r') as cjson:
    config = json.load(cjson)
  ch = message.channel;
  user = discord.utils.get(message.guild.members, mention=message.author.mention)
  for b in ch.members:
    await ch.set_permissions(b, overwrite=None)
  category = await bot.fetch_channel(config['closedID'])
  await ch.edit(category=category)
  embed = discord.Embed(title="Ticket Closed", colour=discord.Colour(0x1869f), description="Member: "+ user.display_name)

  embed.set_thumbnail (url=user.avatar_url)
  embed.set_author(name="Bucket Bot",   icon_url=user.avatar_url)
  embed.set_footer(text=user.display_name, icon_url=user.avatar_url)
  await message.channel.send(embed=embed)