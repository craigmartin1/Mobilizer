import React, { Component } from 'react';
import './App.css';
import Mobilizees from './components/Mobilizees/Mobilizees';
import Mobilizers from './components/Mobilizers/Mobilizers';
import axios from 'axios';

class App extends Component {
  componentDidMount(){
    console.log("Mounted");
    if(this.state.role === "coordinator"){
      axios.get('/coordinator/see_mobilizers')
        .then(response => {
          this.setState({mobilizers: response.data});
        })
        .catch(error => {
          console.log(error);
        });
      //axios.get('/coordinator/unattached_mobilizees')
        //.then(response => {
          //this.setState({mobilizees: response.data});
        //})
        //.catch(error => {
          //console.log(error);
        //});
    }else if(this.state.role === "mobilizer"){
      axios.get('/mobilizer/seeMobilizees')
        .then(response => {
          this.setState({mobilizees: response.data});
        })
        .catch(error => {
          console.log(error);
        });
    }
  }
  removeMobilizerHandler = (id) =>{
    axios.post('/coordinator/removeMobilizer', {id:id}).catch(error => {
          console.log(error);
        });
  }

  removeMobilizeeHandler = (id) =>{
    axios.post('/mobilizer/removeMobilizee', {id:id}).catch(error => {
          console.log(error);
        });
  }

  deleteMobilizeeHandler = (id) =>{
    axios.post('/coordinator/deleteMobilizee', {id:id}).catch(error => {
          console.log(error);
        });
  }
  state = {
    //role: props.role,
    //get mobilizer,mobilizee content from server here, test data below
    role: "coordinator",
    mobilizers: [
      {id: 1, name: "Test1", phone: '555-555-5555', email: 'test@gmail.com'},
      {id: 2, name: "Test2", phone: '222-555-5555', email: 'test2@gmail.com'},
      {id: 3, name: "Test3", phone: '333-555-5555', email: 'test3@gmail.com'}
    ],

    mobilizees: [
      {id: 1, name: "mob1", phone: '555-555-5555', email: 'mob_test@test.com', address: '123 Real Street'}, 
      {id: 2, name: "mob2", phone: '555-222-5555', email: 'mob_test2@test.com', address: '124 Real Street'},
      {id: 3, name: "mob3", phone: '555-333-5555', email: 'mob_test3@test.com', address: '133 Real Street'}
    ]
  }
  render() {
    if(this.state.role === 'coordinator'){
      return (
        <div className="App">
          <Mobilizers mobilizers={this.state.mobilizers} removal_function={this.removeMobilizer} />
          <Mobilizees mobilizees={this.state.mobilizees} removal_function={this.deleteMobilizer}/>
        </div>
      );
    } else if(this.state.role === 'mobilizer'){
      return (
        <div className="App">
          <Mobilizees mobilizees={this.state.mobilizees} />
        </div>
      );
    }
  }
}

export default App;
