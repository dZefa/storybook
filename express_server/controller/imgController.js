const Image = require('../db/model/images');

const Sequelize = require('sequelize');
const Op = Sequelize.Op;

module.exports = {
  addImg: (req, res) => {
    Image.create({
      image_url: req.body.url,
      longitude: req.body.long,
      latitude: req.body.lat,
      likes_count: 0,
      caption: req.body.caption,
      image_tags_array: []
    })
      .then(data => {
        res.status(201).send(data);
      })
      .catch(err => {
        console.log('Error posting Image: ', err);
        res.status(400).send(err);
      });
  },
  allImgLocForUser: (req, res) => {
    Image.findAll({
      where: {
        image_user_id: req.params.id
      },
      attributes: ['longitude', 'latitude']
    })
      .then(data => {
        res.status(200).send(data);
      })
      .catch(err => {
        console.log('Error retrieving Long/Lat: ', err);
        res.status(400).send(err)
      });
  },
  imgsByLoc: (req, res) => {
    Image.findAll({
      where: {
        longitude: {
          [Op.contains]: [req.params.long - 0.02, req.params.long + 0.02]
        },
        latitude: {
          [Op.contains]: [req.params.lat - 0.02, req.params.lat + 0.02]
        }
      }
    })
      .then(data => {
        res.status(200).send(data);
      })
      .catch(err => {
        console.log('Error finding Imgs by loc: ', err);
      });
  }
}