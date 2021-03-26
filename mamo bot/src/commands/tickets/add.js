const Command = require('../Command.js');
const { MessageEmbed } = require('discord.js');
const Tickets = require('../../utils/tickets.js');
const Utils = require('../../utils/utils.js')

module.exports = class AddCommand extends Command {
  constructor(client) {
    super(client, {
      name: 'add',
      aliases: ['add'],
      usage: 'add <user mention/ID>',
      description: 'adds a user to the ticket',
      type: client.types.TICKETS,
      examples: ['add @Mamoth112']
    });
  }
  run(message, args) {
    const member =  Utils.getUserFromMention(message.client, args[0])
    Tickets.addUser(message, member)
  }
};