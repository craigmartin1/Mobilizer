import React from 'react';
import axios from 'axios';

const mobilizerform = (props) => {
	const submitUpdateHandler = ev => {
		ev.preventDefault();
		const username = ev.target.username.value;
		const password = ev.target.password.value;
		const name = ev.target.name.value;
		const email = ev.target.email.value;
		const phone = ev.target.phone.value;
		console.log(phone);
    	axios.post('/coordinator/register_mobilizer', {password: password, username: username, name: name, email: email, phone: phone, coordinator_id:props.id}).catch(error => {
          console.log(error);
        });
  	}

	return (
		<div>
			<form onSubmit = {submitUpdateHandler}>
				<input type="hidden" name="id" defaultValue={props.id} />
				<label>
					Username:
					<input type="text" name="username"/>
				</label>
				<label>
					Name:
					<input type="text" name="name"/>
				</label>
				<label>
					Password:
					<input type="text" name="password" />
				</label>
				<label>
					email:
					<input type="email" name="email" />
				</label>
				<label>
					Phone:
					<input type="text" name="phone"/>
				</label>
				<button type="submit"> Save Changes </button>
			</form>
		</div>
		
	)

}

export default mobilizerform;