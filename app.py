from flask import Flask, render_template, jsonify, request
import chess

app = Flask(__name__)
board = chess.Board()

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/get-board')
def get_board():
    # board_fen() gives us the pieces. We replace empty squares with '.'
    # Then we convert the board into a 64-character string
    board_str = board.board_fen().split(' ')[0]
    board_str = board_str.replace('/', '')
    for i in range(1, 9):
        board_str = board_str.replace(str(i), '.' * i)
    return jsonify({"board": board_str})

@app.route('/make-move', methods=['POST'])
def make_move():
    data = request.json
    try:
        # Convert browser index (0-63, top-left is 0) to chess index (0-63, bottom-left is 0)
        from_sq = ((7 - (int(data['from']) // 8)) * 8) + (int(data['from']) % 8)
        to_sq = ((7 - (int(data['to']) // 8)) * 8) + (int(data['to']) % 8)
        
        move = chess.Move(from_sq, to_sq)
        
        # Auto-promote to Queen
        if board.piece_at(from_sq) and board.piece_at(from_sq).piece_type == chess.PAWN:
            if (to_sq // 8 == 0) or (to_sq // 8 == 7):
                move.promotion = chess.QUEEN
        
        if move in board.legal_moves:
            board.push(move)
            return jsonify({"success": True})
        return jsonify({"success": False, "error": "Illegal move"})
    except Exception as e:
        return jsonify({"success": False, "error": str(e)})

if __name__ == '__main__':
    app.run(debug=True)