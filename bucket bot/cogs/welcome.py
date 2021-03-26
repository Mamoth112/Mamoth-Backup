from discord.ext import commands, tasks
import discord
import json
from datetime import datetime
import random


class WelcomeCog(commands.Cog):

    def __init__(self, bot):
        self.bot = bot
        with open('./config.json', 'r') as cjson:
            config = json.load(cjson)
        self.config = config
        with open('./joins.json', 'r') as cjson:
            joins = json.load(cjson)
        self.joins = joins


    @commands.Cog.listener(name="on_member_join")
    async def on_member_join(self, member):
        now = datetime.now()
        current_time = now.strftime("%H:%M:%S")
        print(f"{member.name}#{member.discriminator} joined at {current_time}")
        random_welcome_messages = [
            f"Welcome to {member.guild.name}, {member.mention}, grab yourself a drink and say g'day in <#789930598554796052>",
            f"Yooooooooooooo {member.mention}, thanks for joining the {member.guild.name}",
            f"WTF?! YOU'RE HERE! HOLY COW! WELCOME {member.mention}!",
            f"Put your hands together, {member.mention} just joined {member.guild.name}",
            f"How the bloody hell are ya {member.mention}? Thanks for joining {member.guild.name}",
            f"Pssssst... Seen ya sneak in here {member.mention}, the cool kids all hang out in <#789930598554796052>.",
            f"Welcome welcome {member.mention}!",
            f"{member.mention} lol. wtf is your profile photo? Kidding. Welcome to {member.guild.name}! We all hang out in <#789930598554796052>",
            f"G'day {member.mention}, thanks for joining {member.guild.name}",
            f"Howdy {member.mention}... Check out <#789930598554796052>",
            f"Howdy {member.mention}... Check out <#789930598554796052>", f"OMG OMG OMG OMG. hi {member.mention}",
            f"**A wild {member.mention} has just appeared from the mist** of the internet",
            f"Do you have aim {member.mention}?",
            f"Everybody put your hands together {member.mention} just arrived on a stallion",
            f"Clap yo hands ladies and gents {member.mention} just arrived.",
            f"If you've been searching for a place to call home on Rust {member.mention}, you've made it...",
            f"Ooops I did it again, to your heart, got lost, in this game of baaaby.. {member.mention} thanks for joining {member.guild.name}"]

        role = member.guild.get_role(self.config['joinrole'])
        welcomechannel = discord.utils.get(member.guild.channels, id=self.config['welcomechannel'])
        msglogchannel = discord.utils.get(member.guild.channels, id=self.config['msglogchannel'])
        await member.add_roles(role)

        embed = discord.Embed(title=f"User Joined", colour=0x3498DB)
        embed.set_thumbnail(url=member.avatar_url)
        embed.add_field(name=f"**Username**", value=f"{member.name}", inline=False)
        embed.add_field(name=f"**Discriminator**", value=f"{member.discriminator}", inline=False)
        embed.add_field(name=f"**ID**", value=f"{member.id}", inline=False)
        embed.set_footer(text=f"rustbucket.group | Rust Bucket • Today at {current_time}")
        await msglogchannel.send(embed=embed)

        await welcomechannel.send(random.choice(random_welcome_messages))
        if self.joins['joins']['messageId'] != 0:
            totalId = await welcomechannel.fetch_message(self.joins['joins']['messageId'])
            await totalId.delete()
        newtotalId = await welcomechannel.send(f"{self.joins['joins']['today'] + 1} users have joined today! <:rb:821611474056773693>")
        self.joins['joins']['today'] = self.joins['joins']['today'] + 1
        self.joins['joins']['messageId'] = newtotalId.id
        with open("./joins.json", "w") as jsonFile:
            json.dump(self.joins, jsonFile)


def setup(bot):
    bot.add_cog(WelcomeCog(bot))