const Command = require('../Command.js');
const { MessageEmbed } = require('discord.js');
const Tickets = require('../../utils/tickets.js');
const Utils = require('../../utils/utils.js')

module.exports = class RemoveCommand extends Command {
  constructor(client) {
    super(client, {
      name: 'remove',
      aliases: ['remove'],
      usage: 'remove <user mention/ID>',
      description: 'removes a user to the ticket',
      type: client.types.TICKETS,
      examples: ['remove @Mamoth112']
    });
  }
  run(message, args) {
    const member =  Utils.getUserFromMention(message.client, args[0])
    Tickets.removeUser(message, member)
  }
};