// javascript functionality for the chess game
function allowDrop(ev) {
    ev.preventDefault();
}

function drag(ev) {
    ev.dataTransfer.setData('text', ev.target.id);
}

// Drop chess piece event handler function, this should be called when a piece is dropped on a cell. For now it works fine
// but it should be make it better, and eliminate the need of the piece color and current turn checks, and debug logs.
function drop(ev) {
    ev.preventDefault();
    const data = ev.dataTransfer.getData('text');
    let target = ev.target;
    if (target.tagName === 'IMG') {
        target = target.parentElement;
    }
    const piece = document.getElementById(data);
    const pieceColor = piece.alt === piece.alt.toUpperCase() ? 'white' : 'black';
    const current_turn = document.getElementById('current_turn').value;

    if ((target.children.length !== current_turn || (target.children.length > 0 && target.children[0].alt.toUpperCase() !== piece.alt.toUpperCase())) && pieceColor === current_turn) {
        if (target.children.length > 0 && target.children[0].alt.toUpperCase() !== piece.alt.toUpperCase() && target.children.length !== current_turn) {
            target.innerHTML = ''; // Remove the captured piece
        }
        target.appendChild(piece);
        const start_pos = data.slice(5);
        const end_pos = target.id.slice(4);

        const start_file = String.fromCharCode('a'.charCodeAt(0) + parseInt(start_pos[1]));
        const start_rank = (8 - parseInt(start_pos[0])).toString();
        const end_file = String.fromCharCode('a'.charCodeAt(0) + parseInt(end_pos[1]));
        const end_rank = (8 - parseInt(end_pos[0])).toString();

        const start_notation = start_file + start_rank;
        const end_notation = end_file + end_rank;

        let promotion_piece = 'q'; // Default to queen
        if ((piece.alt === 'P' && end_rank === '8') || (piece.alt === 'p' && end_rank === '1')) {
            promotion_piece = prompt("Promote to (q, r, b, n):", "q");
        }

        fetch('/move', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({start_pos: start_notation, end_pos: end_notation, promotion_piece: promotion_piece})
        }).then(response => response.json()).then(data => {
            if (data.status === 'error') {
                alert(data.message);
            } else {
                document.body.innerHTML = data.board;
            }
        }).catch(error => {
            console.error('Fetch error:', error);
        });
    }
}

// Reset the board to the initial state
function resetGame() {
    fetch('/reset', {
        method: 'POST'
    }).then(response => response.json()).then(data => {
        if (data.status === 'success') {
            document.body.innerHTML = data.board;
        } else {
            alert('Failed to reset the game');
        }
    }).catch(error => {
        console.error('Fetch error:', error);
    });
}