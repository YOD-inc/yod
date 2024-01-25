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