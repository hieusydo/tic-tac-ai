from flask import Flask, jsonify, request
from flask_cors import CORS, cross_origin
from random import randint

app = Flask(__name__)
CORS(app)

INF = 9999
player = 'O'
opponent = 'X'
maxDepth = 10

@app.route('/')
def index():
    return 'Hello'

def isMoveLeft(board):
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
            if board[a] == player:
                return 10
            elif board[a] == opponent:
                return -10
    return 0

def minimax(board, depth, isMax):
    score = evaluate(board)
    if depth == 0:
        return score

    if score == 10:
        return score
    if score == -10:
        return score
    if isMoveLeft(board) is False:
        return 0

    if isMax:
        best = -INF
        for i in xrange(len(board)):
            if board[i] is None: 
                board[i] = player
                val = minimax(board, depth-1, not isMax)
                best = max(best, val)
                board[i] = None
        return best
    else: 
        best = INF
        for i in xrange(len(board)):
            if board[i] is None: 
                board[i] = opponent
                val = minimax(board, depth-1, not isMax)
                best = min(best, val)
                board[i] = None
        return best        

@app.route('/api/move', methods=['POST'])
def calculateComputerMove():
    currState = request.json['squaresParam']
    bestVal = -INF
    bestMove = -1
    print currState
    for i in xrange(len(currState)):
        if currState[i] is None: 
            currState[i] = player
            moveVal = minimax(currState, maxDepth, False)
            currState[i] = None
            if moveVal > bestVal:
                bestMove = i
                bestVal = moveVal
    move = bestMove
    return jsonify(move=move)

if __name__ == '__main__':
    app.run(debug=True)