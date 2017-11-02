//use Jordan's component
//block user
//unfriend
import React, { Component } from 'react'
import { View, Text } from 'react-native'
import { connect } from 'react-redux'
import { bindActionCreators } from 'redux'

import key from '../../../../../sensitive.json'

class FriendProfile extends Component {
  constructor(props) {
    super(props);
  }
  
  componentDidMount() {
    //get user profile using this.props.navigation.state.params.userId
  }


  sendRequest(friendId) {
    axios.post('http://localhost:5000/api/add_friend', {
      friendId: friendId,
      // userId: this.screenProps,
      userId: 1
    })
    .then(({ data }) => {
      console.log('Success sending request', data);
    })
    .catch(err => {
      console.log('Request failed', err);
    })
  }
  
  deleteFriend(friendId) {
    axios.post(key.flask_server + 'api/remove_friend', {
      userId: this.screenProps,
      friendId: friendId
    })
  }

  blockFriend(friendId) {
    axios.post(key.flask_server + 'api/block_friend', {
      userId: this.screenProps,
      friendId: friendId
    })
  }

  render() {
    if (this.props.navigation.state.params.type === "result") {
      return (
        <View>
          <Text>This profile is private</Text>
        </View>
      )
    } else {
      return (
        <View>
          <Text>Friend's profile</Text> 
        </View>
      )
    }
  }
}

const mapStateToProps = (store) => {
  return {
    friends: store.Friends.friends
   }
 }

//  const userDispatch = (dispatch) => {
//    return {
//      actions: bindActionCreators(userActions, dispatch)
//    }
//  }

export default connect(mapStateToProps)(FriendProfile); 

// import React from 'react';
// import { View, Text, Image, StyleSheet, ScrollView, Dimensions, TouchableHighlight } from 'react-native';
// import { connect } from 'react-redux';
// import UserMap from './map.js';
// import Login from '../../auth/Login'

// const { width, height } =  Dimensions.get('window');
// const Profile = ( props ) => {
// 	console.log(props, 'profile props')
// 	if (props.profileInfo.Auth.name){
// 		let name = props.profileInfo.Auth.name;
// 		let email = props.profileInfo.Auth.email;
// 		let picture = props.profileInfo.Auth.picture;
// 		let id = props.profileInfo.Auth.id;
// 		let friendIcon = "https://cdn.iconscout.com/public/images/icon/premium/png-512/profile-group-friend-team-user-avatar-3d104201ce065c29-512x512.png"

// 		const viewFriends = () => {
//     	props.navigation.navigate("Friends")
// 		}
		
// 		const viewRequests = () => {
// 			props.navigation.navigate("FriendRequests")
// 		}

//   	const getFriends = () => {
//   		// get all friends, count them all, return count
//   		// put user id in get request params
//   		//'/api/get_all_friends'
//   	}

// 		return (
// 	    <ScrollView style={styles.profileContainer}>
// 	    	<View style={{flex:.3, backgroundColor: 'white', marginTop:10, justifyContent: 'center', alignItems: 'center', flexDirection: 'row'}}>
// 					<TouchableHighlight onPress={viewRequests} >
// 			      <Image source={{uri:friendIcon}} style={styles.friendIcon}/> 
// 			  	</TouchableHighlight>
// 	    		<Text style={styles.email}>
// 		      	{email}
// 		      </Text>
// 		      <TouchableHighlight onPress={viewFriends} >
// 			      <Image source={{uri:friendIcon}} style={styles.friendIcon}/> 
// 			    </TouchableHighlight>
// 	    	</View>
// 	    	<View style ={styles.profileDetails}>
// 	    		<View style={{flexDirection: 'row', flex: 1}}>
// 	    			<View style={{flexDirection: 'column', flex: 1}}>
// 	    				<View style={{flexDirection: 'row', alignItems: 'center'}}>
// 			    			<Image source={{uri:picture}} style={styles.profilePicture}/>
// 			    			<View style={{paddingLeft: 150, justifyContent: 'space-around', flexDirection: 'row'}}>
// 			    				<View style={{marginRight: 20}}>
// 				    				<Text> Photos </Text>
// 				    				<Text style={{textAlign: 'center'}}> 0 </Text>
// 				    			</View>
// 				    			<View>
// 					    			<Text> Friends </Text>
// 				    				<Text style={{textAlign: 'center'}}> 0 </Text>
// 				    			</View>
// 			    			</View>
// 			    		</View>
// 			    		<Text style={styles.profileName}> {name} </Text>
// 			    	</View>
// 		    		<View style={{ marginLeft: 180}}>
			    		
// 		      	</View>
// 		    	</View>
		      	
// 		      	<View style={{margin: 5}}>
// 		      		<Login />
// 		      	</View>
// 		    </View>






// 	      <View style={styles.profileMap}>
// 	      	<UserMap navigation={props.navigation}/>
// 	      </View>
// 	    </ScrollView> 
// 	  )
// 	}	else {
// 		  return (
// 		    <View>
// 		    </View> 
// 	  	)
// 	}
// }

// const mapStateToProps = (store) =>{
//   console.log(store, 'profile js state')
 
//   return {
//     profileInfo: store
//   }
// }

// const styles = StyleSheet.create({
// 	profileContainer: {
// 		flex: 1,
// 		flexDirection: 'row',
// 		backgroundColor: 'white'
// 	},
// 	profileDetails: {
// 		flex: 1,
// 		backgroundColor: 'skyblue'
// 	},
// 	profilePicture: {
// 		marginTop: 15,
// 		marginLeft: 30,
// 		marginBottom: 10,
// 		width: 50, 
// 		height: 50,
// 		justifyContent: 'center',
// 		alignItems: 'center',
// 		borderRadius: 20
// 	}, 
// 	friendIcon: {
// 		width: 40, 
// 		height: 40,
// 		borderRadius: 10,
// 		marginLeft: 30,
// 	},
// 	email: {
// 		paddingTop: 5,
// 		fontSize: 14,
// 		fontFamily: 'Verdana',
// 		fontWeight: 'bold',
// 		marginRight: 20,
// 	},
// 	profileName: {
// 		fontSize: 14,
// 		paddingBottom: 5,
// 		fontFamily: 'Verdana'
// 	},
// 	profileMap: {
// 		flex: 3,
// 		flexDirection: 'column',
// 		width: width,
// 	}
// })


// export default connect(mapStateToProps, null)(Profile);