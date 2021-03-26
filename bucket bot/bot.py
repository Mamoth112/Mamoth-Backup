import discord
from discord.ext import commands, tasks
from pretty_help import PrettyHelp
import json
import toml
from twitchAPI import getGame, getLive, getUsers, refreshCode
import random
import ticket
from datetime import datetime, timedelta
from threading import Timer
import rustMapsAPI
import logging

logger = logging.getLogger('discord')
logger.setLevel(logging.DEBUG)
handler = logging.FileHandler(filename='discord.log', encoding='utf-8', mode='w')
handler.setFormatter(logging.Formatter('%(asctime)s:%(levelname)s:%(name)s: %(message)s'))
logger.addHandler(handler)

intents = discord.Intents.all()
with open('config.toml', 'r') as ctoml:
    config = toml.load(ctoml)
with open('config.json', 'r') as cjson:
    config2 = json.load(cjson)

bot = commands.AutoShardedBot(command_prefix=commands.when_mentioned_or('bucket '), case_insensitive=True, owner_ids=config2["ownerids"], intents=intents, help_command=PrettyHelp())
initial_extensions = ['cogs.members',
                      'cogs.owner',
                      'cogs.admin',
                      'cogs.welcome',
                      'cogs.tickets',
                      'cogs.rust',
                      'cogs.clan',
                      'cogs.error_handler']

for extension in initial_extensions:
    bot.load_extension(extension)


x=datetime.today()
y = x.replace(day=x.day, hour=1, minute=0, second=0, microsecond=0) + timedelta(days=1)
delta_t=y-x

secs=delta_t.total_seconds()

def every24Hour():
    with open('joins.json', 'r') as cjson:
        joins = json.load(cjson)
    joins['joins']['today'] = 0
    with open("joins.json", "w") as jsonFile:
        json.dump(joins, jsonFile)
    t = Timer(secs, every24Hour)
    t.start()

t = Timer(secs, every24Hour)
t.start()

@tasks.loop(seconds=7)
async def setPresence():
    await bot.change_presence(status=discord.Status.online, activity=discord.Activity(type=discord.ActivityType.watching, name=random.choice(config2["status"]).format(len(bot.users))))

@tasks.loop(seconds=7200) # 2 hours
async def refreshTwitchToken():
    await refreshCode()

@tasks.loop(seconds=30)
async def checkIfLive():
    with open('config.json', 'r') as cjson:
        config3 = json.load(cjson)
    res = await getLive()
    live = res['data'][0]['is_live']
    game = res['data'][0]['game_id']
    display_name = res['data'][0]['display_name']
    title = res['data'][0]['title']
    if live == True:
        if config3['Twitch']['Live'] != True:
            config3['Twitch']['Live'] = True
            with open("config.json", "w") as jsonFile:
                json.dump(config3, jsonFile)
                game = await getGame(game)
                viewers = await getUsers()
                e = discord.Embed(
                color=discord.Color(0x9146ff),
                title="**"+title+"**",
                description=f"Playing {game} for {viewers['viewer_count']} viewers\n[Watch Stream](https://twitch.tv/{display_name})",
                timestamp=datetime.utcnow())
                e.set_footer(text="Notification preview")
                e.set_author(
                    name=f"{display_name} is now live on Twitch!",
                    url="https://twitch.tv/"+display_name,
                    icon_url='https://cdn.discordapp.com/attachments/807472274214748170/807506395598553088/Rust-Bucket.png')
                e.set_image(
                    url=viewers['thumbnail_url'].format(width=1920, height=1080)
                )
                channel = await bot.fetch_channel(config3['announcement'])
                await channel.send(content="@everyone RustBucketGroup is live!", embed=e)
    else:
        config3['Twitch']['Live'] = False
        with open("config.json", "w") as jsonfile:
            json.dump(config3, jsonfile)


@bot.event
async def on_ready():
    print(f'\n\nLogged in as: {bot.user.name} - {bot.user.id}\nVersion: {discord.__version__}\n')
    print(f'Successfully logged in!')
    await bot.change_presence(status=discord.Status.online, activity=discord.Activity(type=discord.ActivityType.watching, name="{:,} Members...".format(len(bot.users))))

@bot.event
async def on_raw_reaction_add(user):
    if user.user_id != bot.user.id:
        with open('tickets.json', 'r') as cjson:
            ticketss = json.load(cjson)
        with open('config.json', 'r') as cjson:
            configg = json.load(cjson)
        ticketType = "general"
        if user.message_id == ticketss['panelID']:
          guild = discord.utils.get(bot.guilds, id=user.guild_id)
          channel= discord.utils.get(guild.channels, id=user.channel_id)
          message = await channel.fetch_message(user.message_id)
          await ticket.create(bot, user, ticketType, message)
          reaction = message.reactions[0]
          user = discord.utils.get(guild.members, id=user.user_id)
          await reaction.remove(user)
        elif user.message_id == configg['mapvoteId']:
            if user.emoji.name == "✅":
                channel = bot.get_channel(user.channel_id)
                message = await channel.fetch_message(user.message_id)
                reaction = discord.utils.get(message.reactions, emoji=user.emoji.name)
                if reaction and reaction.count >= 15:
                    await channel.send("MAP SELECTED")
                    await message.clear_reactions()
            elif user.emoji.name == "❌":
                channel = bot.get_channel(user.channel_id)
                message = await channel.fetch_message(user.message_id)
                reaction = discord.utils.get(message.reactions, emoji=user.emoji.name)
                if reaction and reaction.count >= 15:
                    await channel.send("MAP SKIPPED")
                    await message.clear_reactions()
                    monuments, mapURL, imageURL = await rustMapsAPI.getMaps()
                    embed = discord.Embed(title="Map Vote", colour=discord.Colour(0x3628bc), description=f"[Click Here for map link]({mapURL})")
                    embed.set_image(url=imageURL)
                    embed.set_thumbnail(url="https://cdn.discordapp.com/attachments/823828946055200829/823829023536185374/rb_22x.png")
                    embed.set_author(name="Bucket", icon_url="https://cdn.discordapp.com/attachments/823828946055200829/823829023536185374/rb_22x.png")
                    embed.set_footer(text=f"Bucket Bot\u3000".repeat(10), icon_url="https://cdn.discordapp.com/attachments/823828946055200829/823829023536185374/rb_22x.png")
                    airfield = False
                    bandit = False
                    outpost = False
                    excavator = False
                    junkyard = False
                    launch_site = False
                    military_tunnels = False
                    powerplant = False
                    sewer_branch = False
                    dome = False    
                    trainyard = False
                    water_treatment = False
                    for a in monuments:
                        if a == "Airfield":
                            airfield = True
                        elif a == "Bandit_Town":
                            bandit = True
                        elif a == "Outpost":
                            outpost = True
                        elif a == "Excavator":
                            excavator = True
                        elif a == "Junkyard":
                            junkyard = True
                        elif a == "Launch_Site":
                            launch_site = True
                        elif a == "Military_Tunnels":
                            military_tunnels = True
                        elif a == "Powerplant":
                            powerplant = True
                        elif a == "Sewer_Branch":
                            sewer_branch = True
                        elif a == "Sphere_Tank":
                            dome = True
                        elif a == "Trainyard":
                            trainyard = True
                        elif a == "Water_Treatment":
                            water_treatment = True
                    if airfield == True:
                        embed.add_field(name="Airfield", value="✅")
                    else:
                        embed.add_field(name="Airfield", value="❌")
                    if bandit == True:
                        embed.add_field(name="Bandit Camp", value="✅")
                    else:
                        embed.add_field(name="Bandit Camp", value="❌")
                    if outpost == True:
                        embed.add_field(name="Outpost", value="✅")
                    else:
                        embed.add_field(name="Outpost", value="❌")
                    if excavator== True:
                        embed.add_field(name="Excavator", value="✅")
                    else:
                        embed.add_field(name="Excavator", value="❌")
                    if junkyard == True:
                        embed.add_field(name="Junkyard", value="✅")
                    else:
                        embed.add_field(name="Junkyard", value="❌")
                    if launch_site == True:
                        embed.add_field(name="Launch Site", value="✅")
                    else:
                        embed.add_field(name="Launch Site", value="❌")
                    if military_tunnels == True:
                        embed.add_field(name="Military Tunnels", value="✅")
                    else:
                        embed.add_field(name="Military Tunnels", value="❌")
                    if powerplant == True:
                        embed.add_field(name="Powerplant", value="✅")
                    else:
                        embed.add_field(name="Powerplant", value="❌")
                    if sewer_branch == True:
                        embed.add_field(name="Sewer Branch", value="✅")
                    else:
                        embed.add_field(name="Sewer Branch", value="❌")
                    if dome == True:
                        embed.add_field(name="The Dome", value="✅")
                    else:
                        embed.add_field(name="The Dome", value="❌")
                    if trainyard == True:
                        embed.add_field(name="Trainyard", value="✅")
                    else:
                        embed.add_field(name="Trainyard", value="❌")
                    if water_treatment == True:
                        embed.add_field(name="Water Treatment", value="✅")
                    else:
                        embed.add_field(name="Water Treatment", value="❌")  
                    
                    message = await channel.send(embed=embed)
                    await message.add_reaction("✅")
                    await message.add_reaction("❌")
                    configg['mapvoteId'] = message.id
                    with open('./config.json', 'w') as cjson:
                        json.dump(configg, cjson)
            
bot.run(config["tokens"]['mainbot'], bot=True)