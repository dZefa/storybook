from flask import Flask, g, render_template, request, make_response
from flask_assets import Environment, Bundle
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.dialects import postgresql
from sqlalchemy import Integer, Table, Column, ForeignKey
from app import app, db, DropTable
from schema import Images, Users, friendships, messages, Comments, Likes
from config import app_config, basedir
from azure_get_tags import get_tags
from werkzeug.datastructures import ImmutableMultiDict
from pprint import pprint
import sqlalchemy_utils
from sqlalchemy_utils import drop_database
import json
import os
import unittest



@app.route('/')
def index():
  """This module renders main page"""
  return render_template('index.html')


#add image
@app.route('/api/add_image', methods=['POST'])
def add_photo():
  #request.args, .forms, .files, .values also exist. look them up in the docs
  request_data = dict(request.json)

  url = request_data["url"]
  parsed_url = url.encode('utf-8')

  #tags
  request_body = "{'url': '" + parsed_url + "'}"

  image_tags = get_tags(request_body)
  image_tags = []

  scn_code = '0'
  parsed_scn_code = scn_code.encode('utf-8')
  image_user_id = request_data["image_user_id"]
  parsed_image_user_id = int(image_user_id)
  
  #geolocation
  latitude = request_data["latitude"]
  parsed_latitude = int(latitude)

  longitude = request_data["longitude"]
  parsed_longitude = int(longitude)

  likes_count = 0
  parsed_likes_count = int(likes_count)

  image_caption = request_data["caption"]
  parsed_image_caption = image_caption.encode('utf-8')

  db.session.add(Images(parsed_url,parsed_scn_code, parsed_image_user_id, parsed_latitude, parsed_longitude, parsed_likes_count, parsed_image_caption, image_tags)) #replace later with actual values
  db.session.commit()
  resp = make_response('added successfully!', 201)
  return resp


#add user
@app.route('/api/add_user', methods=['POST'])
def add_user():
  #request.args, .forms, .files, .values also exist. look them up in the docs
  request_data = dict(request.json)

  name = request_data["name"]
  parsed_name = name.encode('utf-8')

  email = request_data["email"]
  parsed_email = email.encode('utf-8')

  profile_image_url = request_data["profile_image_url"]
  parsed_profile_image_url = profile_image_url.encode('utf-8')

  friends_count = request_data["friends_count"]
  parsed_friends_count = int(friends_count)

  # user_tags_array = 
  user_tags_array = ['']

  db.session.add(Users(parsed_name, parsed_email, parsed_profile_image_url, parsed_friends_count, user_tags_array)) #replace later with actual values
  db.session.commit()
  resp = make_response('added successfully!', 201)
  return resp


@app.route('/api/add_comment', methods=['POST'])
def add_comment():
  #request.args, .forms, .files, .values also exist. look them up in the docs
  request_data = dict(request.json)

  text = request_data["text"]
  parsed_text = text.encode('utf-8')
  comment_user_id = request_data["comment_user_id"]
  parsed_comment_user_id = int(comment_user_id)
  comment_image_id = request_data["comment_image_id"]
  parsed_comment_image_id = int(comment_image_id)

  db.session.add(Comments(parsed_text, parsed_comment_user_id, parsed_comment_image_id)) #replace later with actual values
  db.session.commit()
  resp = make_response('added successfully!', 201)
  return resp


@app.route('/api/add_like', methods=['POST'])
def add_like():
  #request.args, .forms, .files, .values also exist. look them up in the docs
  request_data = dict(request.json)

  like_user_id = request_data["like_user_id"]
  parsed_like_user_id = int(like_user_id)
  
  like_image_id = request_data["like_image_id"]
  parsed_like_image_id = int(like_image_id)

  db.session.add(Likes(parsed_like_user_id, parsed_like_image_id)) #replace later with actual values
  db.session.commit()
  resp = make_response('added successfully!', 201)
  return resp


@app.route('/api/get_all_locations', methods=['GET'])
def grab_all_locations():
  request_data = dict(request.args)
  get_all_locations_query = db.session.query(Images) #returns all images
  coords = []
  for i in get_all_locations_query:
    new_loc = {
      "latitude": i.latitude,
      "longitude": i.longitude
    }
    coords.append(new_loc)
  result = {}
  result["data"] = coords
  resp = make_response(json.dumps(result, sort_keys=True, separators=(',', ':')), 200)
  return resp

@app.route('/api/get_all_locations_for_user', methods=['GET'])
def get_all_locations_for_user():
  request_data = dict(request.args)
  get_all_locations_for_user_user_id = request_data["userId"][0]
  print(get_all_locations_for_user_user_id)
  parsed_get_all_locations_for_user_user_id = int(get_all_locations_for_user_user_id)
  get_all_locations_for_user_query = db.session.query(Images).filter(Images.image_user_id == parsed_get_all_locations_for_user_user_id) #returns all images
  coords = []
  for i in get_all_locations_for_user_query:
    new_loc = {
      "latitude": i.latitude,
      "longitude": i.longitude
    }
    coords.append(str(new_loc))
  result = {}
  result["data"] = coords
  resp = make_response(json.dumps(result, sort_keys=True, separators=(',', ':')), 200)
  return resp

@app.route('/api/get_user_info', methods=['GET'])
def get_user_info():
  request_data = dict(request.args)
  get_user_info_user_email = request_data["email"][0]
  parsed_get_user_info_user_email = str(get_user_info_user_email)

  get_user_info_query = db.session.query(Users).filter(Users.email == parsed_get_user_info_user_email)
  user_info = []
  for i in get_user_info_query:
    queried_user = {
      "userId": i.id,
      "name": i.name,
      "email": i.email,
      "profile_image_url": i.profile_image_url,
      "friends_count": i.friends_count
    }
    user_info.append(queried_user)
  result = {}
  result["data"] = user_info
  resp = make_response(json.dumps(result, sort_keys=True, separators=(',', ':')), 200)
  return resp

@app.route('/api/add_user_info', methods=['POST'])
def add_user_info():
  request_data = dict(request.json)
  add_user_info_user_name = request_data["name"]
  parsed_add_user_info_user_name = str(add_user_info_user_name)

  add_user_info_email = request_data["email"]
  parsed_add_user_info_email = str(add_user_info_email)

  add_user_info_profile_image_url = request_data["profile_image_url"]
  parsed_add_user_info_profile_image_url = str(add_user_info_profile_image_url)

  add_user_info_friends_count = 0
  parsed_add_user_info_friends_count = int(0)
  
  user_tags_array = []

  db.session.add(Users(parsed_add_user_info_user_name, parsed_add_user_info_email, parsed_add_user_info_profile_image_url, parsed_add_user_info_friends_count, user_tags_array))
  db.session.commit()
  new_user_id = db.session.query(Users).filter(Users.email == parsed_add_user_info_email)
  parsed_new_user_id = -1
  for i in new_user_id:
    parsed_new_user_id = i.id
  resp = make_response(json.dumps({"userId": parsed_new_user_id}), 201)
  return resp

@app.route('/api/get_imgs_by_loc', methods=['GET'])
def get_imgs_by_loc():
    print("grabbing photos by specific location...")
    request_data = dict(request.args)
    get_imgs_by_loc_latitude = request_data["latitude"][0]
    get_imgs_by_loc_latitude = float(get_imgs_by_loc_latitude)
    get_imgs_by_loc_longitude = request_data["longitude"][0]
    get_imgs_by_loc_longitude = float(get_imgs_by_loc_longitude)
    
    get_imgs_by_loc_query = db.session.query(Images).filter((Images.latitude > (get_imgs_by_loc_latitude - 0.002)) & (Images.latitude < (get_imgs_by_loc_latitude + 0.01)) & (Images.longitude > (get_imgs_by_loc_longitude - 0.01)) & (Images.longitude < (get_imgs_by_loc_longitude + 0.002)))
    all_images = []
    for i in get_imgs_by_loc_query:
      all_images.append({
        "image_user_id": i.image_user_id,
        "image_id": i.id,
        "imageUrl": i.image_url
      })
    result = {}
    result["data"] = all_images
    resp = make_response(json.dumps(result, sort_keys=True, separators=(',', ':')), 200)
    return resp


@app.route('/api/get_imgs_by_frs_at_loc', methods=['GET'])
def get_imgs_by_frs_at_loc():
    print("grabbing most recent photo from each friend within a 10 mile radius at OP's location...")
    request_data = dict(request.args)

    get_imgs_by_frs_at_loc_latitude = request_data["latitude"][0]
    parsed_get_imgs_by_frs_at_loc_latitude = float(get_imgs_by_frs_at_loc_latitude)
    
    get_imgs_by_frs_at_loc_longitude = request_data["longitude"][0]
    parsed_get_imgs_by_frs_at_loc_longitude = float(get_imgs_by_frs_at_loc_longitude)
    
    get_imgs_by_frs_at_loc_user_id = request_data["userId"][0]
    parsed_get_imgs_by_frs_at_loc_user_id = int(get_imgs_by_frs_at_loc_user_id)
    
    get_list_of_friends_query = db.session.execute("SELECT * FROM users RIGHT JOIN friendships ON users.id = friendships.relating_user_id WHERE id = " + str(parsed_get_imgs_by_frs_at_loc_user_id) + "AND friendship_type='friend'")

    list_of_photos = []
    for i in get_list_of_friends_query:
      print(i.related_user_id)
      parsed_user_id = int(i.related_user_id)
      most_recent_image_at_loc = Images.query.filter_by(image_user_id=parsed_user_id).filter((Images.latitude > (parsed_get_imgs_by_frs_at_loc_latitude - 0.01)) & (Images.latitude < (parsed_get_imgs_by_frs_at_loc_latitude + 0.01)) & (Images.longitude > (parsed_get_imgs_by_frs_at_loc_longitude - 0.001)) & (Images.longitude < (parsed_get_imgs_by_frs_at_loc_longitude + 0.001))).order_by(Images.id.desc()).first()
      if (most_recent_image_at_loc):
        # list_of_photos.append(most_recent_image_at_loc.image_url)
        list_of_photos.append({
          "image_user_id": most_recent_image_at_loc.image_user_id,
          "image_id": most_recent_image_at_loc.id,
          "imageUrl": most_recent_image_at_loc.image_url
        })
      print("list of photos...", list_of_photos)
    
    result = {}
    result["data"] = list_of_photos

    resp = make_response(json.dumps(result, sort_keys=True, separators=(',', ':')), 200)
    return resp   


@app.route('/api/get_all_friends', methods=['GET'])
def get_all_friends():
    print("grabbing list of user's friends...")
    request_data = dict(request.args)
    
    get_all_friends_user_id = request_data["userId"][0]
    parsed_get_all_friends_user_id = int(get_all_friends_user_id)
    
    get_all_relating_friends_query = db.session.execute('SELECT * FROM users RIGHT JOIN friendships ON users.id = friendships.relating_user_id WHERE id = ' + str(parsed_get_all_friends_user_id))
    get_all_related_friends_query = db.session.execute('SELECT * FROM users RIGHT JOIN friendships ON users.id = friendships.related_user_id WHERE id = ' + str(parsed_get_all_friends_user_id))
    
    list_of_friends = []
    for i in get_all_relating_friends_query:
      if i[len(i) - 1] == 'friend':
        relative_info_query = db.session.query(Users).filter(Users.id == i.related_user_id)
        for j in relative_info_query:
          temp = {
            "id": j.id,
            "name": j.name,
            "email": j.email,
            "profile_image_url": j.profile_image_url
          }
          list_of_friends.append(temp)

    for i in get_all_related_friends_query:
      if i[len(i) - 1] == 'friend':
        relative_info_query = db.session.query(Users).filter(Users.id == i.relating_user_id)
        for j in relative_info_query:
          temp = {
            "id": j.id,
            "name": j.name,
            "email": j.email,
            "profile_image_url": j.profile_image_url
          }
          list_of_friends.append(temp)

    result = {}
    result["data"] = list_of_friends
    resp = make_response(json.dumps(result), 200)
    return resp

@app.route('/api/get_friend_requests', methods=['GET'])
def get_friend_requests():
    print("grabbing all friend requests for specific user...")
    request_data = dict(request.args)
    get_friend_requests_user_id = request_data["userId"][0]
    parsed_get_friend_requests_user_id = int(get_friend_requests_user_id)

    get_friend_requests_query = db.session.execute('SELECT * FROM users RIGHT JOIN friendships ON users.id = friendships.relating_user_id WHERE id = ' + str(parsed_get_friend_requests_user_id))
    list_of_requests = []
    for i in get_friend_requests_query:
      if i[len(i) - 1] == 'pending':
        pending_friend_query = db.session.execute('SELECT * FROM users WHERE id = ' + str(i.related_user_id))
        for j in pending_friend_query:
          temp = {
            "id": j[0],
            "name": j[1],
            "email": j[2],
            "profile_image_url": j[3]
          }
          list_of_requests.append(temp)

    result = {}
    result["data"] = list_of_requests
    resp = make_response(json.dumps(result, sort_keys=True, separators=(',', ':')), 200)
    return resp

# get all friend requests using req.params.userId along with name and profile pic
  #DONE

@app.route('/api/add_friend', methods=['POST'])
def add_friend():
    request_data = dict(request.json)
    add_friend_relating_user_id = request_data["userId"]
    parsed_add_friend_relating_user_id = str(add_friend_relating_user_id)

    add_friend_related_user_id = request_data["friendId"]
    parsed_add_friend_related_user_id = str(add_friend_related_user_id)

    db.session.execute("insert into friendships (relating_user_id, related_user_id, friendship_type) values (" + parsed_add_friend_relating_user_id + ", " + parsed_add_friend_related_user_id + ", 'pending')")
    db.session.commit()

    resp = make_response('added successfully!', 201)
    return resp


@app.route('/api/accept_friend_request', methods=['POST'])
def accept_friend_request():
    print("accepting friend request...")
    request_data = dict(request.json)
    accept_friend_request_relating_user_id = request_data["userId"]
    parsed_accept_friend_request_relating_user_id = str(accept_friend_request_relating_user_id)

    accept_friend_request_related_user_id = request_data["friendId"]
    parsed_accept_friend_request_related_user_id = str(accept_friend_request_related_user_id)

    db.session.execute("UPDATE friendships SET friendship_type='friend' WHERE relating_user_id=" + parsed_accept_friend_request_related_user_id + " AND related_user_id=" + parsed_accept_friend_request_relating_user_id)
    db.session.commit()

    resp = make_response('modified successfully!', 201)
    return resp


# @app.route('/api/block_friend', methods=['POST'])
# def block_friend():
#     print("blocking friend...")
#     request_data = dict(request.json)
#     block_friend_relating_user_id = request_data["userId"]
#     parsed_block_friend_relating_user_id = str(block_friend_relating_user_id)

#     block_friend_related_user_id = request_data["friendId"]
#     parsed_block_friend_related_user_id = str(block_friend_related_user_id)

#     db.session.execute("UPDATE friendships SET friendship_type='blocked' WHERE relating_user_id=" + parsed_block_friend_relating_user_id + " AND related_user_id=" + parsed_block_friend_related_user_id)
#     db.session.commit()

#     resp = make_response('modified successfully!', 201)
#     return resp


@app.route('/api/remove_friend', methods=['POST'])
def remove_friend():
    print("removing friend...")
    request_data = dict(request.json)
    remove_friend_relating_user_id = request_data["userId"]
    parsed_remove_friend_relating_user_id = str(remove_friend_relating_user_id)

    remove_friend_related_user_id = request_data["friendId"]
    parsed_remove_friend_related_user_id = str(remove_friend_related_user_id)

    db.session.execute("DELETE FROM friendships WHERE relating_user_id=" + parsed_remove_friend_relating_user_id + " AND related_user_id=" + parsed_remove_friend_related_user_id)
    db.session.commit()

    db.session.execute("DELETE FROM friendships WHERE relating_user_id=" + parsed_remove_friend_related_user_id + " AND related_user_id=" + parsed_remove_friend_relating_user_id)
    db.session.commit()

    resp = make_response('removed successfully!', 201)
    return resp

@app.route('/api/get_convo', methods=['GET'])
def get_convo():
  print('getting conversation...')
  request_data = dict(request.args)
  get_convo_sender_id = request_data["senderId"][0]
  parsed_get_convo_sender_id = str(get_convo_sender_id)
  print(parsed_get_convo_sender_id)

  get_convo_recipient_id = request_data["recipientId"][0]
  parsed_get_convo_recipient_id = str(get_convo_recipient_id)
  print(parsed_get_convo_recipient_id)
  print("select * from messages where (sender_id=" + parsed_get_convo_sender_id + "and recipient_id=" + parsed_get_convo_recipient_id + ") OR (sender_id=" + parsed_get_convo_recipient_id + "and recipient_id=" + parsed_get_convo_sender_id + ")")

  convo_query = db.session.execute("select * from messages where (sender_id=" + parsed_get_convo_sender_id + "and recipient_id=" + parsed_get_convo_recipient_id + ") OR (sender_id=" + parsed_get_convo_recipient_id + "and recipient_id=" + parsed_get_convo_sender_id + ")")
  # most_recent_message_query_2 = db.session.execute("select * from messages where sender_id=" + parsed_get_convo_recipient_id + "and recipient_id=" + parsed_get_convo_sender_id + "ORDER BY recipient_id DESC")
  
  convo_array = []
  for i in convo_query:
    convo_array.append({
      "sender_id": i.sender_id,
      "recipient_id": i.recipient_id,
      "message": str(i.message)
    })

  result = {}
  result["data"] = convo_array
  resp = make_response(json.dumps(result, sort_keys=True, separators=(',', ':')), 200)
  return resp



@app.route('/api/get_last_message', methods=['GET'])
def get_last_message():
  print('getting most recent message...')
  request_data = dict(request.args)
  get_last_message_sender_id = request_data["senderId"][0]
  parsed_get_last_message_sender_id = str(get_last_message_sender_id)
  print(parsed_get_last_message_sender_id)

  get_last_message_recipient_id = request_data["recipientId"][0]
  parsed_get_last_message_recipient_id = str(get_last_message_recipient_id)
  print(parsed_get_last_message_recipient_id)
  # print("select * from messages where (sender_id=" + parsed_get_last_message_sender_id + "and recipient_id=" + parsed_get_last_message_recipient_id + ") OR (sender_id=" + parsed_get_last_message_recipient_id + "and recipient_id=" + parsed_get_last_message_sender_id + ")")
  # select * from messages where ((sender_id=1 and recipient_id=4) OR (sender_id=4 and recipient_id=1)) and date_created IN (SELECT max(date_created) FROM messages);

  last_message_query = db.session.execute("select * from messages where ((sender_id=" + parsed_get_last_message_sender_id + "and recipient_id=" + parsed_get_last_message_recipient_id + ") OR (sender_id=" + parsed_get_last_message_recipient_id + "and recipient_id=" + parsed_get_last_message_sender_id + ")) AND date_created IN (SELECT max(date_created) FROM messages)")
  # most_recent_message_query_2 = db.session.execute("select * from messages where sender_id=" + parsed_get_convo_recipient_id + "and recipient_id=" + parsed_get_convo_sender_id + "ORDER BY recipient_id DESC")
  
  result = {}
  for i in last_message_query:
      result["sender_id"]= i.sender_id
      result["recipient_id"]= i.recipient_id
      result["message"]= str(i.message)

  resp = make_response(json.dumps(result, sort_keys=True, separators=(',', ':')), 200)
  return resp



#get all likes for a specific image
@app.route('/api/get_all_likes_by_image', methods=['GET'])
def get_all_likes_by_image():
  print('getting all likes for specific image')
  request_data = dict(request.args)
  get_all_likes_image_id = request_data["imageId"][0]
  parsed_get_all_likes_image_id = str(get_all_likes_image_id)

  get_all_likes_by_image_query = db.session.execute('SELECT * FROM likes WHERE like_image_id = ' + parsed_get_all_likes_image_id)
  all_likes_array = []
  for i in get_all_likes_by_image_query:
    like_obj = {
      "user_id": i.like_user_id
    }
    all_likes_array.append(like_obj)
  
  result = {}
  result["data"] = all_likes_array
  resp = make_response(json.dumps(result, sort_keys=True, separators=(',', ':')), 200)
  return resp 

#get all images for a specific user
@app.route('/api/get_all_images_by_user', methods=['GET'])
def get_all_images_by_user():
  print('getting all images for specific user')
  request_data = dict(request.args)
  get_all_images_user_id = request_data["userId"][0]
  parsed_get_all_images_user_id = str(get_all_images_user_id)

  get_all_images_by_user_query = db.session.execute('SELECT * FROM images WHERE image_user_id = ' + parsed_get_all_images_user_id)
  all_images_array = []
  for i in get_all_images_by_user_query:
    image_obj = {
      "imageUrl": i.image_url,
      "imageId": i.id
    }
    all_images_array.append(image_obj)

  result = {}
  result["data"] = all_images_array
  resp = make_response(json.dumps(result, sort_keys=True, separators=(',', ':')), 200)
  return resp 

#getting all comments for a specific image. make this a join table with the users
@app.route('/api/get_all_comments_by_image', methods=['GET'])
def get_all_comments_by_image():
  print('getting all comments by image')
  request_data = dict(request.args)
  get_all_comments_image_id = request_data["imageId"][0]
  parsed_get_all_comments_image_id = str(get_all_comments_image_id)

  get_all_comments_by_image_query = db.session.execute('SELECT * FROM comments RIGHT JOIN users ON comment_user_id = users.id WHERE comment_image_id = ' + parsed_get_all_comments_image_id)
  all_comments_array = []
  for i in get_all_comments_by_image_query:
    comment_obj = {
      "comment": i[1],
      "userName": i[5],
      "profileImage": i[7]
    }
    all_comments_array.append(comment_obj)

  result = {}
  result["data"] = all_comments_array
  resp = make_response(json.dumps(result, sort_keys=True, separators=(',', ':')), 200)
  return resp


#retrieve all photos for specific user
@app.route('/api/get_all_photos_loc_by_user', methods=['GET'])
def get_all_photos_loc_by_user():
  print('getting all image locations by user')
  request_data = dict(request.args)
  get_all_images_by_user_id = request_data["userId"][0]
  parsed_get_all_images_by_user_id = str(get_all_images_by_user_id)
  
  get_all_images_by_user_query = db.session.execute('SELECT * FROM images WHERE image_user_id = ' + parsed_get_all_images_by_user_id)
  all_images_array = []
  for i in get_all_images_by_user_query:
    user_loc = {
      "longitude": i.longitude,
      "latitdue": i.latitude
    }
    all_images_array.append(user_loc)

  result = {}
  result["data"] = all_images_array
  resp = make_response(json.dumps(result, sort_keys=True, separators=(',', ':')), 200)
  return resp


#search friends
@app.route('/api/search', methods=['GET'])
def search():
  print('searching for user...')
  request_data = dict(request.args)
  search_user_name = request_data["userName"][0]
  parsed_search_user_name = str(search_user_name)
  
  search_user_name_query = db.session.execute("SELECT * FROM users WHERE name = " + parsed_search_user_name)

  result = {}
  for i in last_message_query:
      result["name"]= str(i.name)
      result["email"]= i.email
      result["profile_image_url"] = i.profile_image_url
      result["friends_count"] = i.friends_count

  resp = make_response(json.dumps(result, sort_keys=True, separators=(',', ':')), 200)
  return resp