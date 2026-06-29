from flask import Flask, render_template, jsonify, request
import chess

app = Flask(__name__)
board = chess.Board()

@app.route('/make-move', methods=['POST'])
def make_move():
    data = request.json
    try:
        # Convert index (0-63) to move format
        move = chess.Move(data['from'], data['to'])
        if move in board.legal_moves:
            board.push(move)
            return jsonify({"success": True})
        # Handle promotion logic here if needed
        return jsonify({"success": False})
    except:
        return jsonify({"success": False})

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/get-board')
def get_board():
    # Keep your existing logic here
    fen = board.board_fen().replace('/', '').replace('1', '.').replace('2', '..').replace('3', '...').replace('4', '....').replace('5', '.....').replace('6', '......').replace('7', '.......').replace('8', '........')
    return jsonify({"board": fen})

if __name__ == '__main__':
    app.run(debug=True)