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
    console.log(`Piece color: ${pieceColor}, Current turn: ${current_turn}, Chi: ${target.children.length}`);
    if (target.children.length === 0 && pieceColor === current_turn) {
        target.appendChild(piece);
        const start_pos = data.slice(5);
        const end_pos = target.id.slice(4);

        // Convert cell IDs to chess notation
        const start_file = String.fromCharCode('a'.charCodeAt(0) + parseInt(start_pos[1]));
        const start_rank = (8 - parseInt(start_pos[0])).toString();
        const end_file = String.fromCharCode('a'.charCodeAt(0) + parseInt(end_pos[1]));
        const end_rank = (8 - parseInt(end_pos[0])).toString();

        const start_notation = start_file + start_rank;
        const end_notation = end_file + end_rank;

        console.log(`Dragging piece from ${start_notation}`); // Just debugging log, it will be removed when the app is finished
        console.log(`Dropping piece to ${end_notation}`); // same ass the upper log
        console.log(`Moving piece from ${start_notation} to ${end_notation}`); // idk, i put it for some cases
        fetch('/move', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({start_pos: start_notation, end_pos: end_notation})
        }).then(response => response.json()).then(data => {
            console.log(`Server response: ${JSON.stringify(data)}`);
            console.log(`Server status: ${data.status}`);
            if (data.status === 'error') {
                console.error(`Server error: ${data.message}`);
                alert(data.message);
            } else {
                console.log('Move successful');
                document.body.innerHTML = data.board;
            }
        }).catch(error => {
            console.error('Fetch error:', error);
        });
        console.log('Move request sent'); // debugging log, nothing important
    } else {
        console.log('Invalid move: target cell is not empty or wrong turn'); // debugging log, sometimes it's useful
    }
    console.log('Piece dropped'); // just kidding, it's a debugging log
}