const express = require('express');
const parser = require('body-parser');
const path = require('path');
const cors = require('cors');

const routes = require('./routes');
const User = require('./db/model/user');
const Chatroom = require('./db/model/chatroom');
const Messages = require('./db/model/messages');
const Friendships = require('./db/model/friendship');
const Image = require('./db/model/images');

const PORT = process.env.PORT || 1337;

const app = express();

app.use(parser.json());
app.use(parser.urlencoded({extended: true}));
app.use(cors());
app.use('/api', routes);

app.get('/*', (req, res) => {
  res.send(404, 'Server Only');
});

User.sync()
  .then(() => {
    Chatroom.sync({force: true});
    Friendships.sync({force: true});
    Image.sync({force: true});
  })
  .then(() => {
    Messages.sync({force: true});
  })
  .then(() => {
    app.listen(PORT, () => {
      console.log('listening on port: ', PORT);
    });
  })
  .catch(err => {
    console.log('Error syncing db: ', err);
  });
