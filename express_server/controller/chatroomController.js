const Chatroom = require('../db/model/chatroom');
const User = require('../db/model/user');

const Sequelize = require('sequelize');
const Op = Sequelize.Op;

module.exports = {
  addChatroom: (req, res) => {
    Chatroom.create({
      chatroom_sender: req.body.userId,
      chatroom_recipient: req.body.friendId
    })
      .then(data => {
        res.status(201).send(data);
      })
      .catch(err => {
        res.status(400).send(err);
      });
  },
  getChatroom: (req, res) => {
    Chatroom.findAll({
      where: {
        [Op.or]: [{
          chatroom_sender: req.params.userId
        }, {
          chatroom_recipient: req.params.userId
        }]
      },
      include: [{
        model: User,
        as: 'sender',
        attributes: ['name']
      }, {
        model: User,
        as: 'recipient',
        attributes: ['name']
      }]
    })
      .then(data => {
        res.status(200).send(data);
      })
      .catch(err => {
        console.log('Error finding chatrooms: ', err);
        res.status(400).send(err);
      });
  }
};
