const { MessageEmbed } = require('discord.js');
const { verify } = require('../utils/emojis.json');
const { stripIndent } = require('common-tags');
const Tickets = require("../utils/tickets.js")

module.exports = async (client, messageReaction, user) => {

  if (client.user === user) return;

  const { message, emoji} = messageReaction;

  // Ticket
  if (emoji.name === "📑") {
    let type = null;
    const member = message.guild.members.cache.get(user.id);
    const { support_Id_ban: support_Id_ban, support_Id_billing: support_Id_billing, support_Id_bug: support_Id_bug, support_Id_question: support_Id_question, support_Id_request: support_Id_request, support_Id_suggest: support_Id_suggest, support_Id_support: support_Id_support, support_Id_ticket: support_Id_ticket } =
      client.db.settings.listSupportIds.get(message.guild.id);
    if (!support_Id_ban == null || !support_Id_ban == 0 && message.id == support_Id_ban) {
      type = "ban";
      const banMessage = message.channel.messages.fetch(support_Id_ban, cache = true, force = true);
    } else if (!support_Id_billing == null || !support_Id_billing == 0 && message.id == support_Id_billing) {
      type = "billing";
      const billingMessage = message.channel.messages.fetch(support_Id_billing, cache = true, force = true);
    } else if (!support_Id_bug == null || !support_Id_bug == 0 && message.id == support_Id_bug) {
      type = "bug";
      const bugMessage = message.channel.messages.fetch(support_Id_bug, cache = true, force = true);
    } else if (!support_Id_question == null || !support_Id_question == 0 && message.id == support_Id_question) {
      type = "question";
      const questionMessage = message.channel.messages.fetch(support_Id_question, cache = true, force = true);
    } else if (!support_Id_request == null || !support_Id_request == 0 && message.id == support_Id_request) {
      type = "request";
      const requestMessage = message.channel.messages.fetch(support_Id_request, cache = true, force = true);
    } else if (!support_Id_suggest == null || !support_Id_suggest == 0 && message.id == support_Id_suggest) {
      type = "suggest";
      const suggestMessage = message.channel.messages.fetch(support_Id_suggest, cache = true, force = true);
    } else if (!support_Id_support == null || !support_Id_support == 0 && message.id == support_Id_support) {
      type = "support";
      const supportMessage = message.channel.messages.fetch(support_Id_support, cache = true, force = true);
    } else if (!support_Id_ticket == null || !support_Id_ticket == 0 && message.id == support_Id_ticket) {
      type = "generic ticket";
      const ticketMessage = message.channel.messages.fetch(support_Id_ticket, cache = true, force = true);
    };
    const msg = await message.channel.messages.fetch(message.id);
    msg.reactions.resolve("📑").users.remove(user.id);
    Tickets.create(user, type, message)
  }
  // Verification
  if (emoji.id === verify.split(':')[2].slice(0, -1)) {
    const { verification_role_id: verificationRoleId, verification_message_id: verificationMessageId } =
      client.db.settings.selectVerification.get(message.guild.id);
    const verificationRole = message.guild.roles.cache.get(verificationRoleId);

    if (!verificationRole || message.id != verificationMessageId) return;
    const msg = await message.channel.messages.fetch(verificationMessageId);
    msg.reactions.resolve(verify.split(':')[2].slice(0, -1)).users.remove(user.id);


    const member = message.guild.members.cache.get(user.id);
    if (!member.roles.cache.has(verificationRole)) {
      try {
        await member.roles.add(verificationRole);
      } catch (err) {
        return client.sendSystemErrorMessage(member.guild, 'verification',
          stripIndent`Unable to assign verification role,` +
          'please check the role hierarchy and ensure I have the Manage Roles permission'
          , err.message);
      }
    }
  }

  // Starboard
  if (emoji.name === '⭐' && message.author != user) {
    const starboardChannelId = client.db.settings.selectStarboardChannelId.pluck().get(message.guild.id);
    const starboardChannel = message.guild.channels.cache.get(starboardChannelId);
    if (
      !starboardChannel ||
      !starboardChannel.viewable ||
      !starboardChannel.permissionsFor(message.guild.me).has(['SEND_MESSAGES', 'EMBED_LINKS']) ||
      message.channel === starboardChannel
    ) return;

    const emojis = ['⭐', '🌟', '✨', '💫', '☄️'];
    const messages = await starboardChannel.messages.fetch({ limit: 100 });
    const starred = messages.find(m => {
      return emojis.some(e => {
        return m.content.startsWith(e) &&
          m.embeds[0] &&
          m.embeds[0].footer &&
          m.embeds[0].footer.text == message.id;
      });
    });

    // If message already in starboard
    if (starred) {
      const starCount = parseInt(starred.content.split(' ')[1].slice(2)) + 1;

      // Determine emoji type
      let emojiType;
      if (starCount > 20) emojiType = emojis[4];
      else if (starCount > 15) emojiType = emojis[3];
      else if (starCount > 10) emojiType = emojis[2];
      else if (starCount > 5) emojiType = emojis[1];
      else emojiType = emojis[0];

      const starMessage = await starboardChannel.messages.fetch(starred.id);
      await starMessage.edit(`${emojiType} **${starCount}  |**  ${message.channel}`)
        .catch(err => client.logger.error(err.stack));

      // New starred message
    } else {

      // Check for attachment image
      let image = '';
      const attachment = message.attachments.array()[0];
      if (attachment && attachment.url) {
        const extension = attachment.url.split('.').pop();
        if (/(jpg|jpeg|png|gif)/gi.test(extension)) image = attachment.url;
      }

      // Check for url
      if (!image && message.embeds[0] && message.embeds[0].url) {
        const extension = message.embeds[0].url.split('.').pop();
        if (/(jpg|jpeg|png|gif)/gi.test(extension)) image = message.embeds[0].url;
      }

      if (!message.content && !image) return;

      const embed = new MessageEmbed()
        .setAuthor(message.author.tag, message.author.displayAvatarURL({ dynamic: true }))
        .setDescription(message.content)
        .addField('Original', `[Jump!](${message.url})`)
        .setImage(image)
        .setTimestamp()
        .setFooter(message.id)
        .setColor('#ffac33');
      await starboardChannel.send(`⭐ **1  |**  ${message.channel}`, embed);
    }
  }
};