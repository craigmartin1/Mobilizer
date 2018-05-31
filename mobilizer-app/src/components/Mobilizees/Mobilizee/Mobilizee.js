import React from 'react';
import { Link } from 'react-router-dom';
import './Mobilizee.css';

const mobilizee = (props) => {
	if(props.mobilizers != null){
		var mobilizer_options = []
		var i;
		for(i = 0; i< props.mobilizers.length; i++){
			mobilizer_options.push([props.mobilizers[i].mobilizer_id,props.mobilizers[i].name]);
		}
	}
	let are_there_mobilizers = false
	if(props.mobilizers){
		are_there_mobilizers = true;
	}
	const handleChange = (event) => {
		props.assign_function(props.id, event.target.value);
	}

	const populate = (options) => {
		return options.map((option, index) => (
			<option key={index} value={option.id}>{option.name}</option>
			));
	}

	const Dropdown = (props) => {
		return (
			<select onChange={handleChange}> 
				<option value="-1">Unassigned</option>
				{populate(props.mobilizers)}
			</select>	
		);
	}
	const UpdateLink = (props) =>{
		return
	}
	return (

		<div className="Mobilizee">
			<p><strong>{props.name}</strong></p>
			<p>{props.address}</p>
			<p>{props.email}</p>
			<p>{props.phone}</p>
			<button onClick={props.removal_function}>Remove</button>
			{are_there_mobilizers ? <Dropdown mobilizers={props.mobilizers} change_function = {handleChange}/> : <p><Link to={{ pathname:"/update", state: {id: props.id, name: props.name, email: props.email, phone: props.phone, address: props.address} }}>Update Contact</Link></p>}
			
			<p>{props.notes}</p>
		</div>
		
	)

}

export default mobilizee;