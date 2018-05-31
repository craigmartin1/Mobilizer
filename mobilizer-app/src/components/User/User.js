import Mobilizees from '../Mobilizees/Mobilizees';
import Mobilizers from '../Mobilizers/Mobilizers';
import React, { Component } from 'react';
import { BrowserRouter, Route, Link, withRouter } from 'react-router-dom';
import axios from 'axios';

const user = (props) => {
	console.log(props.id)
	const removeMobilizeeHandler = (id) =>{
    
    }


	return (
        <div>
         <Mobilizees mobilizees={props.mobilizees} removal_function={removeMobilizeeHandler} />
         <p><Link to={{ pathname:"/change_password", state: {id: props.id} }}>Change Password</Link></p>
        </div>
       
		)

};

export default withRouter(user);