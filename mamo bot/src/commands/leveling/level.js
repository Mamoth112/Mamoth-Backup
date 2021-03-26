const Command = require('../Command.js');
const { MessageEmbed } = require('discord.js');
const { oneLine } = require('common-tags');

module.exports = class LevelCommand extends Command {
  constructor(client) {
    super(client, {
      name: 'level',
      aliases: ['lvl'],
      usage: 'level @user',
      description: 'Send the mentioned users level and points and yours if no user mentioned',
      type: client.types.LEVELING,
      examples: ['level @Mamoth112']
    });
  }
  run(message, args) {
    const member =  this.getMemberFromMention(message, args[0]) || 
      message.guild.members.cache.get(args[0]) || 
      message.member;
    const key = `${message.guild.id}-${member.id}`;
    message.channel.send(`You currently have ${message.client.points.get(key, "points")} points, and are level ${message.client.points.get(key, "level")}!`);

  }
}