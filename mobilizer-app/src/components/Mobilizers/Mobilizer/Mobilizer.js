import React from 'react';
import classes from './Mobilizer.css';

const mobilizer = (props) => {
	return (
		<div className={classes.Mobilizer}>
			<p><strong>{props.name}</strong></p>
			<p>{props.email}</p>
			<p>{props.phone}</p>
			<button onClick={props.removal_function}>Delete</button>
		</div>
	)

}

export default mobilizer;