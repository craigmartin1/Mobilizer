import React from 'react';
import axios from 'axios';

const updateform = (props) => {
	const submitUpdateHandler = (event) => {
		console.log(event.target.name);
		const target = event.target.name;
    	axios.post('/mobilizer/update', {[target]: event.target.value, mobilizee_id:props.id}).catch(error => {
          console.log(error);
        });
  	}

	return (

		<div>
			<form onSubmit = {submitUpdateHandler}>
				<input type="hidden" defaultValue={props.id} />
				<label>
					Name:
					<input type="text" name="name" defaultValue={props.name} onChange={submitUpdateHandler}/>
				</label>
				<label>
					Email:
					<input type="email" name="email" defaultValue={props.email} onChange={submitUpdateHandler}/>
				</label>
				<label>
					Phone:
					<input type="text" name="phone" defaultValue={props.phone} onChange={submitUpdateHandler}/>
				</label>
				<label>
					Address:
					<input type="text" name="address" defaultValue={props.address} onChange={submitUpdateHandler}/>
				</label>
				<input type="submit" defaultValue="Save Changes" />
			</form>
		</div>
		
	)

}

export default updateform;