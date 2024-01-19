// Заполнение таблицы врачей с загрузкой страницы

document.addEventListener("DOMContentLoaded", function () {
    axios.get("http://127.0.0.1:8000/doctors")
        .then(response => {
            const tableBody = document.querySelector("#doctor-table tbody");

            tableBody.innerHTML = "";

            response.data.doctor.forEach(item => {
                const row = tableBody.insertRow();
                row.insertCell(0).textContent = item.id;
                // row.insertCell(1).textContent = item.last_n;
                // row.insertCell(2).textContent = item.first_n;
                // row.insertCell(3).textContent = item.patro_n;
                row.insertCell(1).textContent = item.full_n;
                row.insertCell(2).textContent = item.phone_n;
                row.insertCell(3).textContent = item.block_id;
                row.insertCell(4).textContent = item.exp;
            });
        })
        .catch(error => {
            // console.error("Error fetching data:", error);
            alert("Error fetching data from database. Ошибка получения значений из базы данных.");
        });
});


// Функция для добавления врачей

function doctor_add() {
    const last_n = document.getElementById("addlast").value;
    const first_n = document.getElementById("addname").value;
    const patro_n = document.getElementById("addpatro").value;
    const phone_num = document.getElementById("addphone").value;
    const block_id = document.getElementById("addblock").value;
    const exp = document.getElementById("addexp").value;

    if (!last_n || !first_n || !patro_n || !phone_num || !block_id || !exp) {
        alert("Please enter all the necessary data. Пожалуйста, введите все необходимые данные.");
        return;
    }

    const data = {
        last_n: last_n,
        first_n: first_n,
        patro_n: patro_n,
        phone_num: phone_num,
        block_id: first_n,
        exp: exp
    };

    axios.post("http://127.0.0.1:8000/doctors/add", data)
        .then(response => {
            // document.getElementById("response").textContent = JSON.stringify(response.data);
            alert("Doctor added successfully. Врач добавлен успешно.");
        })
        .catch(error => {
            // console.error("Error posting data:", error);
            alert("An error occurred. Возникла ошибка.");
        });
}


// Функция удаления врачей

function doctor_delete() {
    const doctor_id = document.getElementById("deldoctor").value;

    if (!doctor_id) {
        alert("Please enter doctor ID. Пожалуйста, введите ID врача.");
        return;
    }

    axios.delete(`http://127.0.0.1:8000/doctors/delete/{id}?id=${doctor_id}`)
        .then(response => {
            alert("Doctor deleted successfully. Врач удален успешно.");
        })
        .catch(error => {
            // console.error("Error deleting user:", error);
            alert("An error occurred. Возникла ошибка.");
        });
}
