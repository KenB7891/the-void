document.getElementById('yell-btn').addEventListener('click', function() {
    document.getElementById('yell-section').style.display = 'block';
});

document.getElementById('peek-btn').addEventListener('click', function() {
    fetch('/peek')
        .then(response => response.json())
        .then(data => {
            document.getElementById('peek-message').innerText = data.message || "The Abyss is currently empty.";
        })
        .catch(error => {
            document.getElementById('peek-message').innerText = "Error peeking into The Abyss.";
        });
});

document.getElementById('send-yell').addEventListener('click', function() {
    const message = document.getElementById('yell-message').value;

    fetch('/yell', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
        },
        body: JSON.stringify({message: message})
    })
        .then(response => response.json())
        .then(data => {
            alert(data.status);
            document.getElementById('yell-message').value = '';
            document.getElementById('yell-section').style.display = 'none';
        })
        .catch(error => {
            alert('Error reaching The Void.');
        });
});