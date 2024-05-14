import Ionicons from '@expo/vector-icons/Ionicons';
import { StyleSheet, Image, Platform, TextInput, View, Pressable, Alert, Text } from 'react-native';

import ParallaxScrollView from '@/components/ParallaxScrollView';
import React, { useEffect, useState } from 'react';

export default function TabTwoScreen() {
  const [loginStatus, setLoginStatus] = useState(false);
  const [email, setEmail] =  useState("");
  const [password,setPassword] =  useState("");
  const [contents, setContents] = useState<Array<any>>([]);
  const [favorites, setFavorites] = useState<Array<any>>([]);

  useEffect(() => {
    fetch('http://10.0.2.2:5000/api/contents')
      .then((response) => response.json())
      .then((json) => {
        setContents(json.contents);
      })
      .catch((error) => {
        console.error(error);
      });
    if (email !== "" && loginStatus) {
      console.log(email)
      fetch('http://10.0.2.2:5000/api/favorites', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({
          email
        }),
      })
        .then((response) => response.json())
        .then((json) => {
          console.log(contents)
          setFavorites(json.favorites.map((item:any) => {
            const content = contents.find((c) => c.id === item.content_id);
            return {
              content_id: item.content_id,
              title: content.title
            };
          }));
        })
        .catch((error) => {
          // console.error(error);
        });
    }
  }, [loginStatus]);

  return (
    <ParallaxScrollView
      headerBackgroundColor={{ light: '#D0D0D0', dark: '#353636' }}
      headerImage={<Ionicons size={310} name="person" style={styles.headerImage} />}>
      { !loginStatus ? <View>
        <Text style={styles.title}>Login</Text>
      <View style={styles.inputView}>
            <TextInput style={styles.input} placeholder='EMAIL' value={email} onChangeText={setEmail} autoCorrect={false}
        autoCapitalize='none' />
            <TextInput style={styles.input} placeholder='PASSWORD' secureTextEntry value={password} onChangeText={setPassword} autoCorrect={false}
        autoCapitalize='none'/>
      </View>
      <View style={styles.buttonView}>
          <Pressable style={styles.button} onPress={() => {
            if(email === "" || password === ""){
              Alert.alert("Please fill all the fields");
            } else {
              fetch('http://10.0.2.2:5000/api/login', {
                method: 'POST',
                headers: {
                  'Content-Type': 'application/json',
                },
                body: JSON.stringify({
                  email,
                  password,
                }),
              })
                .then((response) => response.text())
                .then((data) => {
                  if (data === "Login success") {
                    setLoginStatus(true);
                  } else {
                    setLoginStatus(false);
                  }
                })
                .catch((error) => {
                  console.log(error);
                });
            }
          }}>
              <Text style={styles.buttonText}>LOGIN</Text>
          </Pressable>
      </View>
      </View>: <View>
          <Text style={styles.title}>My Favorite</Text>
          {favorites.map((item, index) => {
            return (
              <View style={styles.card} key={index}>
                <Text style={styles.title}>{item.title}</Text>
              </View>
            );
          })}
        </View>}
    </ParallaxScrollView>
  );
}

const styles = StyleSheet.create({
  card: {
    backgroundColor: '#fff',
    borderRadius: 10,
    padding: 20,
    margin: 20,
    alignItems: 'center',
    borderColor: '#000',
    borderWidth: 1,
  },
  title: {
    fontSize: 20,
    fontWeight: 'bold',
  },
  headerImage: {
    color: '#808080',
    bottom: -90,
    left: -35,
    position: 'absolute',
  },
  titleContainer: {
    flexDirection: 'row',
    gap: 8,
  },
  inputView : {
    gap : 15,
    width : "100%",
    paddingHorizontal : 40,
    marginBottom  :5
  },
  input : {
    height : 50,
    paddingHorizontal : 20,
    borderColor : "red",
    borderWidth : 1,
    borderRadius: 7
  },
  button : {
    backgroundColor : "red",
    height : 45,
    borderColor : "gray",
    borderWidth  : 1,
    borderRadius : 5,
    alignItems : "center",
    justifyContent : "center"
  },
  buttonText : {
    color : "white"  ,
    fontSize: 18,
    fontWeight : "bold"
  },
  buttonView :{
    width :"100%",
    paddingHorizontal : 50
  },
});
