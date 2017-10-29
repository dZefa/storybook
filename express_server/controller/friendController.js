const Friendship = require('../db/model/friendship');
const User = require('../db/model/user');

const Sequelize = require('sequelize');
const Op = Sequelize.Op;

module.exports = {
  getList: (req, res) => {
    Friendship.findAll({
      where: {
        user_id: req.params.userId,
        friendship_type: 'friend'
      },
      include: [{
        model: User,
        as: 'friend',
        attributes: ['name', 'profile_image_url']
      }]
    })
      .then(data => {
        res.status(200).send(data);
      })
      .catch(err => {
        console.log('Error getting friendslist: ', )
        res.status(400).send(err);
      })
  },
  sendRequest: (req, res) => {
    Friendship.create({
      user_id: req.body.userId,
      friend_id: req.body.friendId,
      friendship_type: 'pending'
    })
      .then(data => {
        res.status(201).send(data);
        Friendship.create({
          user_id: req.body.friendId,
          friend_id: req.body.userId,
          friendship_type: 'pending'
        })
      })
      .catch(err => {
        console.log('Error sending friend request: ', err);
        res.status(400).send(err);
      })
  },
  getRequest: (req, res) => {
    Friendship.findAll({
      where: {
        user_id: req.params.userId,
        friendship_type: 'pending'
      },
      include: [{
        model: User,
        as: 'friend',
        attributes: ['name', 'profile_image_url']
      }]
    })
      .then(data => {
        res.status(200).send(data);
      })
      .catch(err => {
        console.log('Error finding friend requests: ', err);
        res.status(400).send(err);
      });
  },
  acceptRequest: (req, res) => {
    Friendship.update({
      friendship_type: 'friend'
    }, {
      where: {
        user_id: req.body.userId,
        friend_id: req.body.friendId
      }
    })
      .then(data => {
        res.status(200).send(data);
        Friendship.update({
          friendship_type: 'friend'
        }, {
          where: {
            user_id: req.body.friendId,
            friend_id: req.body.userId
          }
        })
      })
      .catch(err => {
        console.log('Error accepting friend request: ', err);
        res.status(400).send(err);
      });
  },
}

// get list of friends (names)
// send request
// get request
// accept request
// delete request
// block user
// search friend
