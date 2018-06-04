import Mobilizees from '../Mobilizees/Mobilizees';
import Mobilizers from '../Mobilizers/Mobilizers';
import React, { Component } from 'react';
import { BrowserRouter, Route, Link, withRouter } from 'react-router-dom';
import axios from 'axios';

const coordinator = (props) => {

	const deleteMobilizeeHandler = (id) =>{
    	axios.post('/coordinator/delete_mobilizee', {mobilizee_id:id}).catch(error => {
          console.log(error);
        });
  	}

  	const removeMobilizerHandler = (id) =>{
    axios.post('/coordinator/remove_mobilizer', {mobilizer_id:id}).catch(error => {
          console.log(error);
        });
    }

  	const assignMobilizeeHandler = (mobilizee_id, mobilizer_id) => {
    	axios.post('/coordinator/assign', {mobilizees:mobilizee_id, mobilizer_id:parseInt(mobilizer_id)}).catch(error =>{
      		console.log(error);
    	});
    }

	return (
		<div>
			<p><Link to={{ pathname:"/register_mobilizer", state: {id: props.id} }}>Register Mobilizer</Link></p>
          	<p><Link to={{ pathname:"/register_mobilizee", state: {id: props.id} }}>Register Mobilizee</Link></p>
          	<p><Link to={{ pathname:"/mass_register", state: {id: props.id} }}>Mass Register Mobilizees</Link></p>
			<Mobilizers mobilizers={props.mobilizers} removal_function={removeMobilizerHandler} />
          	<h1>Unattached Mobilizees</h1>
          	<Mobilizees mobilizees={props.mobilizees} removal_function={deleteMobilizeeHandler} assign_function={assignMobilizeeHandler} mobilizers={props.mobilizers}/>
          	<h1>Removal Requests</h1>
          	<Mobilizees mobilizees={props.removal_requests} removal_function={deleteMobilizeeHandler} />

		</div>
		)

};

export default withRouter(coordinator);

