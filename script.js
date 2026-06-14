document.addEventListener("DOMContentLoaded", () => {
    // data.json se data read karna
    fetch('data.json')
        .then(response => response.json())
        .then(data => {
            document.getElementById('status').innerText = `${data.message} - Version: ${data.version}`;
        })
        .catch(err => {
            document.getElementById('status').innerText = "Failed to load data.json";
            console.error(err);
        });

    document.getElementById('btn').addEventListener('click', () => {
        alert("JavaScript is working perfectly!");
    });
});
