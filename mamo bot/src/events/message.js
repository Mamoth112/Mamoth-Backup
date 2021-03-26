const { MessageEmbed } = require('discord.js');
const { oneLine } = require('common-tags');
const Enmap = require("enmap");
const config = require("../../config.json");

module.exports = (client, message) => {
  client.points = new Enmap("points");
  if (message.channel.type === 'dm' || !message.channel.viewable || message.author.bot) return;

  // Get disabled commands
  let disabledCommands = client.db.settings.selectDisabledCommands.pluck().get(message.guild.id) || [];
  if (typeof(disabledCommands) === 'string') disabledCommands = disabledCommands.split(' ');
  
  // Get points
  const { point_tracking: pointTracking, message_points: messagePoints, command_points: commandPoints } = 
    client.db.settings.selectPoints.get(message.guild.id);
  
  const key = `${message.guild.id}-${message.author.id}`;
  client.points.ensure(key, {
    user: message.author.id,
    guild: message.guild.id,
    points: 0,
    level: 0,
    time: new Date().getTime()
  });
  currentTime = new Date().getTime();
  messageTime = parseInt(client.points.get(key, "time")) + 1000;
  if (messageTime < currentTime) {
    client.points.set(key, currentTime, "time");
    min = Math.ceil(15)
    max = Math.floor(25)
    points = Math.floor(Math.random() * (max - min) + min);
    client.points.math(key, "+", points, "points");
    const levels = config.levels;
    const level1 = client.points.get(key, "level");
    level2 = parseInt(level1);
    const points2 = levels[level2];
    const points3 = parseInt(points2) - parseInt(client.points.get(key, "points"));
    const curLevel2 = 5 * (level1 ^ 2) + (50 * level1) + 100 - Math.abs(points3)-10;
    if (curLevel2 < 0) {
      level3 = level2 + 1;
      console.log("oof")
      message.reply(`You've leveled up to level **${level3}**! Ain't that lovely?`);
    } else {
      level3 = client.points.get(key, "level");
    };
    client.points.set(key, level3, "level");
  }
  // Command handler
  const prefix = client.db.settings.selectPrefix.pluck().get(message.guild.id);
  const prefixRegex = new RegExp(`^(<@!?${client.user.id}>|${prefix.replace(/[.*+?^${}()|[\]\\]/g, '\\$&')})\\s*`);

  if (prefixRegex.test(message.content)) {

    // Get mod channels
    let modChannelIds = message.client.db.settings.selectModChannelIds.pluck().get(message.guild.id) || [];
    if (typeof(modChannelIds) === 'string') modChannelIds = modChannelIds.split(' ');

    const [, match] = message.content.match(prefixRegex);
    const args = message.content.slice(match.length).trim().split(/ +/g);
    const cmd = args.shift().toLowerCase();
    let command = client.commands.get(cmd) || client.aliases.get(cmd); // If command not found, check aliases
    if (command && !disabledCommands.includes(command.name)) {

      // Check if mod channel
      if (modChannelIds.includes(message.channel.id)) {
        if (
          command.type != client.types.MOD || (command.type == client.types.MOD && 
          message.channel.permissionsFor(message.author).missing(command.userPermissions) != 0)
        ) {
          // Update points with messagePoints value
          if (pointTracking)
            client.db.users.updatePoints.run({ points: messagePoints }, message.author.id, message.guild.id);
          return; // Return early so Calypso doesn't respond
        }
      }

      // Check permissions
      const permission = command.checkPermissions(message);
      if (permission) {

        // Update points with commandPoints value
        if (pointTracking)
          client.db.users.updatePoints.run({ points: commandPoints }, message.author.id, message.guild.id);
        message.command = true; // Add flag for messageUpdate event
        return command.run(message, args); // Run command
      }
    } else if ( 
      (message.content === `<@${client.user.id}>` || message.content === `<@!${client.user.id}>`) &&
      message.channel.permissionsFor(message.guild.me).has(['SEND_MESSAGES', 'EMBED_LINKS']) &&
      !modChannelIds.includes(message.channel.id)
    ) {
      const embed = new MessageEmbed()
        .setTitle('Hi, I\'m MamothBot. Need help?')
        .setThumbnail('https://cdn.discordapp.com/attachments/762229292121587716/816625929962389544/mamoth112png.png')
        .setDescription(`You can see everything I can do by using the \`${prefix}help\` command.`)
        .addField('Invite Me', oneLine`
          You can add me to your server by clicking 
          [here](https://discord.com/api/oauth2/authorize?client_id=763699909727485962&permissions=8&redirect_uri=https%3A%2F%2Fdiscord.com%2F&scope=bot)!
        `)
        .addField('Support', oneLine`
          If you have questions, suggestions, or found a bug, please join the 
          [MamothBot Support Server](https://discord.gg/WxUfgsQn5y)!
        `)
        .setFooter('DM Mamoth112#8900 to speak directly with the developer!')
        .setColor(message.guild.me.displayHexColor);
      message.channel.send(embed);
    }
  }

  // Update points with messagePoints value
  if (pointTracking) client.db.users.updatePoints.run({ points: messagePoints }, message.author.id, message.guild.id);
};

