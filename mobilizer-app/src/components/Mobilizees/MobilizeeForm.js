import React from 'react';
import axios from 'axios';

const mobilizeeform = (props) => {
	const submitUpdateHandler = ev => {
		ev.preventDefault();
		const fname = ev.target.fname.value;
		const lname = ev.target.lname.value;
		const address = ev.target.address.value;
		const email = ev.target.email.value;
		const phone = ev.target.phone.value;
    	axios.post('/coordinator/register_mobilizee', {fname: fname, lname: lname, address: address, email: email, phone: phone}).catch(error => {
          console.log(error);
        });
  	}

	return (
		<div>
			<form onSubmit = {submitUpdateHandler}>
				<label>
					First Name:
					<input type="text" name="fname"/>
				</label>
				<label>
					Last Name:
					<input type="text" name="lname"/>
				</label>
				<label>
					Address
					<input type="text" name="address" />
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

export default mobilizeeform;