import Mobilizees from '../Mobilizees/Mobilizees';
import Mobilizers from '../Mobilizers/Mobilizers';
import React, { Component } from 'react';
import { BrowserRouter, Route, Link, withRouter } from 'react-router-dom';
import axios from 'axios';

const user = (props) => {

	const removeMobilizeeHandler = (id) =>{
    axios.post('/mobilizer/removal', {mobilizee_id:id}).catch(error => {
          console.log(error);
        });
    }


	return (
        <div>
         <Mobilizees mobilizees={props.mobilizees} removal_function={removeMobilizeeHandler} />
        </div>
       
		)

};

export default withRouter(user);