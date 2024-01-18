// Заполнение таблицы врачей с загрузкой страницы

document.addEventListener("DOMContentLoaded", function () {
    axios.get("http://127.0.0.1:8000/doctors")
        .then(response => {
            const tableBody = document.querySelector("#doctor-table tbody");

            tableBody.innerHTML = "";

            response.data.doctor.forEach(item => {
                const row = tableBody.insertRow();
                row.insertCell(0).textContent = item.full_n;
                row.insertCell(1).textContent = item.block_id;
            });
        })
        .catch(error => {
            // console.error("Error fetching data:", error);
            alert("Error fetching data from database. Ошибка получения значений из базы данных.");
        });
});