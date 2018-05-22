import React from 'react';
import './Mobilizee.css';

const mobilizee = (props) => {
	return (
		<div className="Mobilizee">
			<p><strong>{props.name}</strong></p>
			<p>{props.address}</p>
			<p>{props.email}</p>
			<p>{props.phone}</p>
			<button onClick={props.removal_function}>Remove</button>
			<p>{props.notes}</p>
		</div>
		
	)

}

export default mobilizee;