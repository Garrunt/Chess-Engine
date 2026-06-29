const pieceMap = { 'P':'♙','R':'♖','N':'♘','B':'♗','Q':'♕','K':'♔','p':'♟','r':'♜','n':'♞','b':'♝','q':'♛','k':'♚' };
let selectedSquare = null;

async function initBoard() {
    const res = await fetch('/get-board');
    const data = await res.json();
    const boardEl = document.getElementById('board');
    boardEl.innerHTML = '';
    for (let i = 0; i < 64; i++) {
        const sq = document.createElement('div');
        sq.className = `square ${(Math.floor(i/8) + i) % 2 === 0 ? 'light' : 'dark'}`;
        const char = data.board[i];
        if (char !== '.') {
            const p = document.createElement('span');
            p.className = `piece ${char === char.toUpperCase() ? 'white' : 'black'}`;
            p.textContent = pieceMap[char];
            sq.appendChild(p);
        }
        sq.onclick = () => handleSquareClick(i);
        boardEl.appendChild(sq);
    }
}

async function handleSquareClick(i) {
    if (selectedSquare === null) { selectedSquare = i; } 
    else {
        const res = await fetch('/make-move', {
            method: 'POST', headers: {'Content-Type': 'application/json'},
            body: JSON.stringify({from: selectedSquare, to: i})
        });
        const result = await res.json();
        if (result.success) { await initBoard(); }
        selectedSquare = null;
    }
}
initBoard();