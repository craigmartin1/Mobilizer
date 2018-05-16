import React from 'react';
import Mobilizer from './Mobilizer/Mobilizer';

const mobilizers = (props) => props.mobilizers.map((mobilizer, index) => {
	return <Mobilizer
		name = {mobilizer.name}
		email = {mobilizer.email}
		phone = {mobilizer.phone}
		removal_function = {() => props.removal_function(mobilizer.id)} />
});

export default mobilizers;