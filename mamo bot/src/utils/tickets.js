const { MessageEmbed, Guild } = require('discord.js');

async function create(user, type, message) {
  const SupportRole = await message.member.guild.members.cache.get(user.id).roles.cache.find(role => role.name === "Support Specialist");
  user = await message.member.guild.members.cache.get(user.id);
  if (!SupportRole) {
    user.guild.roles.create({
      data: {
        name: 'Support Specialist',
        color: 'BLUE',
      },
      reason: 'Created Role for Support Specialists',
    });
    SupportRole = user.guild.roles.cache.find(role => role.name === "Support Specialist");
  }
  try {
    let categoryTry = user.guild.channels.cache.find(c => c.name == "open-tickets");
  } catch (err) {
    await message.guild.channels.create("open-tickets", {
      type: 'category', permissionOverwrites: [{
        id: user.id,
        allow: ['VIEW_CHANNEL', 'SEND_MESSAGES', 'READ_MESSAGE_HISTORY'],
      },
      {
        id: SupportRole.id,
        allow: ['VIEW_CHANNEL', 'SEND_MESSAGES', 'READ_MESSAGE_HISTORY'],
      },
      {
        id: user.guild.id,
        deny: ['VIEW_CHANNEL', 'SEND_MESSAGES', 'READ_MESSAGE_HISTORY'],
      }]
    })
  }
  let category = user.guild.channels.cache.find(c => c.name === "open-tickets");
  let ch = await user.guild.channels.create(user.displayName + " - " + type, {
    type: "text", parent: category.id, permissionOverwrites: [
      {
        id: user.id,
        allow: ['VIEW_CHANNEL', 'SEND_MESSAGES', 'READ_MESSAGE_HISTORY'],
      },
      {
        id: SupportRole.id,
        allow: ['VIEW_CHANNEL', 'SEND_MESSAGES', 'READ_MESSAGE_HISTORY'],
      },
      {
        id: user.guild.id,
        deny: ['VIEW_CHANNEL', 'SEND_MESSAGES', 'READ_MESSAGE_HISTORY'],
      }
    ]
  });
};

async function addUser(message, user) {
  const ch = message.channel;
  user = await message.guild.members.fetch(user.id)
  if (ch.permissionsFor(message.member.guild.members.fetch(user.id)) == null) {
    ch.updateOverwrite(user.id, [
      {
        allow: ['VIEW_CHANNEL'],
        allow: ['SEND_MESSAGES'],
        allow: ['READ_MESSAGE_HISTORY']
      }
    ]);
  }
  const embed = new MessageEmbed()
    .setTitle(`Member Added to Ticket`)
    .setThumbnail(user.user.displayAvatarURL({ dynamic: true }))
    .setDescription(`Member: ${user.user}`)
    .setFooter(message.member.displayName, message.author.displayAvatarURL({ dynamic: true }))
    .setTimestamp()
    .setColor(message.member.displayHexColor);
  message.channel.send(embed)
}

async function removeUser(message, user) {
  const ch = message.channel;
  user = await message.guild.members.fetch(user.id)
  if (ch.permissionsFor(message.member.guild.members.fetch(user.id)) == null) {
    ch.updateOverwrite(user.id, [
      {
        deny: ['VIEW_CHANNEL'],
      }
    ]);
  }
  const embed = new MessageEmbed()
    .setTitle(`Member Removed From Ticket`)
    .setThumbnail(user.user.displayAvatarURL({ dynamic: true }))
    .setDescription(`Member: ${user.user}`)
    .setFooter(message.member.displayName, message.author.displayAvatarURL({ dynamic: true }))
    .setTimestamp()
    .setColor(message.member.displayHexColor);
  message.channel.send(embed)

}
async function close(message) {
  ch = message.channel;
  await ch.updateOverwrite(message.author.id, [
    {
      deny: ['VIEW_CHANNEL'],
    }
  ]);
  let category = message.member.guild.channels.cache.find(c => c.name === "closed-tickets");
  ch.setParent(category);
  const embed = new MessageEmbed()
    .setTitle(`Ticket Closing`)
    .setThumbnail(message.member.user.displayAvatarURL({ dynamic: true }))
    .setDescription("Ticket Closed by " + message.member.displayName)
    .setFooter(message.member.displayName, message.author.displayAvatarURL({ dynamic: true }))
    .setTimestamp()
    .setColor(message.member.displayHexColor);
  message.channel.send(embed)
}
module.exports = {
  addUser,
  create,
  removeUser,
  close
}