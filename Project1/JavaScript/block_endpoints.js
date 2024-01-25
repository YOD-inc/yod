// Заполнение таблицы участков с загрузкой страницы

document.addEventListener("DOMContentLoaded", function () {
    axios.get("http://127.0.0.1:8000/block")
        .then(response => {
            const tableBody = document.querySelector("#block-table tbody");

            tableBody.innerHTML = "";

            response.data.block.forEach(item => {
                const row = tableBody.insertRow();
                row.insertCell(0).textContent = item.id;
                row.insertCell(1).textContent = item.address;
                row.insertCell(2).textContent = item.block_num;
            });
        })
        .catch(error => {
            alert("Error fetching data from database. Ошибка получения значений из базы данных.");
        });
});

// Функция для добавления участков

function block_add() {
    const address = document.getElementById("addstreet").value;
    const block_num = document.getElementById("addblock").value;

    if (!address || !block_num) {
        alert("Please enter both address and number of block. Пожалуйста, введите и адрес, и номер участка.");
        return;
    }

    const data = {
        address: address,
        block_num: block_num
    };

    axios.post(`http://127.0.0.1:8000/block/add?address=${address}&block_num=${block_num}`)
        .then(response => {
            alert("Block added successfully. Участок добавлен успешно.");
        })
        .catch(error => {
            alert("An error occurred. Возникла ошибка.");
        });
}


// Функция удаления участков

function block_delete() {
    const block_id = document.getElementById("delblock").value;

    if (!block_id) {
        alert("Please enter block ID. Пожалуйста, введите ID участка.");
        return;
    }

    axios.delete(`http://127.0.0.1:8000/block/delete/${block_id}`)
        .then(response => {
            alert("Block deleted successfully. Участок удален успешно.");
        })
        .catch(error => {
            alert("An error occurred. Возникла ошибка.");
        });
}
