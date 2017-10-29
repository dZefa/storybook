const Sequelize = require('sequelize');
const db = require('../config');

const User = require('./user');

const Image = db.define('image', {
  image_url: {
    type: Sequelize.STRING,
    allowNull: false
  },
  longitude: {
    type: Sequelize.INTEGER,
    allowNull: false
  },
  latitude: {
    type: Sequelize.INTEGER,
    allowNull: false
  },
  likes_count: {
    type: Sequelize.INTEGER
  },
  caption: {
    type: Sequelize.STRING
  },
  image_tags_array: {
    type: Sequelize.ARRAY({type: Sequelize.STRING})
  }
});

Image.belongsTo(User, {foreignKey: 'image_user_id', allowNull: false, onDelete: 'CASCADE'});
User.hasMany(Image, {foreignKey: 'image_user_id', allowNull: false, onDelete: 'CASCADE'});

module.exports = Image;