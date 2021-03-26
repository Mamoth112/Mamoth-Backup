const Command = require('../Command.js');
const { MessageEmbed } = require('discord.js');
const Tickets = require('../../utils/tickets.js');

module.exports = class CloseCommand extends Command {
  constructor(client) {
    super(client, {
      name: 'close',
      aliases: ['cls'],
      usage: 'close',
      description: 'closes a ticket',
      type: client.types.TICKETS,
      examples: ['close']
    });
  }
  run(message, args) {
    Tickets.close(message)
  }
};