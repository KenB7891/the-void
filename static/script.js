const YELL_TIMEOUT = 30; // seconds
const PEEK_TIMEOUT = 15; // seconds

function canYell() {
    const lastYell = localStorage.getItem('lastYellTime');
    if (!lastYell) {
        return true;
    }
    
    const yellTimePassed = Math.floor(Date.now() / 1000) - parseInt(lastYell);
    return yellTimePassed >= YELL_TIMEOUT;
}

function updateYellTime() {
    localStorage.setItem('lastYellTime', Math.floor(Date.now() / 1000));
}

function canPeek() {
    const lastPeek = localStorage.getItem('lastPeekTime');
    if (!lastPeek) {
        return true;
    }

    const peekTimePassed = Math.floor(Date.now() / 1000) - parseInt(lastPeek);
    return peekTimePassed >= PEEK_TIMEOUT;
}

function updatePeekTime() {
    localStorage.setItem('lastPeekTime', Math.floor(Date.now() / 1000));
}

document.getElementById('yell-btn').addEventListener('click', function() {
    document.getElementById('yell-section').style.display = 'block';
});

document.getElementById('peek-btn').addEventListener('click', function() {
    
    if (!canPeek()) {
        alert(`You must wait ${PEEK_TIMEOUT} before peeking into The Abyss again!`);
        return;
    }

    updatePeekTime();
    
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

    if (!canYell()) {
        alert(`You must wait ${YELL_TIMEOUT} seconds before yelling into The Void again!`);
        return;
    }

    updateYellTime();

    fetch('/yell', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
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