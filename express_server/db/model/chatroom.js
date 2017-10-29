const Sequelize = require('sequelize');
const db = require('../config');
const User = require('./user');

const Chatroom = db.define('chatroom', {
}, {
  timestamps: false
});

Chatroom.belongsTo(User, {as: 'sender', foreignKey: 'chatroom_sender'});
Chatroom.belongsTo(User, {as: 'recipient', foreignKey: 'chatroom_recipient'});

module.exports = Chatroom;