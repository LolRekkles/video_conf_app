document.addEventListener('DOMContentLoaded', function () {
    const chatForm = document.getElementById('chat-form');
    chatForm.addEventListener('submit', function (event) {
        event.preventDefault();

        const formData = new FormData(chatForm);
        fetch(chatForm.action, {
            method: 'POST',
            body: formData
        })
        .then(response => response.text())
        .then(data => {
            if (data === "Deepfake detected!") {
                alert(data);
            } else {
                const chatBox = document.getElementById('chat-box');
                const message = formData.get('message');
                const file = formData.get('file');
                
                if (message) {
                    chatBox.innerHTML += `<div>${message}</div>`;
                } else if (file) {
                    const filename = file.name;
                    chatBox.innerHTML += `<div><a href="/uploads/${filename}" target="_blank">${filename}</a></div>`;
                }
                
                chatForm.reset();
            }
        })
        .catch(error => console.error('Error:', error));
    });
});
