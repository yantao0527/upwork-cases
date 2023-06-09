'use client'

import { useState } from 'react'

function isFilled(value: string) {
  return value === 'X' || value === 'O'
}

function Square({
  value,
  onSquareClick,
}: {
  value: string
  onSquareClick: Function
}) {
  let color =
    value === 'X' || value === 'O' ? 'text-slate-900' : 'text-slate-50'

  return (
    <button className={color} onClick={() => onSquareClick()}>
      {value}
    </button>
  )
}

function Board({
  xIsNext,
  squares,
  onPlay,
}: {
  xIsNext: boolean
  squares: string[]
  onPlay: Function
}) {
  function handleClick(i) {
    console.log(squares[i])
    if (calculateWinner(squares) || squares[i] === 'X' || squares[i] === 'O') {
      return
    }
    const nextSquares = squares.slice()
    if (xIsNext) {
      nextSquares[i] = 'X'
    } else {
      nextSquares[i] = 'O'
    }
    onPlay(nextSquares)
  }

  const winner = calculateWinner(squares)
  let status
  if (winner) {
    status = 'Winner: ' + winner
  } else {
    status = 'Next player: ' + (xIsNext ? 'X' : 'O')
  }

  return (
    <section className="p-5">
      <div className="status text-2xl">{status}</div>
      <div className="relative flex justify-center">
        <div
          className="board m-4 grid grid-cols-3 outline outline-1"
          id="board"
        >
          <div
            id="0"
            className="cell flex h-20 w-20 items-center justify-center text-3xl md:h-32 md:w-32"
          >
            <Square value={squares[0]} onSquareClick={() => handleClick(0)} />
          </div>
          <div
            id="1"
            className="cell flex h-20 w-20 items-center justify-center border-x border-black text-3xl md:h-32 md:w-32"
          >
            <Square value={squares[1]} onSquareClick={() => handleClick(1)} />
          </div>
          <div
            id="2"
            className="cell flex h-20 w-20 items-center justify-center text-3xl md:h-32 md:w-32"
          >
            <Square value={squares[2]} onSquareClick={() => handleClick(2)} />
          </div>
          <div
            id="3"
            className="cell flex h-20 w-20 items-center justify-center border-y border-black text-3xl md:h-32 md:w-32"
          >
            <Square value={squares[3]} onSquareClick={() => handleClick(3)} />
          </div>
          <div
            id="4"
            className="cell flex h-20 w-20 items-center justify-center border border-black text-3xl md:h-32 md:w-32"
          >
            <Square value={squares[4]} onSquareClick={() => handleClick(4)} />
          </div>
          <div
            id="5"
            className="cell flex h-20 w-20 items-center justify-center border-y border-black text-3xl md:h-32 md:w-32"
          >
            <Square value={squares[5]} onSquareClick={() => handleClick(5)} />
          </div>
          <div
            id="6"
            className="cell flex h-20 w-20 items-center justify-center text-3xl md:h-32 md:w-32"
          >
            <Square value={squares[6]} onSquareClick={() => handleClick(6)} />
          </div>
          <div
            id="7"
            className="cell flex h-20 w-20 items-center justify-center border-x border-black text-3xl md:h-32 md:w-32"
          >
            <Square value={squares[7]} onSquareClick={() => handleClick(7)} />
          </div>
          <div
            id="8"
            className="cell flex h-20 w-20 items-center justify-center text-3xl md:h-32 md:w-32"
          >
            <Square value={squares[8]} onSquareClick={() => handleClick(8)} />
          </div>
        </div>
      </div>
    </section>
  )
}

function Game() {
  const [history, setHistory] = useState([
    ['1', '2', '3', '4', '5', '6', '7', '8', '9'],
  ])
  const [currentMove, setCurrentMove] = useState(0)
  const xIsNext = currentMove % 2 === 0
  const currentSquares = history[currentMove]

  function handlePlay(nextSquares: string[]) {
    const nextHistory = [...history.slice(0, currentMove + 1), nextSquares]
    setHistory(nextHistory)
    setCurrentMove(nextHistory.length - 1)
  }

  function jumpTo(nextMove: number) {
    setCurrentMove(nextMove)
    const nextHistory = history.slice(0, nextMove + 1)
    setHistory(nextHistory)
  }

  const moves = history.map((squares, move) => {
    let description
    if (move > 0) {
      description = 'Go to move #' + move
    } else {
      description = 'Go to game start'
    }
    return (
      <li key={move}>
        <button onClick={() => jumpTo(move)}>{description}</button>
      </li>
    )
  })

  return (
    <div className="game flex justify-center">
      <div className="game-board">
        <Board xIsNext={xIsNext} squares={currentSquares} onPlay={handlePlay} />
      </div>
      <div className="game-info p-10 text-2xl">
        <ol>{moves}</ol>
      </div>
    </div>
  )
}

export default function Home() {
  return (
    <main className="min-h-screen p-12">
      <Game />
    </main>
  )
}

function calculateWinner(squares: string[]) {
  const lines = [
    [0, 1, 2],
    [3, 4, 5],
    [6, 7, 8],
    [0, 3, 6],
    [1, 4, 7],
    [2, 5, 8],
    [0, 4, 8],
    [2, 4, 6],
  ]
  for (let i = 0; i < lines.length; i++) {
    const [a, b, c] = lines[i]
    if (squares[a] && squares[a] === squares[b] && squares[a] === squares[c]) {
      return squares[a]
    }
  }
  return null
}
