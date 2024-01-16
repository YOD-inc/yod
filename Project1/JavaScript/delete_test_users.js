// Функция удаления пользователей

function deleteUser() {
    const userId = document.getElementById("deleteId").value;

    if (!userId) {
        alert("Please enter a user ID");
        return;
    }

    axios.delete(`http://127.0.0.1:8000/test_users/delete/{id}?test_user_id=${userId}`)
        .then(response => {
            alert("User deleted successfully");
        })
        .catch(error => {
            // console.error("Error deleting user:", error);
            alert("An error occurred");
        });
}
