const Command = require('../Command.js');
const { MessageEmbed } = require('discord.js');
const Tickets = require('../../utils/tickets.js');

module.exports = class DisableCommand extends Command {
  constructor(client) {
    super(client, {
      name: 'disable',
      aliases: ['disable'],
      usage: 'disable <support type>',
      description: 'disables a support type',
      type: client.types.TICKETS,
      examples: ['disable Ban']
    });
  }
  run(message, args) {
    const yar = 0;
    const yar2 = "ticket";
    switch(args[0].toLowercase()) {
      case "ban":
        yar = 0;
        yar2 = "ban";
        break;
      case "billing":
        yar = 1;
        yar2 = "billing";
        break;
      case "bug":
        yar = 2;
        yar2 = "bug";
        break;
      case "question":
        yar = 3;
        yar2 = "question";
        break;
      case "request":
        yar = 4;
        yar2 = "request";
        break;
      case "suggest":
        yar = 5;
        yar2 = "suggest";
        break;
      case "support":
        yar = 6;
        yar2 = "support";
        break;
      case "ticket":
        yar = 7;
        yar2 = "ticket";
        break;
    }
    if(yar = 0) {
      message.client.db.settings.updateSupportTypeBan.run(0, message.guild.id)
    } else if(yar = 1) {
      message.client.db.settings.updateSupportTypeBilling.run(0, message.guild.id)
    } else if(yar = 2) {
      message.client.db.settings.updateSupportTypeBug.run(0, message.guild.id)
    } else if(yar = 3) {
      message.client.db.settings.updateSupportTypeQuestion.run(0, message.guild.id)
    } else if(yar = 4) {
      message.client.db.settings.updateSupportTypeRequest.run(0, message.guild.id)
    } else if(yar = 5) {
      message.client.db.settings.updateSupportTypeSuggest.run(0, message.guild.id)
    } else if(yar = 6) {
      message.client.db.settings.updateSupportTypeSupport.run(0, message.guild.id)
    } else if(yar = 7) {
      message.client.db.settings.updateSupportTypeTicket.run(0, message.guild.id)
    } else {
      const embed = new MessageEmbed()
      .setTitle(`Ticket Type Disable Fail`)
      .setThumbnail(member.user.displayAvatarURL({ dynamic: true }))
      .setDescription('Support type invalid. Make sure its one of the following:\
      Ban, Billing, Bug, Question, Request, Suggest, Support, Ticket')
      .setFooter(message.member.displayName,  message.author.displayAvatarURL({ dynamic: true }))
      .setTimestamp()
      .setColor(member.displayHexColor);
    message.channel.send(embed);
    return;
    }
    const embed = new MessageEmbed()
      .setTitle(`Ticket Type Disable`)
      .setThumbnail(member.user.displayAvatarURL({ dynamic: true }))
      .setDescription('Support type ' + yar2 + ' disabled succesfully')
      .setFooter(message.member.displayName,  message.author.displayAvatarURL({ dynamic: true }))
      .setTimestamp()
      .setColor(member.displayHexColor);
    message.channel.send(embed);
  }
};