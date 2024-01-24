// Заполнение таблицы осмотров и полей выбора с загрузкой страницы

document.addEventListener("DOMContentLoaded", function () {
    axios.get("http://127.0.0.1:8000/inspect")
        .then(response => {
            const tableBody = document.querySelector("#inspect-table tbody");

            tableBody.innerHTML = "";

            response.data.inspect_choice.forEach(item => {
                const row = tableBody.insertRow();
                row.insertCell(0).textContent = item.id;
                row.insertCell(1).textContent = item.place;
                row.insertCell(2).textContent = item.date;
                row.insertCell(3).textContent = item.doctor;
                row.insertCell(4).textContent = item.patient;
                row.insertCell(5).textContent = item.symptom_id;
                row.insertCell(6).textContent = item.diagnosis_id;
                row.insertCell(7).textContent = item.prescriptions;
            });
        })
        .catch(error => {
            // console.error("Error fetching data:", error);
            alert("Error fetching data from database. Ошибка получения значений из базы данных.");
        });

    // axios.get('http://127.0.0.1:8000/inspect/choice_place')
    //     .then(function (response) {
    //         var options = response.data.map(function(inspect_choice_place) {
    //             return "<option value='" + inspect_choice_place.addplace + "'>" + inspect_choice_place.addplace + "</option>";
    //         });
    //         document.getElementById('addplace').innerHTML = options.join("");
    //     })
    //     .catch(function (error) {
    //         // console.error('Error:', error);
    //         alert("Error fetching data from database. Ошибка получения значений из базы данных. - choice_place");
    //     });

    // axios.get('http://127.0.0.1:8000/inspect/choice_doctor')
    //     .then(function (response) {
    //         var options = response.data.map(function(inspect_choice_doctor) {
    //             return "<option value='" + inspect_choice_doctor.adddoctor + "'>" + inspect_choice_doctor.adddoctor + "</option>";
    //         });
    //         document.getElementById('adddoctor').innerHTML = options.join("");
    //     })
    //     .catch(function (error) {
    //         // console.error('Error:', error);
    //         // alert("Error fetching data from database. Ошибка получения значений из базы данных. - choice_doctor");
    //     });
    
    // axios.get('http://127.0.0.1:8000/inspect/choice_patient')
    //     .then(function (response) {
    //         var options = response.data.map(function(inspect_choice_patient) {
    //             return "<option value='" + inspect_choice_patient.addpatient + "'>" + inspect_choice_patient.addpatient + "</option>";
    //         });
    //         document.getElementById('addpatient').innerHTML = options.join("");
    //     })
    //     .catch(function (error) {
    //         // console.error('Error:', error);
    //         // alert("Error fetching data from database. Ошибка получения значений из базы данных. - choice_patient");
    //     });

    // axios.get('http://127.0.0.1:8000/inspect/choice_symptom')
    //     .then(function (response) {
    //         var options = response.data.map(function(inspect_choice_symptom) {
    //             return "<option value='" + inspect_choice_symptom.addsymptom + "'>" + inspect_choice_symptom.addsymptom + "</option>";
    //         });
    //         document.getElementById('addsymptom').innerHTML = options.join("");
    //     })
    //     .catch(function (error) {
    //         // console.error('Error:', error);
    //         // alert("Error fetching data from database. Ошибка получения значений из базы данных. - choice_symptom");
    //     });

    // axios.get('http://127.0.0.1:8000/inspect/choice_diagnosis')
    //     .then(function (response) {
    //         var options = response.data.map(function(inspect_choice_diagnosis) {
    //             return "<option value='" + inspect_choice_diagnosis.adddiagnosis + "'>" + inspect_choice_diagnosis.adddiagnosis + "</option>";
    //         });
    //         document.getElementById('adddiagnosis').innerHTML = options.join("");
    //     })
    //     .catch(function (error) {
    //         // console.error('Error:', error);
    //         // alert("Error fetching data from database. Ошибка получения значений из базы данных. - choice_doctor");
    //     });
});


// // Заполнение полей для выбора с загрузкой страницы

// document.addEventListener('DOMContentLoaded', function () {
//     // Make a GET request to fetch data for the select options from the FastAPI endpoint
//     axios.get('http://127.0.0.1:8000/inspect/choice_place')
//         .then(function (response) {
//             var options = response.data.map(function(inspect_choice_place) {
//                 return "<option value='" + inspect_choice_place.addplace + "'>" + inspect_choice_place.addplace + "</option>";
//             });
//             document.getElementById('addplace').innerHTML = options.join("");
//         })
//         .catch(function (error) {
//             // console.error('Error:', error);
//             alert("Error fetching data from database. Ошибка получения значений из базы данных. - choice_place");
//         });

//     // Make a GET request to fetch data for the select options from the FastAPI endpoint
//     axios.get('http://127.0.0.1:8000/inspect/choice_doctor')
//         .then(function (response) {
//             // Populate the pet_name and pet_color select options with the received data
//             var petOptions = response.data.map(function (pet) {
//                 return "<option value='" + pet.pet_name + "'>" + pet.pet_name + "</option>";
//             });
//             var colorOptions = response.data.map(function (pet) {
//                 return "<option value='" + pet.pet_color + "'>" + pet.pet_color + "</option>";
//             });
//             document.getElementById('pet_name').innerHTML = petOptions.join("");
//             document.getElementById('pet_color').innerHTML = colorOptions.join("");
//         })
//         .catch(function (error) {
//             console.error('Error:', error);
//         });
// });



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

    axios.post("http://127.0.0.1:8000/inspect/add", data)
        .then(response => {
            // document.getElementById("response").textContent = JSON.stringify(response.data);
            alert("Block added successfully. Участок добавлен успешно.");
        })
        .catch(error => {
            // console.error("Error posting data:", error);
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

    axios.delete(`http://127.0.0.1:8000/inspect/delete/{id}?id=${inspect_id}`)
        .then(response => {
            alert("Inspect deleted successfully. Осмотр удален успешно.");
        })
        .catch(error => {
            // console.error("Error deleting user:", error);
            alert("An error occurred. Возникла ошибка.");
        });
}
