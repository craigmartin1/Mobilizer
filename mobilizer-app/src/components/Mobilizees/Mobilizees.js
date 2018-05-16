import React from 'react';
import Mobilizee from './Mobilizee/Mobilizee';

const mobilizees = (props) => props.mobilizees.map((mobilizee, index) => {
	return <Mobilizee
		name = {mobilizee.name}
		email = {mobilizee.email}
		phone = {mobilizee.phone}
		address = {mobilizee.address}
		notes = {mobilizee.notes}
		removal_function = {() => props.removal_function(mobilizee.id)} />
});

export default mobilizees;