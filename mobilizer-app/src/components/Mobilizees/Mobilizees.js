import React from 'react';
import Mobilizee from './Mobilizee/Mobilizee';

const mobilizees = (props) => props.mobilizees.map((mobilizee, index) => {
	console.log(props.mobilizers);
	return <Mobilizee
		id = {mobilizee.id}
		name = {mobilizee.name}
		email = {mobilizee.email}
		phone = {mobilizee.phone}
		address = {mobilizee.address}
		notes = {mobilizee.notes}
		removal_function = {() => props.removal_function(mobilizee.id)}
		assign_function = {props.assign_function}
		mobilizers = {props.mobilizers}
		 />
});

export default mobilizees;