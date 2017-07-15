from flask import Flask, jsonify, request, redirect
from flask_cors import CORS, cross_origin

app = Flask(__name__)
CORS(app)

INF = 9999
PLAYER = 'O'
OPPONENT = 'X'
MAX_DEPTH = 10

@app.route('/')
def index():
    return redirect("http://hieusydo.com", code=302)

def is_move_left(board):
    for i in board:
        if i is None:
            return True
    return False

def evaluate(board):
    lines = [
        [0, 1, 2],
        [3, 4, 5],
        [6, 7, 8],
        [0, 3, 6],
        [1, 4, 7],
        [2, 5, 8],
        [0, 4, 8],
        [2, 4, 6],
    ]    
    for l in lines: 
        a, b, c = l
        if board[a] and board[a] == board[b] == board[c]:
            if board[a] == PLAYER:
                return 10
            elif board[a] == OPPONENT:
                return -10
    return 0

def minimax(board, depth, isMax, alpha, beta):
    score = evaluate(board)

    if depth == 0:
        return score

    if score == 10:
        return score
    if score == -10:
        return score
    if is_move_left(board) is False:
        return 0

    if isMax:
        best = -INF
        for i in xrange(len(board)):
            if board[i] is None: 
                board[i] = PLAYER
                val = minimax(board, depth-1, not isMax, alpha, beta)
                best = max(best, val)
                # Undo the move. The more appropriate way is 
                # to make a copy of the previous state
                # but this way suffices for a simple game like Tic-Tac-Toe  
                board[i] = None

                if best > alpha:
                    alpha = best
                if alpha >= beta:
                    break

        return best
    else: 
        best = INF
        for i in xrange(len(board)):
            if board[i] is None: 
                board[i] = OPPONENT
                val = minimax(board, depth-1, not isMax, alpha, beta)
                best = min(best, val)
                board[i] = None
                
                if best < beta:
                    beta = best
                if alpha >= beta:
                    break
                
        return best        

@app.route('/api/move', methods=['POST'])
def find_best_move():
    currState = request.json['squaresParam']
    bestVal = -INF
    bestMove = -1
    for i in xrange(len(currState)):
        if currState[i] is None: 
            currState[i] = PLAYER
            moveVal = minimax(currState, MAX_DEPTH, False, -INF, INF)
            currState[i] = None
            if moveVal > bestVal:
                bestMove = i
                bestVal = moveVal
    move = bestMove
    return jsonify(move=move)

if __name__ == '__main__':
    app.run(debug=True)