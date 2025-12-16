# Breakthrough - AI Board Game

A Python implementation of the abstract strategy board game **Breakthrough** with an intelligent AI opponent powered by the Minimax algorithm with Alpha-Beta pruning.

![Python Version](https://img.shields.io/badge/python-3.8%2B-blue)
![PyQt6](https://img.shields.io/badge/GUI-PyQt6-green)
![License](https://img.shields.io/badge/license-MIT-blue)

## Table of Contents
- [About the Game](#about-the-game)
- [Features](#features)
- [Installation](#installation)
- [How to Play](#how-to-play)
- [AI Algorithm: Alpha-Beta Pruning](#ai-algorithm-alpha-beta-pruning)
- [Project Structure](#project-structure)
- [Technical Details](#technical-details)

---

## About the Game

**Breakthrough** is a two-player abstract strategy board game invented by Dan Troyka in 2000. It's played on an 8×8 chess board where each player starts with 16 pawns arranged in the first two rows on opposite sides of the board.

### Game Rules

1. **Objective**: Be the first player to reach the opponent's home row (the opposite end of the board) with one of your pieces.

2. **Movement**: 
   - Pieces move one square forward (straight ahead or diagonally forward)
   - Diagonal moves can capture opponent pieces
   - Forward moves are only valid to empty squares
   - No backward movement is allowed

3. **Capturing**: 
   - Capture by moving diagonally forward onto an opponent's piece
   - Captured pieces are removed from the board

4. **Winning Conditions**:
   - Reach the opponent's home row with any piece
   - Opponent has no legal moves remaining

---

## Features

- **Intelligent AI Opponent**: Uses Minimax algorithm with Alpha-Beta pruning
- **Three Difficulty Levels**:
  - Easy (Depth 1): Quick decisions, beginner-friendly
  - Medium (Depth 3): Balanced challenge
  - Hard (Depth 5): Advanced strategy, longer think time
- **Visual Feedback**:
  - Highlighted valid moves
  - Last move indicators
  - AI thinking visualization
- **Performance Metrics**:
  - Real-time algorithm statistics
  - Nodes visited counter
  - Branching factor calculation
  - Position evaluation score
- **Randomized Starting Positions**: Players are randomly assigned White or Black

---

## Installation

### Prerequisites
- Python 3.8 or higher
- pip package manager

### Setup

1. Clone the repository:
```bash
git clone <repository-url>
cd breakthrough-game
```

2. Install dependencies:
```bash
pip install -r requirements.txt
```

3. Run the game:
```bash
python main.py
```

---

## How to Play

1. **Starting a Game**:
   - Launch the application
   - Select your desired difficulty level
   - You'll be randomly assigned White or Black pieces
   - White always moves first

2. **Making Moves**:
   - Click on one of your pieces to select it
   - Valid moves will be highlighted in green
   - Click on a highlighted square to move
   - The selected piece is shown with a blue highlight

3. **Game Interface**:
   - **Left Panel**: Game board and control buttons
   - **Right Panel**: AI performance metrics and settings
   - **Status Display**: Shows current turn and game state

4. **Winning**:
   - Get any of your pieces to the opponent's home row
   - Or eliminate all opponent moves

---

## AI Algorithm: Alpha-Beta Pruning

The AI opponent uses the **Minimax algorithm with Alpha-Beta pruning**, a decision-making algorithm commonly used in two-player games.

### Minimax Algorithm

The Minimax algorithm explores the game tree by:

1. **Maximizing Player**: Tries to maximize the position score
2. **Minimizing Player**: Tries to minimize the position score (opponent)
3. **Recursive Evaluation**: Explores moves to a specified depth
4. **Best Move Selection**: Chooses the move with the highest/lowest score

#### Pseudocode:
```
function minimax(state, depth, maximizing):
    if depth == 0 or game_over(state):
        return evaluate(state)
    
    if maximizing:
        max_eval = -∞
        for each move in valid_moves:
            eval = minimax(next_state, depth-1, false)
            max_eval = max(max_eval, eval)
        return max_eval
    else:
        min_eval = +∞
        for each move in valid_moves:
            eval = minimax(next_state, depth-1, true)
            min_eval = min(min_eval, eval)
        return min_eval
```

### Alpha-Beta Pruning Optimization

Alpha-Beta pruning significantly improves performance by eliminating branches that cannot affect the final decision.

#### Key Concepts:

- **Alpha (α)**: The best value the maximizer can guarantee
- **Beta (β)**: The best value the minimizer can guarantee
- **Pruning Condition**: When β ≤ α, remaining branches are pruned

#### How It Works:

1. **Alpha Cutoff**: 
   - In minimizing nodes, if the current value ≤ alpha, stop exploring siblings
   - The maximizer already has a better option elsewhere

2. **Beta Cutoff**:
   - In maximizing nodes, if the current value ≥ beta, stop exploring siblings
   - The minimizer already has a better option elsewhere

#### Pruning Example:
```
        Maximize
       /    |    \
      3     ?     2
     / \   / \   / \
    3   5 ?   ? 2   ?
```
- After finding 3 in the first branch
- And finding 2 in the third branch
- The middle branch's first node returns anything ≥ 3
- Since min(3, ?, 2) = 2, we can prune the middle branch
- We know it won't be chosen over the first branch (3)

#### Performance Benefits:

- **Best Case**: O(b^(d/2)) instead of O(b^d)
  - Where b = branching factor, d = depth
  - Effectively doubles the search depth
- **Typical Improvement**: 30-50% reduction in nodes visited
- **Move Ordering**: Better move ordering improves pruning efficiency

### Position Evaluation Function

The AI evaluates board positions using multiple factors:

1. **Material Count** (Weight: 100):
   - Number of pieces each player has
   - Direct comparison of piece count

2. **Advancement Bonus** (Weight: 10):
   - Rewards pieces closer to the opponent's home row
   - Encourages forward progress
   - Calculated as: distance_from_starting_row × weight

3. **Mobility** (Weight: 5):
   - Number of valid moves available
   - Higher mobility = better position
   - Difference: (player_moves - opponent_moves) × weight

4. **Win Detection** (Weight: 10,000):
   - Immediate win = +10,000
   - Immediate loss = -10,000

#### Evaluation Formula:
```
score = (player_material - opponent_material) × 100
      + (player_advancement - opponent_advancement) × 10
      + (player_mobility - opponent_mobility) × 5
```

### Algorithm Complexity

| Difficulty | Depth | Nodes (Avg) | Time Complexity | Space Complexity |
|------------|-------|-------------|-----------------|------------------|
| Easy       | 1     | ~100        | O(b)            | O(d)             |
| Medium     | 3     | ~10,000     | O(b³)           | O(d)             |
| Hard       | 5     | ~1,000,000  | O(b⁵)           | O(d)             |

*Where b ≈ 10-15 (average branching factor) and d = search depth*

### Implementation Highlights

```python
def _minimax(self, state, depth, alpha, beta, maximizing, original_player):
    # Terminal condition
    if depth == 0 or game_over(state):
        return evaluate(state), None
    
    if maximizing:
        max_eval = -∞
        for move in valid_moves:
            eval_score = minimax(next_state, depth-1, alpha, beta, False)
            max_eval = max(max_eval, eval_score)
            alpha = max(alpha, eval_score)
            
            # Alpha-Beta pruning
            if beta <= alpha:
                break  # Beta cutoff
        return max_eval
    else:
        min_eval = +∞
        for move in valid_moves:
            eval_score = minimax(next_state, depth-1, alpha, beta, True)
            min_eval = min(min_eval, eval_score)
            beta = min(beta, eval_score)
            
            # Alpha-Beta pruning
            if beta <= alpha:
                break  # Alpha cutoff
        return min_eval
```

---

## Project Structure

```
breakthrough-game/
├── main.py                 # Application entry point
├── requirements.txt        # Python dependencies
├── controller/            # Game logic controllers
│   ├── __init__.py
│   ├── game_controller.py # Main game flow control
│   ├── ai_controller.py   # AI move calculation (threaded)
│   └── ai_algorithm.py    # Minimax with Alpha-Beta pruning
├── model/                 # Game state and rules
│   ├── __init__.py
│   ├── game_state.py      # Board state management
│   ├── game_rules.py      # Game rules and win conditions
│   ├── move_validator.py  # Legal move validation
│   └── evaluator.py       # Position evaluation function
└── view/                  # PyQt6 GUI components
    ├── __init__.py
    ├── game_window.py     # Main window
    ├── board_view.py      # Board visualization
    ├── metrics_panel.py   # AI statistics display
    ├── difficulty_dialog.py # Difficulty selection
    └── styles.py          # UI styling constants
```

---

## Technical Details

### Architecture Pattern
- **MVC (Model-View-Controller)**: Separates game logic, UI, and control flow
- **Threading**: AI calculations run on separate thread to prevent UI freezing
- **Observer Pattern**: PyQt6 signals/slots for event handling

### Key Technologies
- **PyQt6**: Modern GUI framework for cross-platform desktop applications
- **Python Threading**: QThread for concurrent AI computation
- **Object-Oriented Design**: Clean separation of concerns

### Performance Optimizations
1. **Alpha-Beta Pruning**: Reduces search space by ~50%
2. **Move Ordering**: Evaluates promising moves first
3. **Shallow Evaluation**: Quick heuristic for deep nodes
4. **Threaded Computation**: Non-blocking AI thinking

### Evaluation Metrics Displayed
- **Search Depth**: How many moves ahead the AI looks
- **Nodes Visited**: Total game states evaluated
- **Execution Time**: Time taken for AI decision
- **Branching Factor**: Average number of moves per position
- **Complexity**: Estimated total states (O(b^d))
- **Position Score**: Current evaluation of the board
