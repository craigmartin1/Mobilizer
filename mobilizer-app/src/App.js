import React, { Component } from 'react';
import { BrowserRouter, Route, Link, withRouter } from 'react-router-dom';
import './App.css';
import Mobilizees from './components/Mobilizees/Mobilizees';
import Mobilizers from './components/Mobilizers/Mobilizers';
import Coordinator from './components/Coordinator/coordinator';
import UpdateForm from './components/Mobilizees/UpdateForm';
import PasswordForm from './components/Mobilizers/PasswordForm';
import User from './components/User/User';
import * as queryString from 'query-string';
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
      axios.get('/coordinator/unattached_mobilizees')
        .then(response => {
          this.setState({mobilizees: response.data});
        })
        .catch(error => {
          console.log(error);
        });
      axios.get('/coordinator/see_removal_requests')
        .then(response => {
          this.setState({removal_requests: response.data});
        })
        .catch(error => {
          console.log(error);
        });
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
    ],

    removal_requests: [
      {id: 1, name: "mob1", phone: '555-555-5555', email: 'mob_test@test.com', address: '123 Real Street', mobilizer: 1}
    ]
  }

  render() {
      return (
        <BrowserRouter>
        <div className="App">
          <p><Link to="/coordinator">Coordinator Test</Link></p>
          <p><Link to="/mobilizer">Mobilizer Test</Link></p>
          <Route path="/coordinator" render={(props) => (
              <Coordinator mobilizers={this.state.mobilizers} mobilizees={this.state.mobilizees} removal_requests={this.state.removal_requests} />
            )} />
          <Route path="/mobilizer" render={(props) => (
              <User mobilizees={this.state.mobilizees} id="1" />
            )} />
          <Route path="/update" render = {(props) => (<UpdateForm id={props.location.state.id} name={props.location.state.name} email={props.location.state.email} phone={props.location.state.phone} address={props.location.state.address} submit_function={this.submitUpdateHandler} />)}/>
          <Route path="/change_password" render = {(props) => (<PasswordForm id={props.location.state.id} />)} />
        </div>
        </BrowserRouter>
      );
    }
}

export default App;
