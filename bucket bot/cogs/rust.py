import discord
from discord.ext import commands
import rustMapsAPI
import json
from datetime import datetime
import toml


class RustCog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    with open('./config.json', 'r') as cjson:
        config = json.load(cjson)
    with open('config.toml', 'r') as ctoml:
        config2 = toml.load(ctoml)

    @commands.command(name="vote", hidden=True)
    @commands.is_owner()
    async def mapVote(self, ctx):
        """command which creates a map vote"""
        bot = self.bot
        monuments, mapURL, imageURL = await rustMapsAPI.getMaps()
        embed = discord.Embed(title="Map Vote", colour=discord.Colour(0x3628bc), description=f"[Click Here for map link]({mapURL})")
        embed.set_image(url=imageURL)
        embed.set_thumbnail(url="https://cdn.discordapp.com/attachments/823828946055200829/823829023536185374/rb_22x.png")
        embed.set_author(name="Bucket", icon_url="https://cdn.discordapp.com/attachments/823828946055200829/823829023536185374/rb_22x.png")
        embed.set_footer(text=f"Bucket Bot"+"\u3000"*10, icon_url="https://cdn.discordapp.com/attachments/823828946055200829/823829023536185374/rb_22x.png")
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
        
        message = await ctx.send(embed=embed)
        await message.add_reaction("✅")
        await message.add_reaction("❌")
        self.config['mapvoteId'] = message.id
        with open('./config.json', 'w') as cjson:
            json.dump(self.config, cjson)
      # embed = discord.Embed(title="Create a Ticket", colour=discord.Colour(0x1869f), description="React to create a ticket!")
      # embed.set_thumbnail (url=app_info.icon_url)
      # embed.set_author(name="Bucket Bot",   icon_url=app_info.icon_url)
      # embed.set_footer(text="Bucket Bot", icon_url=app_info.icon_url)
      # message = await ctx.message.channel.send(embed=embed)
      # await message.add_reaction('📑')
      # self.ticketss['panelID'] = message.id
      # with open('./tickets.json', 'w') as jsonfile:
      #   json.dump(self.ticketss, jsonfile)
def setup(bot):
    bot.add_cog(RustCog(bot))