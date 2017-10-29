const router = require('express').Router();

const userCtrlr = require('./controller/userController');
const imgCtrlr = require('./controller/imgController');
const chatCtrlr = require('./controller/chatroomController');
const frndCtrlr = require('./controller/friendController');

// User routes
router.route('/user')
  .post(userCtrlr.addUser);

router.route('/user/:userId')
  .get(userCtrlr.getUser)
  .put(userCtrlr.updateUser);

// Image routes
router.route('/image')
  .post(imgCtrlr.addImg);

router.route('/image/:userId')
  .get(imgCtrlr.allImgLocForUser);

router.route('/image/:long&&:lat')
  .get(imgCtrlr.imgsByLoc);

// Chatroom routes
router.route('/chat')
  .post(chatCtrlr.addChatroom);

router.route('/chat/:userId')
  .get(chatCtrlr.getChatroom);

// Friends routes
router.route('/friend/request')
  .post(frndCtrlr.sendRequest)
  .put(frndCtrlr.acceptRequest);

router.route('/friend/get/:userId')
  .get(frndCtrlr.getList);

router.route('/friend/request/:userId')
  .get(frndCtrlr.getRequest);

module.exports = router;