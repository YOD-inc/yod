// Функция для добавления пользователей

function add_test_user() {
    const last_name = document.getElementById("last_name").value;
    const first_name = document.getElementById("first_name").value;

    if (!last_name || !first_name) {
        alert("Please enter both last name and first name");
        return;
    }

    const data = {
        last_name: last_name,
        first_name: first_name
    };

    axios.post("http://127.0.0.1:8000/test_users/add", data)
        .then(response => {
            // document.getElementById("response").textContent = JSON.stringify(response.data);
            alert("User added successfully");
        })
        .catch(error => {
            // console.error("Error posting data:", error);
            alert("An error occurred");
        });
}

