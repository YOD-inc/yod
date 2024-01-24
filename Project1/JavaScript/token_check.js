document.addEventListener("DOMContentLoaded", function () {
// Retrieve the access token from local storage
    const accessToken = localStorage.getItem('access_token');

    // Example: Make an authenticated GET request to a protected route
    axios.get('/protected', {
    headers: {
        Authorization: `Bearer ${accessToken}`
    }
    })
    .then((response) => {
    // Handle successful response from protected route
    console.log(response.data);
    })
    .catch((error) => {
    // Handle authentication errors or unauthorized access
    console.error('Error:', error);
    });
});