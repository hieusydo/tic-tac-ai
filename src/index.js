import React from 'react';
import ReactDOM from 'react-dom';
import './index.css';

function Square(props) {
  return (
    <button className="square" onClick={props.onClick}>
      {props.value}
    </button>
  );
}

class Board extends React.Component {
  constructor() {
    super();
    this.state = {
      squares: Array(9).fill(null),
      humanTurn: true,
    };
  }

  // No Access control origin error: https://stackoverflow.com/a/20035319/3975668
  // Understanding CORS: https://www.html5rocks.com/en/tutorials/cors/
  // Using CORS in ReactJS: https://flask-cors.readthedocs.io/en/latest/
  calculateComputerMove(squares) {
    return fetch('http://dev.hieusydo.com/api/move' , {
      method: 'POST',
      headers: {
        'Accept': 'application/json',
        'Content-Type': 'application/json',
      },
      body: JSON.stringify({
        squaresParam: squares,
      })
    })
      .then((response) => response.json())
      .then((responseJson) => {
        if (calculateWinner(squares)) {return;}
        let chosenIdx = responseJson.move;
        squares[chosenIdx] = 'O';
        this.setState({
          squares: squares, 
          humanTurn: true,
        });       
      });      
  }

  handleClick(i) {
    const squares = this.state.squares.slice();
    // If someone has already won the game or if a square is already filled
    if (calculateWinner(squares) || squares[i]) {
      return;
    }
    
    if (this.state.humanTurn) {
      squares[i] =  'X';
      this.setState({
        squares: squares, 
        humanTurn: false,
      });      

      // Computer moves right away...
      this.calculateComputerMove(squares);
    } 
  }

  renderSquare(i) {
    return (
      <Square 
        value={this.state.squares[i]}
        onClick={() => this.handleClick(i)}
      />
    );
  }

  render() {
    const winner = calculateWinner(this.state.squares);
    let status;
    if (winner) {
      if (winner === 'Tie') {
        status = 'Tie';
      } else {
        status = 'Winner: ' + winner;
      }
    } else {
      status = 'Next player: ' + (this.state.humanTurn ? 'X' : 'O');
    }

    return (
      <div>
        <div className="status">{status}</div>
        <div className="board-row">
          {this.renderSquare(0)}
          {this.renderSquare(1)}
          {this.renderSquare(2)}
        </div>
        <div className="board-row">
          {this.renderSquare(3)}
          {this.renderSquare(4)}
          {this.renderSquare(5)}
        </div>
        <div className="board-row">
          {this.renderSquare(6)}
          {this.renderSquare(7)}
          {this.renderSquare(8)}
        </div>
      </div>
    );
  }
}

class Game extends React.Component {
  render() {
    return (
      <div className="game">
        <div className="game-board">
          <Board />
        </div>
        <div className="game-info">
          <div>{/* status */}</div>
          <ol>{/* TODO */}</ol>
        </div>
      </div>
    );
  }
}

// ========================================

ReactDOM.render(
  <Game />,
  document.getElementById('root')
);

function calculateWinner(squares) {
  const lines = [
    [0, 1, 2],
    [3, 4, 5],
    [6, 7, 8],
    [0, 3, 6],
    [1, 4, 7],
    [2, 5, 8],
    [0, 4, 8],
    [2, 4, 6],
  ];
  for (let i = 0; i < lines.length; i++) {
    const [a, b, c] = lines[i];
    if (squares[a] && squares[a] === squares[b] && squares[a] === squares[c]) {
      return squares[a];
    }
  }

  let allFill = true;
  for (let i = 0; i < squares.length; i++) {
    if (!squares[i]) {
      allFill = false;
    }
  }
  if (allFill) {
    return 'Tie';
  } 
  return null;
}
