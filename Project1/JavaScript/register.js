document.addEventListener("DOMContentLoaded", function () {
    axios.get("http://127.0.0.1:8000/pass")
        .then(response => {
        })
        .catch(error => {
            alert("Error fetching data from database. Ошибка получения значений из базы данных.");
        });
});
function login() {
	const username = document.getElementById('username').value;
	const password = document.getElementById('password').value;
	if (!username || !password) {
        alert("Пожалуйста, введите все необходимые данные.");
        return;
    }
	axios.post(`http://127.0.0.1:8000/cookie?username=${username}&password=${password}`)
		.then(response => {
			alert("Вход произведен успешно.");
		})
		.catch(error => {                                                                                                                                                                                                                           
			console.error('Ошибка аутентификации', error);
		});
}