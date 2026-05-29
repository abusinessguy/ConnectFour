# Connect Four with AI Player

A terminal-based Python implementation of Connect Four featuring human-vs-computer gameplay, move validation, win detection, and multiple AI strategies including a minimax-based opponent.

## Overview

This project implements the classic Connect Four game in Python. The game supports a human player against a computer-controlled opponent and includes several AI strategies, ranging from random moves to a minimax search with board evaluation.

The project was built as a way to practice game logic, search algorithms, and basic AI decision-making in a simple turn-based environment.

## Features

- 6-row by 7-column Connect Four board
- Human vs. AI gameplay
- Move validation for full or invalid columns
- Horizontal, vertical, and diagonal win detection
- Multiple computer-player strategies:
  - Random AI
  - Defensive AI
  - Offensive/defensive AI
  - Minimax AI
- Board evaluation function for scoring possible game states
- Undo functionality used during AI search
- Simple terminal interface

## AI Strategies

The project includes several levels of computer-player behavior:

### Random AI

Chooses any valid non-full column at random.

### Defensive AI

Checks whether the opponent has an immediate winning move and blocks it.

### Offensive/Defensive AI

First checks whether the AI can win immediately. If not, it checks whether the opponent needs to be blocked. If neither applies, it chooses randomly.

### Minimax AI

Uses recursive minimax search to evaluate future board positions and choose a stronger move. The evaluation function rewards central positions, vertical positioning, winning states, and penalizes dangerous opponent threats.

## How to Run

Install dependencies:

```bash
pip install numpy
