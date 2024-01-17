document.getElementById('loginform').addEventListener('submit', function(event)
{
	event.preventDefault();
	let username = document.getElementById('username').value;
	let password = document.getElementById('password').value;
});

document.getElementById('registerform').addEventListener('submit', function(event)
{
	event.preventDefault();
	let lastname = document.getElementById('lastname').value;
	let firstname = document.getElementById('firstname').value;
	let username = document.getElementById('username').value;
	let password = document.getElementById('password').value;
});