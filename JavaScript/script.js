import axios from 'axios';

const axios = require('axios');

const app = axios();

document.getElementById('addpatientbutton').addEventListener('click', async () => {
	try {
		const response = await axios.get('http://127.0.0.1:8000/docs#/doctors/get_all_doctors_doctors_get');

		document.getElementById('responseTextArea').value = JSON.stringify(response.data, null, 2);
	}
	catch (error) {
		console.error('Error mking API query:', error);
	}
});