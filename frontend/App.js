import React, { useState } from 'react';
import { StyleSheet, View, Button, TextInput, ActivityIndicator } from 'react-native';
import * as DocumentPicker from 'expo-document-picker';
import Header from './header';
import Logo from './components/logo';
import Secondary from './secondary';
import faker from 'faker';

export default function App() {

  const [file, setFile] = useState(null);
  const [text, onChangeText] = useState('');
  const [outputFile, setOututFile] = useState('');
  //Change hashcode for every new call
  const hashcode = faker.random.alphaNumeric(9);
  // const [hashcode, setHashCode] = useState('nuiuvenui');
  const [fileStatus, setFileStatus] = useState('Complete');
  console.log(hashcode);

  //Main python file upload
  const pickFile = async () => {
    console.log(hashcode);
    let result = await DocumentPicker.getDocumentAsync({
      allowsEditing: false,
      quality: 1,
    });
    // console.log(result);

    if (result.type === 'success') {
      // console.log(result.uri)

      //Source code upload
      fetch(
        `http://127.0.0.1:5000/upload-source-code/${hashcode}`,
        {
          body: result.file,
          method: "POST",
          headers: {
            'Content-Type': 'text/plain'
          }
        }
      )
      .then((responseData) => {
        setFile(result.uri)
        console.log("Source code success " + result.file + ". Response = "  + responseData)
      }).catch((error) => console.error(error));

    }
  };

  //Input file upload
  const pickHelpingFile = async () => {
    console.log(hashcode);
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
      .then((responseData) => {
        console.log("Input file success " + result.file + ". Response = "  + responseData)
      }).catch((error) => console.error(error));

    }
  };


  //Dependency upload
  const addDependencies = async () => {
    console.log(hashcode);
    fetch(
        `http://127.0.0.1:5000/add-dependecies/${hashcode}`,
        {
          body: JSON.stringify(text),
          method: "POST",
          headers: {
            'Accept': 'application/json',
            'Content-Type': 'application/json'
          }
        }
      )
      .then((responseData) => {
        console.log("Dependency Success")
      }).catch((error) => console.error(error));
  };

  //Execute File
  const executeFile = async () => {
    console.log(hashcode);
    fetch(
        `http://127.0.0.1:5000/execute/${hashcode}`,
        {
          method: "POST"
        }
      )
      .then((responseData) => {
        console.log("Execute success. Response data = " + responseData);
        //To run loading circle which only runs on null value
        setFileStatus(null);
      }).catch((error) => console.error(error));


      //Check execution
      let interval = setInterval(() => {
        console.log("Running");
        fetch(
          `http://127.0.0.1:5000/poll/${hashcode}`,
          {
            method: "GET"
          }
        )
        .then((responseData) => {
          if(responseData.status === 'SUCCESS')  {
            setFileStatus('Complete');
            setOututFile(responseData.url);
            console.log("File executed " + responseData.url)
            clearInterval(interval);
            return;
          }
          console.log("Execution in progress " + responseData)
        }).catch((error) => console.error(error));
      }, 3000);
  };

  return (
    <View style={{ flex: 1, alignItems: 'center', justifyContent: 'center' }}>
      <Logo/>
      <Header> Run Python file on server. </Header> <br/><br/><br/>
      <Button title="Pick python file(.py) from storage" onPress={pickFile} /> <br/><br/><br/>
      <Button title="Pick optional supporting input file" onPress={pickHelpingFile} /> <br/><br/><br/>
      <Secondary>Add dependencies in json format</Secondary>
      <TextInput style={styles.input} onChangeText={onChangeText} value={text} />
      <Button title="Add Dependencies" onPress={addDependencies} /> <br/><br/><br/>
      {file && <Header>Your file is being uploaded and it will execute on the server.</Header> && <br/> && <br/> && <br/>}<br/><br/><br/>
      <Button title="Execute Python File" onPress={executeFile}></Button>
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
