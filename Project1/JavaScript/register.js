function registerUser(){
	let lastname = document.getElementById('Reglastn').value;
	let firstname = document.getElementById('RegFirstn').value;
	let username = document.getElementById('Regusername').value;
	let password1 = document.getElementById('Regpassword1').value;
	let password2 = document.getElementById('Regpassword2').value;

	if (password1 !== password2) {
		alert("Пароли не совпадают");
		return;
	}

		localStorage.setItem('userData', JSON.stringify({
		lastname: lastname,
		firstname: firstname,
		username: username,
		password: password1,}));
		alert("Регистрация прошла успешно");
}


function authorizationUser(){
	let username = document.getElementById('username').value;
	let password = document.getElementById('password').value;

	let userData = JSON.parse(localStorage.getItem('userData'));

	if (userData && userData.username === username && userData.password === password) {
		alert('Авторизация прошла успешно');
		window.location.href = "../Project1/Pages/indexUser.html";
	}
	else {
		alert('Имя пользователя или пароль не верны');
	}
}







// document.getElementById('loginform').addEventListener('submit', function(event)
// {
// 	event.preventDefault();
// 	let username = document.getElementById('username').value;
// 	let password = document.getElementById('password').value;
// });

// document.getElementById('registerform').addEventListener('submit', function(event)
// {
// 	event.preventDefault();
// 	let lastname = document.getElementById('lastname').value;
// 	let firstname = document.getElementById('firstname').value;
// 	let username = document.getElementById('username').value;
// 	let password = document.getElementById('password').value;
// });



// function checkPassword() {
// 	let password1 = document.getElementById('Regpassword1').value;
// 	let password2 = document.getElementById('Regpassword2').value;

// 	if (password1 === password2) {
// 		alert("ОК");
// 		localStorage.setItem('password', password1);
// 		// window.location.href = "../Project1/Pages/indexUser.html";
// 	}
// 	else {
// 		alert("Пароли не совпадают, попробуйте ввести их заново.");
// 		document.getElementById('Regpassword1').value = clear;
// 		document.getElementById('Regpassword2').value = clear;
// 	}
// 	localStorage.setItem('userData', JSON.stringify({
// 		lastname: lastname,
// 		firstname: firstname,
// 		username: username,
// 		password: password1,
// 	}));

// }

// function Authorization() {
// 	let username = document.getElementById('username').value;
// 	let password = document.getElementById('password').value;

// 	if (localStorage.getItem(username) === password1) {
// 		alert('Авторизация успешна');
// 		window.location.href = "../Project1/Pages/indexUser.html"
// 	}
// 	else {
// 		alert('Имя пользователя или пароль неверны');
// 		document.getElementById('username').value = clear;
// 		document.getElementById('password').value = clear;
// 	}
// }