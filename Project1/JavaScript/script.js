function toggleDropdown() {
	var dropdown = document.getElementById("dropdown-content");
	if (dropdown.style.display === "block") {
		dropdown.style.display = "none";
	}
	else {
		dropdown.style.display = "block";
	}
}

window.addEventListener("click", function(event){
	if (!event.target.matches('.dropbtn')){
		var dropdowns = document.getElementsByClassName("dropdown-content")
		for (var i = 0; i < dropdown.length; i++){
			var openDropdown = dropdowns[i];
			if (openDropdown.style.display === "block"){
				openDropdown.style.display = "none"
			}
		}
	}
});

function invis_acc() {
	document.getElementById("mybtn").addEventListener('click', function () {
		document.getElementById("myli").innerHTML = "<a href='#'><img src='../Project1/Images/Account.png' alt='Логотип больницы' class='logo'></img></a>"
	})
}
// function gotoPage() {
// 	var selectedValue = document.getElementById("myList").value;
// 	if (selectedValue) {
// 		window.location = selectedValue;
// 	}
// }
// import axios from 'axios';

// const axios = require('axios');

// const app = axios();

// document.getElementById('addpatientbutton').addEventListener('click', async () => {
// 	try {
// 		// const response = await axios.get('http://127.0.0.1:8000/docs#/doctors/get_all_doctors_doctors_get');
// 		const response = await axios.get('http://127.0.0.1:8000/docs#/test_users/get_all_test_users_test_users_get');

// 		document.getElementById('responseTextArea').value = JSON.stringify(response.data, null, 2);
// 	}
// 	catch (error) {
// 		console.error('Error mking API query:', error);
// 	}
// });