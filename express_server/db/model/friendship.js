const Sequelize = require('sequelize');
const db = require('../config');

const User = require('./user');

const Friendships = db.define('friendship', {
  friendship_type: {
    type: Sequelize.STRING
  }
}, {
  timestamps: false
});

Friendships.belongsTo(User, {as: 'friend', foreignKey: 'friend_id'});
Friendships.belongsTo(User, {as: 'user', foreignKey: 'user_id'});

Friendships.removeAttribute('id');

module.exports = Friendships;