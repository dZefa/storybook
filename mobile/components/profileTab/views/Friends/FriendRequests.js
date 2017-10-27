import React, { Component } from 'react'
import { View, Text, Image } from 'react-native'
import axios from 'axios'

import Request from './Request'
//need function to delete request 

class FriendRequests extends Component {
  constructor(props) {
    super(props);
    this.state = {
      requests: [], 
    }
  }
  
  acceptRequest(friendId) {
    axios.post('/acceptRequest', {
      friendId: friendId
    })
    .then(({ data }) => {
      this.setState({requests: this.state.requests.splice(indexOf(data), 1)});
    })
    .catch(err => 
      console.log('error accepting request', err)
    )
  }

  // deleteRequest(friendId) {
  //   axios.post('deleteRequest', {
  //     friendId: friendId
  //   })
  //   .then({
      
  //   })
  // }
  
  componentDidMount() {
    axios.get('/requests/' + this.props.UserId) 
    .then(({ data }) => {
      this.setState({requests: data})
    })
    .catch(err => {
      console.log('error getting friend requests', err); 
    })
  }

  render() {
    <View>
      {this.state.requests.map(request => {
        <Request 
          acceptRequest={this.acceptRequest.bind(this)}
          deleteRequest={this.deleteRequest.bind(this)}
          friend={request.friendId}
        />
      })}
    </View>
  }
}