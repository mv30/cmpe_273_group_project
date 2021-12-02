import React, { useState } from 'react';
import { StyleSheet, View, Button, TextInput, ActivityIndicator } from 'react-native';
import * as DocumentPicker from 'expo-document-picker';
import Header from './header';
import Logo from './components/logo';
import Secondary from './secondary';

export default function App() {
  const [file, setFile] = useState(null);
  const [fileStatus, setFileStatus] = useState('Complete');
  const [text, onChangeText] = useState('');

  //Main python file upload
  const pickFile = async () => {
    let result = await DocumentPicker.getDocumentAsync({
      allowsEditing: false,
      quality: 1,
    });
    // console.log(result);

    if (result.type === 'success') {
      console.log(result.uri)
      var form = new FormData();
      form.append('pythonFile',result.file);

      //Source code upload
      fetch(
        'http://127.0.0.1:5000/upload-source-code/as01ass8123asd',
        {
          body: form,
          method: "POST",
          headers: {
            'Content-Type': 'application/octet-stream'
          }
        }
      ).then((response) => response.json())
      .catch((error) => {
        console.error(error);
      })
      .then((responseData) => {
        setFile(result.uri)
        console.log("Success " + responseData)
      }).catch((error) => console.error(error));

    }
  };

  //Input file upload
  const pickHelpingFile = async () => {
    let result = await DocumentPicker.getDocumentAsync({
      allowsEditing: false,
      quality: 1,
    });
    // console.log(result);

    if (result.type === 'success') {
      console.log(result.uri)

      //Input file upload
      fetch(
        'http://127.0.0.1:5000/upload-input/as01ass8123asd',
        {
          body: result.file,
          method: "POST",
          headers: {
            'Content-Type': 'text/plain'
          }
        }
      ).then((response) => response.json())
      .catch((error) => {
        console.error(error);
      })
      .then((responseData) => {
        console.log("Success " + responseData)
      }).catch((error) => console.error(error));

    }
  };


  //Dependency upload
  const addDependencies = async () => {
    fetch(
        'http://127.0.0.1:5000/add-dependecies/zzsxa213987asda',
        {
          body: text,
          method: "POST",
          headers: {
            'Content-Type': 'application/json'
          }
        }
      ).then((response) => response.json())
      .catch((error) => {
        console.error(error);
      })
      .then((responseData) => {
        console.log("Success " + responseData)
      }).catch((error) => console.error(error));
  };

  //Execute File
  const executeFile = async () => {
    fetch(
        'http://127.0.0.1:5000/execute/helloworld',
        {
          method: "POST"
        }
      ).then((response) => response.json())
      .catch((error) => {
        console.error(error);
      })
      .then((responseData) => {
        console.log("Success " + responseData)
      }).catch((error) => console.error(error));

      setFileStatus(null);


      //Check execution
      fetch(
        'http://127.0.0.1:5000/poll/as01ass8123asd',
        {
          method: "GET"
        }
      ).then((response) => response.json())
      .catch((error) => {
        console.error(error);
      })
      .then((responseData) => {
        if(responseData.status === 'SUCCESS')  {
          setFileStatus('Complete');
        }
        console.log("Success " + responseData)
      }).catch((error) => console.error(error));
  };



  return (
    <View style={{ flex: 1, alignItems: 'center', justifyContent: 'center' }}>
      <Logo/>
      <Header> Run Python file on server. </Header> <br/><br/><br/>
      <Button title="Pick python file(.py) from storage" onPress={pickFile} /> <br/><br/><br/>
      <Button title="Pick optional supporting input file" onPress={pickHelpingFile} /> <br/><br/><br/>
      <Secondary>Add dependencies in json format</Secondary>
      <TextInput style={styles.input} onChangeText={onChangeText} value={text} /> <br/><br/><br/>
      {file && <Header>Your file is being uploaded and it will execute on the server.</Header> && <br/> && <br/> && <br/>}<br/><br/><br/>
      <Button title="Execute Python File" onPress={addDependencies && executeFile}></Button>
      {!fileStatus && <ActivityIndicator size="large" color="#0000ff" />}
    </View>
  );
}

const styles = StyleSheet.create({
  container: {
    flex: 1,
    backgroundColor: '#fff',
    alignItems: 'center',
    justifyContent: 'center',
  },
  input: {
    height: 40,
    margin: 12,
    borderWidth: 1,
    padding: 10,
  },
});
