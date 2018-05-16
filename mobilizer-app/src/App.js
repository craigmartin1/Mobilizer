import React, { Component } from 'react';
import logo from './logo.svg';
import './App.css';
import Mobilizees from '../components/Mobilizes/Mobilizees';
import Mobilizers from '../components/Mobilizers/Mobilizers';

class App extends Component {
  state = {
    role = props.role
    //get mobilizer,mobilizee content from server here
  }
  render() {
    if(this.state.role === 'coordinator'){
      return (
        <div className="App">
          <Mobilizers mobilizers={this.state.mobilizers} removal_function={this.removeMobilizer} />
          <Mobilizees mobilizees={this.state.unattached_mobilizees} removal_function={this.deleteMobilizer}/>
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
