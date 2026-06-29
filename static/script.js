const pieceMap = { 'P': '♙', 'R': '♖', 'N': '♘', 'B': '♗', 'Q': '♕', 'K': '♔', 'p': '♟', 'r': '♜', 'n': '♞', 'b': '♝', 'q': '♛', 'k': '♚' };

async function initBoard() {
    const boardEl = document.getElementById('board');
    // Fetch board state from Python
    const response = await fetch('/get-board');
    const data = await response.json(); // Expected format: string of 64 chars
    
    boardEl.innerHTML = '';
    for (let i = 0; i < 64; i++) {
        const square = document.createElement('div');
        square.className = `square ${(Math.floor(i/8) + i) % 2 === 0 ? 'light' : 'dark'}`;
        const char = data.board[i];
        if (char !== '.') {
            const piece = document.createElement('span');
            piece.className = `piece ${char === char.toUpperCase() ? 'white' : 'black'}`;
            piece.textContent = pieceMap[char] || '';
            square.appendChild(piece);
        }
        boardEl.appendChild(square);
    }
}
initBoard();
let selectedSquare = null;

async function handleSquareClick(index) {
    if (selectedSquare === null) {
        selectedSquare = index; // Select the piece
    } else {
        // Send move to Python (e.g., source index to target index)
        const response = await fetch('/make-move', {
            method: 'POST',
            headers: {'Content-Type': 'application/json'},
            body: JSON.stringify({from: selectedSquare, to: index})
        });
        const result = await response.json();
        if (result.success) {
            initBoard(); // Refresh board
        }
        selectedSquare = null; // Reset
    }
}