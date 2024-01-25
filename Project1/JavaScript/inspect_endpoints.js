// Заполнение таблицы осмотров и полей выбора с загрузкой страницы

document.addEventListener("DOMContentLoaded", function () {
    axios.get("http://127.0.0.1:8000/inspect")
        .then(response => {
            const tableBody = document.querySelector("#inspect-table tbody");

            tableBody.innerHTML = "";

            response.data.inspect.forEach(item => {
                const row = tableBody.insertRow();
                row.insertCell(0).textContent = item.id;
                row.insertCell(1).textContent = item.place;
                row.insertCell(2).textContent = item.date;
                row.insertCell(3).textContent = item.doctor;
                row.insertCell(4).textContent = item.patient;
                row.insertCell(5).textContent = item.symptom;
                row.insertCell(6).textContent = item.diagnosis
                row.insertCell(7).textContent = item.prescriptions;
            });
        })
        .catch(error => {
            alert("Error fetching data from database. Ошибка получения значений из базы данных.");
        });


// Функция для добавления осмотров

function inspect_add() {
    const place = document.getElementById("addplace").value;
    const date = document.getElementById("adddate").value;
    const doctor = document.getElementById("adddoctor").value;
    const patient = document.getElementById("addpatient").value;
    const symptom = document.getElementById("addsymptoms").value;
    const diagnosis = document.getElementById("adddyagnosis").value;
    const prescriptions = document.getElementById("addprescriptions").value;

    if (!place || !date || !doctor || !patient || !symptom || !diagnosis || !prescriptions) {
        alert("Please enter all the necessary data. Пожалуйста, введите все необходимые данные.");
        return;
    }

    const data = {
        place: place,
        date: date,
        doctor: doctor,
        patient: patient,
        symptom: symptom,
        diagnosis: diagnosis,
        prescriptions: prescriptions
    };

    axios.post(`http://127.0.0.1:8000/inspect/add?place=${place}&date=${date}&doctor=${doctor}&patient=${patient}&symptom=${symptom}&diagnosis=${diagnosis}&prescriptions=${prescriptions}`, data)
        .then(response => {
            alert("Block added successfully. Участок добавлен успешно.");
        })
        .catch(error => {
            alert("An error occurred. Возникла ошибка.");
        });
}


// Функция удаления осмотров

function inspect_delete() {
    const inspect_id = document.getElementById("delinspect").value;

    if (!inspect_id) {
        alert("Please enter inspect ID. Пожалуйста, введите ID осмотра.");
        return;
    }

    axios.delete(`http://127.0.0.1:8000/inspect/delete/${inspect_id}`)
        .then(response => {
            alert("Inspect deleted successfully. Осмотр удален успешно.");
        })
        .catch(error => {
            alert("An error occurred. Возникла ошибка.");
        });
    }
})