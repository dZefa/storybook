const User = require('../db/model/user');

module.exports = {
  addUser: (req, res) => {
    User.findOrCreate({
      where: {
        email: req.body.email
      }
    })
      .spread((user, created) => {
        if(created) {
          User.update({
            name: req.body.name,
            profile_image_url: req.body.url,
            friends_count: 0,
            user_tags_array: [0],
            chatroom_array: [0]
          }, {
            where: {
              email: req.body.email
            }
          })
            .then(data => {
              res.status(201).send(data);
            })
            .catch(err => {
              console.log('Error addingUser: ', err);
              res.status(400).send(err);
            })
        } else {
          res.status(200).send(user);
        }
      })
      .catch(err => {
        res.status(400).send(err);
      });
  },
  getUser: (req, res) => {
    User.findOne({
      where: {
        id: req.params.userId
      }
    })
      .then(data => {
        res.status(200).send(data);
      })
      .catch(err => {
        res.status(400).send(err);
      })
  },
  updateUser: (req, res) => {
    User.update({
      name: req.body.name,
      email: req.body.email,
      profile_image_url: req.body.url
    }, {
      where: {
        id: req.params.userId
      }
    })
      .then(data => {
        res.status(200).send(data);
      })
      .catch(err => {
        res.status(400).send(err);
      });
  }
};