const Command = require('../Command.js');
const {
  MessageEmbed
} = require('discord.js');
const Tickets = require('../../utils/tickets.js');

module.exports = class CreatePanelCommand extends Command {
  constructor(client) {
    super(client, {
      name: 'createpanel',
      aliases: ['cp'],
      usage: 'createpanel <support type>',
      description: 'creates a ticket reaction panel for the specified support type',
      type: client.types.TICKETS,
      examples: ['createpanel Ban']
    });
  }
  async run(message, args) {
    let yar = 0;
    let yar2 = "none";
    switch (args[0].toLowerCase()) {
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
      case 'suggest':
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
      default:
        yar = 8;
        break;
    };
    console.log(yar)
    if (yar == 8) {
      const embed = new MessageEmbed()
        .setTitle(`Ticket Panel Creation Failed`)
        .setThumbnail(message.author.displayAvatarURL({
          dynamic: true
        }))
        .setDescription('Support type invalid. Make sure its one of the following: Ban, Billing, Bug, Question, Request, Suggest, Support, Ticket')
        .setFooter(message.member.displayName, message.author.displayAvatarURL({
          dynamic: true
        }))
        .setTimestamp()
        .setColor(message.member.displayHexColor);
      message.channel.send(embed);
      return;
    } else {
      const embed = new MessageEmbed()
        .setTitle(`Create a Ticket`)
        .setDescription(`React to Create a ${yar2} ticket`)
        .setTimestamp();
      let ticketId = await message.channel.send(embed);
      if (yar == 0) {
        message.client.db.settings.updateSupportIdBan.run(ticketId.id, message.guild.id)
      } else if (yar == 1) {
        message.client.db.settings.updateSupportIdBilling.run(ticketId.id, message.guild.id)
      } else if (yar == 2) {
        message.client.db.settings.updateSupportIdBug.run(ticketId.id, message.guild.id)
      } else if (yar == 3) {
        message.client.db.settings.updateSupportIdQuestion.run(ticketId.id, message.guild.id)
      } else if (yar == 4) {
        message.client.db.settings.updateSupportIdRequest.run(ticketId.id, message.guild.id)
      } else if (yar == 5) {
        message.client.db.settings.updateSupportIdSuggest.run(ticketId.id, message.guild.id)
      } else if (yar == 6) {
        message.client.db.settings.updateSupportIdSupport.run(ticketId.id, message.guild.id)
      } else if (yar == 7) {
        message.client.db.settings.updateSupportIdTicket.run(ticketId.id, message.guild.id)
      };
      await ticketId.react('📑')
    }
  }
};