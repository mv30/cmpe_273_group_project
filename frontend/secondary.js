import React from 'react'
import { StyleSheet } from 'react-native'
import { Text } from 'react-native-paper'
import { theme } from './core'

export default function Secondary(props) {
  return <Text style={styles.header} {...props} />
}

const styles = StyleSheet.create({
  header: {
    fontSize: 21,
    color: theme.colors.secondary,
    fontWeight: 'bold',
    paddingVertical: 12,
  },
})
