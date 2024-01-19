function registerUser(){
	const lastname = document.getElementById('Reglastn').value;
	const firstname = document.getElementById('RegFirstn').value;
	const username = document.getElementById('Regusername').value;
	const password1 = document.getElementById('Regpassword1').value;
	const password2 = document.getElementById('Regpassword2').value;

	if (!lastname || !firstname || !username || !password1 || !password2) {
		alert("Пожалуйста, введите все необходимые данные.");
		return;
	}

	if (password1 !== password2) {
		alert("Пароли не совпадают");
		return;
	}

	// localStorage.setItem('userData', JSON.stringify({
	// 	lastname: lastname,
	// 	firstname: firstname,
	// 	username: username,
	// 	password: password1,}));
	
	// alert("Регистрация прошла успешно");

	const data = {
        last_name: lastname,
        first_name: firstname,
        password: password1,
        user_name: username
    };

	axios.post("http://127.0.0.1:8000/users/reg", data)
	.then(
		alert("Регистрация прошла успешно")
	)
	.catch(
		alert("Возникла ошибка в момент регистрации.")
	);
}


function authorizationUser(){
	const username = document.getElementById('username').value;
	const password = document.getElementById('password').value;

	// let userData = JSON.parse(localStorage.getItem('userData'));

	if (!username || !password) {
        alert("Пожалуйста, введите все необходимые данные.");
        return;
    }

	// if (userData && userData.username === username && userData.password === password) {
	// 	alert('Авторизация прошла успешно');
	// 	window.location.href = "../Project1/Pages/indexUser.html";
	// }
	// else {
	// 	alert('Имя пользователя или пароль не верны');
	// }
	

}


async function login() {
	const username = document.getElementById('username').value;
	const password = document.getElementById('password').value;

	// const data = {
    //     user_name: username,
    //     password: password
    // };

    // axios.post("http://127.0.0.1:8000/users/log", data)
    //     .then(response => {
    //         // document.getElementById("response").textContent = JSON.stringify(response.data);
    //         alert("Вход выполнен успешно");
    //     })
    //     .catch(error => {
    //         // console.error("Error posting data:", error);
    //         alert("Возникла ошибка в момент входа.");
    //     });


	axios.post('http://127.0.0.1:8000/token', {
		username: username,
		password: password
		})
		.then(response => {
			const token = response.data.access_token;
			localStorage.setItem('access_token', token);
			window.location.href = "../Pages/indexUser.html";
		})
		.catch(error => {
			console.error('Ошибка аутентификации', error);
		});

}
// 	// Отправка данных на сервер для аутентификации
// 	const response = await fetch('/token', {
// 		method: 'POST',
// 		headers: {
// 			'Content-Type': 'application/x-www-form-urlencoded',
// 		},
// 		body: `username=${encodeURIComponent(username)}&password=${encodeURIComponent(password)}`,
// 	});

// 	const data = await response.json();


// 	// Проверка ответа сервера

// 	if (response.ok) {
// 		const token = data.access_token;
		
// 		// // Сохранение токена в localStorage (или другом безопасном месте)
// 		// localStorage.setItem('token', token);

//         // Декодирование токена

// 		const decodedToken = parseJwt(token);

//         // Сохранение данных в localStorage

// 		localStorage.setItem('token', token);
//         localStorage.setItem('username', decodedToken.sub);
//         localStorage.setItem('role', decodedToken.lvl);

//         // Перенаправление на нужную страницу

// 		if (decodedToken.lvl === '0') {
//             window.location.href = '../Pages/indexUser.html';
//         } else if (decodedToken.lvl === '1') {
//             window.location.href = '../indexAdmin.html';
//         }		

// 	} else {
// 		// Обработка ошибок аутентификации

// 		console.error(data.detail);
// 	}
// }


// // Функция для декодирования JWT токена

// function parseJwt(token) {
//     const base64Url = token.split('.')[1];
//     const base64 = base64Url.replace(/-/g, '+').replace(/_/g, '/');
//     const jsonPayload = decodeURIComponent(atob(base64).split('').map(function(c) {
//         return '%' + ('00' + c.charCodeAt(0).toString(16)).slice(-2);
//     }).join(''));

//     return JSON.parse(jsonPayload);
// }


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