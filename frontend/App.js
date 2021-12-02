import React, { useState } from 'react';
import { StyleSheet, View, Button, TextInput, ActivityIndicator } from 'react-native';
import * as DocumentPicker from 'expo-document-picker';
import Header from './header';
import Logo from './components/logo';
import Secondary from './secondary';
import faker from 'faker';

export default function App() {
  const [file, setFile] = useState(null);
  const [fileStatus, setFileStatus] = useState('Complete');
  const [text, onChangeText] = useState('');
  const [outputFile, setOututFile] = useState('');
<<<<<<< HEAD
  //Change hashcode for every new call
  const hashcode = faker.random.alphaNumeric(9);
=======
  const hashcode = 'as01ass81';
>>>>>>> 263f32cb5f1014b18bf538c3b7475add1308da32


  //Main python file upload
  const pickFile = async () => {
    let result = await DocumentPicker.getDocumentAsync({
      allowsEditing: false,
      quality: 1,
    });
    // console.log(result);

    if (result.type === 'success') {
      // console.log(result.uri)

      //Source code upload
      fetch(
<<<<<<< HEAD
        `http://127.0.0.1:5000/upload-source-code/${hashcode}`,
=======
        'http://127.0.0.1:5000/upload-source-code/as01ass81',
>>>>>>> 263f32cb5f1014b18bf538c3b7475add1308da32
        {
          body: result.file,
          method: "POST",
          mode: 'no-cors',
          headers: {
            'Content-Type': 'text/plain'
          }
        }
      )
<<<<<<< HEAD
=======
      // .then((response) => response.json())
      // .catch((error) => {
      //   console.error(error);
      // })
>>>>>>> 263f32cb5f1014b18bf538c3b7475add1308da32
      .then((responseData) => {
        setFile(result.uri)
        console.log("Source code success " + result.file + ". Response = "  + responseData)
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
      // console.log(result.uri)

      //Input file upload
      fetch(
        `http://127.0.0.1:5000/upload-input/${hashcode}`,
        {
          body: result.file,
          method: "POST",
          headers: {
            'Content-Type': 'text/plain'
          }
        }
      )
<<<<<<< HEAD
=======
      // .then((response) => response.json())
      // .catch((error) => {
      //   console.error(error);
      // })
>>>>>>> 263f32cb5f1014b18bf538c3b7475add1308da32
      .then((responseData) => {
        console.log("Input file success " + result.file + ". Response = "  + responseData)
      }).catch((error) => console.error(error));

    }
  };


  //Dependency upload
  const addDependencies = async () => {
    fetch(
        `http://127.0.0.1:5000/add-dependecies/${hashcode}`,
        {
          body: text,
          method: "POST",
          headers: {
            'Content-Type': 'application/json'
          }
        }
      )
<<<<<<< HEAD
=======
      // .then((response) => response.json())
      // .catch((error) => {
      //   console.error(error);
      // })
>>>>>>> 263f32cb5f1014b18bf538c3b7475add1308da32
      .then((responseData) => {
        console.log("Dependency Success")
      }).catch((error) => console.error(error));
  };

  //Execute File
  const executeFile = async () => {
    fetch(
        `http://127.0.0.1:5000/execute/${hashcode}`,
        {
          method: "POST"
        }
      )
<<<<<<< HEAD
=======
      // .then((response) => response.json())
      // .catch((error) => {
      //   console.error(error);
      // })
>>>>>>> 263f32cb5f1014b18bf538c3b7475add1308da32
      .then((responseData) => {
        console.log("Execute success. Response data = " + responseData)
      }).catch((error) => console.error(error));

      //To run loading circle which only runs on null value
      setFileStatus(null);


      //Check execution
      while(true) {
          fetch(
          `http://127.0.0.1:5000/poll/${hashcode}`,
          {
            method: "GET"
          }
        )
<<<<<<< HEAD
=======
        // .then((response) => response.json())
        // .catch((error) => {
        //   console.error(error);
        // })
>>>>>>> 263f32cb5f1014b18bf538c3b7475add1308da32
        .then((responseData) => {
          if(responseData.status === 'SUCCESS')  {
            setFileStatus('Complete');
            setOututFile(responseData.url);
<<<<<<< HEAD
            console.log("File executed " + responseData.url)
            return;
          }
          console.log("Execution in progress " + responseData)
=======
            setFileStatus(null);
            return;
          }
          console.log("Success " + responseData)
>>>>>>> 263f32cb5f1014b18bf538c3b7475add1308da32
        }).catch((error) => console.error(error));
    }
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
      {<Secondary>Output can be downloaded from this url - </Secondary> && outputFile}
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
