// Заполнение таблицы участков с загрузкой страницы для пользователя

document.addEventListener("DOMContentLoaded", function () {
    axios.get("http://127.0.0.1:8000/block")
        .then(response => {
            const tableBody = document.querySelector("#block-table tbody");

            tableBody.innerHTML = "";
            
            response.data.block.forEach(item => {
                const row = tableBody.insertRow();
                row.insertCell(0).textContent = item.address;
                row.insertCell(1).textContent = item.block_num;
            });
        })
        .catch(error => {
            // console.error("Error fetching data:", error);
            alert("Error fetching data from database. Ошибка получения значений из базы данных.");
        });
});