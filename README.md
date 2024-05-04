## Description
A Monte Carlo Tree Search implementation for Othello. Two policies are used to guide the tree search according to Othello strategies.

**Component-Based Policy:** Evaluates game states using a linear combination of four heuristics:
  - Mobility: The amount of moves available to the player
  - Stability: The stability of the player's held positions
  - Corner Control: The player's control over the corners of the board
  - Square Parity: The proportion of squares held by player and opponent

The weights assigned to each heuristic adjust according to the stage of the game

**Weight-Table Policy:** Evaluates game states using a static weight table for positions on the board

## Sources
Game environment adapted from https://github.com/suragnair/alpha-zero-general

Base MCTS algorithm from https://github.com/kstruempf/MCTS/tree/main

Policy descriptions from https://courses.cs.washington.edu/courses/cse573/04au/Project/mini1/RUSSIA/Final_Paper.pdf
