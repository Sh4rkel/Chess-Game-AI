let whiteTimer = 300; // 5 minutes
let blackTimer = 300; // 5 minutes
let currentPlayer = 'white';

function startTimer() {
    setInterval(() => {
        if (currentPlayer === 'white') {
            whiteTimer--;
            document.getElementById('white-timer').innerText = formatTime(whiteTimer);
            if (whiteTimer <= 0) {
                alert('Black wins!');
                resetGame();
            }
        } else {
            blackTimer--;
            document.getElementById('black-timer').innerText = formatTime(blackTimer);
            if (blackTimer <= 0) {
                alert('White wins!');
                resetGame();
            }
        }
    }, 1000);
}

function formatTime(seconds) {
    const minutes = Math.floor(seconds / 60);
    const secs = seconds % 60;
    return `${minutes}:${secs < 10 ? '0' : ''}${secs}`;
}

function allowDrop(ev) {
    ev.preventDefault();
}

function drag(ev) {
    ev.dataTransfer.setData('text', ev.target.id);
}

function drop(ev) {
    ev.preventDefault();
    const data = ev.dataTransfer.getData('text');
    let target = ev.target;
    if (target.tagName === 'IMG') {
        target = target.parentElement;
    }
    const piece = document.getElementById(data);
    target.appendChild(piece);

    const start_pos = data.slice(5);
    const end_pos = target.id.slice(4);

    const start_file = String.fromCharCode('a'.charCodeAt(0) + parseInt(start_pos[1]));
    const start_rank = (8 - parseInt(start_pos[0])).toString();
    const end_file = String.fromCharCode('a'.charCodeAt(0) + parseInt(end_pos[1]));
    const end_rank = (8 - parseInt(end_pos[0])).toString();

    const start_notation = start_file + start_rank;
    const end_notation = end_file + end_rank;

    fetch('/captured_pieces')
        .then(response => response.json())
        .then(data => {
            let promotion = null;
            if ((piece.alt === 'P' && end_rank === '8') || (piece.alt === 'p' && end_rank === '1')) {
                if (data.captured_pieces.length > 0) {
                    promotion = prompt(`Promote to (${data.captured_pieces.join(', ')}):`, data.captured_pieces[0]);
                }
            }

            fetch('/move', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json'
                },
                body: JSON.stringify({start_pos: start_notation, end_pos: end_notation, promotion: promotion})
            }).then(response => response.json()).then(data => {
                if (data.status === 'error') {
                    alert(data.message);
                } else {
                    document.body.innerHTML = data.board;
                    currentPlayer = currentPlayer === 'white' ? 'black' : 'white';
                }
            }).catch(error => {
                console.error('Fetch error:', error);
            });
        });
}

document.addEventListener('DOMContentLoaded', () => {
    startTimer();
});