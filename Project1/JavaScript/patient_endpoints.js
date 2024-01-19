// Заполнение таблицы пациентов с загрузкой страницы

document.addEventListener("DOMContentLoaded", function () {
    axios.get("http://127.0.0.1:8000/patients")
        .then(response => {
            const tableBody = document.querySelector("#patient-table tbody");

            tableBody.innerHTML = "";

            response.data.patient.forEach(item => {
                const row = tableBody.insertRow();
                row.insertCell(0).textContent = item.id;
                row.insertCell(1).textContent = item.last_n;
                row.insertCell(2).textContent = item.first_n;
                row.insertCell(3).textContent = item.patro_n;
                row.insertCell(4).textContent = item.phone_num;
                row.insertCell(5).textContent = item.address;
                row.insertCell(6).textContent = item.gender_char;
                row.insertCell(6).textContent = item.age;
            });
        })
        .catch(error => {
            // console.error("Error fetching data:", error);
            alert("Error fetching data from database. Ошибка получения значений из базы данных.");
        });
});

// Гендер селект (если нижеследующее не сработает)
// 
// document.querySelector('form').addEventListener('submit', function(e) {
//     e.preventDefault();
//     const gender = document.querySelector('input[name="gender"]:checked').value;
//     console.log(gender); // You can then save this value in a const or use it as needed
//   });

// Функция для добавления пациентов

function patient_add() {
    const last_n = document.getElementById("addlast").value;
    const first_n = document.getElementById("addname").value;
    const patro_n = document.getElementById("addpatro").value;
    const phone_num = document.getElementById("addphone").value;
    const address = document.getElementById("addstreet").value;
    const age = document.getElementById("addage").value;
    // const gender = document.getElementById("addgender").value;
    const gender = document.querySelector('input[name="gender"]:checked').value;


    if (!last_n || !first_n || !patro_n || !phone_num || !address || !age || !gender) {
        alert("Please enter all the necessary data. Пожалуйста, введите все необходимые данные.");
        return;
    }

    const data = {
        last_n: last_n,
        first_n: first_n,
        patro_n: patro_n,
        phone_num: phone_num,
        address: address,
        age: age,
        gender: gender
    };

    axios.post(`http://127.0.0.1:8000/patients/add?last_n=${last_n}&first_n=${first_n}&patro_n=${patro_n}&phone_num=${phone_num}&address=${address}&age=${age}&gender=${gender}`)
        .then(response => {
            // document.getElementById("response").textContent = JSON.stringify(response.data);
            alert("Patient added successfully. Пациент добавлен успешно.");
        })
        .catch(error => {
            // console.error("Error posting data:", error);
            alert("An error occurred. Возникла ошибка.");
        });
}


// Функция удаления пациентов

function patient_delete() {
    const patient_id = document.getElementById("delpatient").value;

    if (!patient_id) {
        alert("Please enter patient ID. Пожалуйста, введите ID пациента.");
        return;
    }

    axios.delete(`http://127.0.0.1:8000/patients/delete/${patient_id}`)
        .then(response => {
            alert("Patient deleted successfully. Пациент удален успешно.");
        })
        .catch(error => {
            // console.error("Error deleting user:", error);
            alert("An error occurred. Возникла ошибка.");
        });
}
