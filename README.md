# 🧠 AI Search Algorithms for Games

AI solvers for classic board games including **Hua Rong Dao**, **Checkers**, and **Battleship Solitaire**, built using Python and core AI algorithms like A\*, DFS, Minimax, and CSP with Arc Consistency. Developed as part of a 3rd-year Artificial Intelligence course at the University of Toronto.

> 🎯 Combines search strategies, adversarial planning, and constraint satisfaction to solve deterministic logic-based games.

---

## 🚀 Features

* 🔍 **Search-Based Solvers**: Implements A\* and DFS to solve sliding puzzles (Hua Rong Dao)
* 🧠 **Game AI Agents**: Uses Minimax and Alpha-Beta pruning to simulate endgame Checkers with optimal play
* 📐 **Constraint Satisfaction Engine**: Solves Battleship Solitaire using CSP techniques with AC-3, forward checking, and backtracking

---

## 🧱 Tech Stack

| Language | Libraries & Algorithms      | Concepts                    |
| -------- | --------------------------- | --------------------------- |
| Python   | heapq, itertools, copy, sys | A\*, DFS, Minimax, CSP, GAC |

---

## 🔍 Project Overview

This project was part of the "Introduction to Artificial Intelligence" course and required applying classical AI algorithms to practical game-solving tasks. Each assignment targeted a different AI domain:

* **Hua Rong Dao (Sliding Block Puzzle)**: Apply uninformed (DFS) and informed (A\*) search to find solutions from initial to goal states. Focus on optimality, pathfinding, and heuristic design.
* **Checkers Endgame Solver**: Use adversarial planning with Minimax and Alpha-Beta pruning to compute optimal sequences of moves in deterministic win states.
* **Battleship CSP Solver**: Model the puzzle as a CSP and solve it with constraint propagation (AC-3), backtracking, and domain-reducing heuristics (MRV, LCV).

All algorithms were implemented from scratch and optimized for correctness, efficiency, and generalizability.

---

## 📊 Performance & Benchmarks

* 🔁 **Sliding Puzzle (Hua Rong Dao)**: Solves complex configurations in under 20 seconds using optimized A\* with custom heuristics
* 🧠 **Checkers AI**: Reduced move computation by 5x using alpha-beta pruning
* 📏 **Battleship Solver**: Solves medium-size grids with full fleet layout using AC-3 and MRV heuristics

---

## 📸 Screenshots / Diagrams
### Hua Rong Dao
```
11.^  
112v  
.^<>  
2v<>  
22<>
```
* 1 denotes 2x2 piece
* 2 denotes 1x1 piece
* <> denotes 1x2 horizontal piece
* ^v denotes 1x2 vertical piece
* . denotes empty space

### Checkers
```
........  
....b...  
.......R  
..b.b...  
...b...r  
........  
...r....  
....B...
```
* . (the period character) denotes an empty square
* r denotes a red piece
* b denotes a black piece
* R denotes a red king
* B denotes a black king

### Battleship Solitaire
INPUT FILE:  
```
211222  
140212  
32100  
000000  
0000S0  
000000  
000000  
00000.  
000000
```
* The first line describes the row constraints as a string of N numbers.
* The second line describes the column constraints as a string of N numbers.
* The third line describes the number of each type of ship.
* The remaining lines will be an NxN grid representing the initial layout of the puzzle.
  * 0 represents no hint for that square
  * S represents a submarine
  * . represents water


OUTPUT FILE (Solved Board):  
```
<>....  
....S.  
.^....  
.M...S  
.v.^..  
...v.S
```
* < represents the left end of a horizontal ship
* \> represents the right end of a horizontal ship
* ^ represents the top end of a vertical ship
* v (lower-cased letter v) represents the bottom end of a vertical ship
* M represents a middle segment of a ship (horizontal or vertical)

---

## 🧠 What I Learned

* Gained deep hands-on experience implementing AI algorithms including A\*, DFS, Minimax, Alpha-Beta Pruning, CSP, and Arc Consistency (AC-3)
* Learned how to design heuristics and evaluation functions tailored to specific problem domains
* Developed a strong grasp of game theory concepts like optimality, adversarial search, and utility evaluation
* Understood the power of constraint propagation in reducing problem complexity for combinatorial puzzles

---

## 🏁 How to Run Locally

```bash
# clone the repo
https://github.com/Dam-Sam/board-game-ai.git
cd board-game-ai

# Run one of the solvers (examples):
python3 hrd.py --algo astar --inputfile inputs/hrd1.txt --outputfile outputs/hrd1_solved.txt
python3 checkers.py < input.txt > output.txt
python3 Battleship/battle.py < input.txt > output.txt
```

> Some files may require formatted input files in a specific structure. See repo for details.

---

## 🤝 Collaboration & Credits

Solo project as part of CSC384 - Introduction to Artificial Intelligence (University of Toronto).&#x20;

Authored by Sam Zhang.

---

## 🔗 Links

* [🔗 GitHub Repository](https://github.com/Dam-Sam/board-game-ai)
* [📄 Assignment Report (Summary)](AI%20Search%20Algorithms%20For%20Games.md)
* [📄 Resume](https://linkedin.com/in/ssam-zhang)

---
