import { Image, StyleSheet, View, Text } from 'react-native';

import ParallaxScrollView from '@/components/ParallaxScrollView';
import { useEffect, useState } from 'react';

export default function HomeScreen() {
  const [content, setContent] = useState<Array<any>>([]);

  useEffect(() => {
    fetch('http://10.0.2.2:5000/api/contents')
      .then((response) => response.json())
      .then((json) => {
        setContent(json.contents)
      }).catch((error) => {
        console.error(error)
      });
  }, [])

  return (
    <ParallaxScrollView
      headerBackgroundColor={{ light: '#A1CEDC', dark: '#1D3D47' }}
      headerImage={
        <Image
          source={require('@/assets/images/partial-react-logo.png')}
          style={styles.reactLogo}
        />
      }>
        {
          content.map((item, index) => {
            return (
              <View style={styles.card} key={index}>
                <Text style={styles.title}>{item.title}</Text>
              </View>
            )
          })
        }
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
  reactLogo: {
    height: 178,
    width: 290,
    bottom: 0,
    left: 0,
    position: 'absolute',
  },
});
