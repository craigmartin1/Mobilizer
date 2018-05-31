import React from 'react';
import axios from 'axios';

const passwordform = (props) => {
	const submitUpdateHandler = (event) => {
		console.log(props.id);
    	axios.post('/mobilizer/change_password', {password: event.target.value, mobilizer_id:props.id}).catch(error => {
          console.log(error);
        });
  	}

	return (

		<div>
			<form onSubmit = {submitUpdateHandler}>
				<input type="hidden" defaultValue={props.id} />
				<label>
					New Password:
					<input type="text" name="password" onChange={submitUpdateHandler}/>
				</label>
				<input type="submit" defaultValue="Save Changes" />
			</form>
		</div>
		
	)

}

export default passwordform;