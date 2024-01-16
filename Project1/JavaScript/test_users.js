// Заполнение таблицы пользователей с загрузкой страницы

document.addEventListener("DOMContentLoaded", function () {
    axios.get("http://127.0.0.1:8000/test_users")
        .then(response => {
            const tableBody = document.querySelector("#data-table tbody");

            tableBody.innerHTML = "";

            response.data.test_users.forEach(item => {
                const row = tableBody.insertRow();
                row.insertCell(0).textContent = item.id;
                row.insertCell(1).textContent = item.last_name;
                row.insertCell(2).textContent = item.first_name;
            });
        })
        .catch(error => {
            console.error("Error fetching data:", error);
        });
});



