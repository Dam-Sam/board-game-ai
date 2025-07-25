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

## 📸 Screenshots / Diagrams (optional)

> *You can add visuals here for board representations or search trees.*

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

# cd into the project
git clone https://github.com/Dam-Sam/board-game-ai.git
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
