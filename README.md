# Maze Pathfinding Visualization

A Python & Pygame application demonstrating three classic pathfinding algorithms—A\*, Breadth‑First Search (BFS), and Depth‑First Search (DFS)—on a randomly generated maze. Users can interactively adjust maze size, obstacle density, and algorithm parameters, then watch each solver animate in real time.

---

## 🎯 Features

* **Maze Generation**
  Random obstacle-based maze: fill rate controlled by `--obstacle_rate`. Guarantees solvability by retrying generation until a path exists.
* **Algorithms**

  * **A**\*: Optimal path with Manhattan-distance heuristic.
  * **BFS**: Guaranteed shortest path in unweighted grid.
  * **DFS**: Fast but not necessarily shortest.
* **Interactive Controls**

  * **[SPACE]**: Start / pause path animation
  * **[A] / [B] / [D]**: Switch to A\*/BFS/DFS solver
  * **[UP] / [DOWN]**: Increase / decrease animation speed
  * **[LEFT] / [RIGHT]**: Decrease / increase obstacle density
  * **[","] / ["."]**: Decrease / increase maze size
  * **[Left‑click] / [Right‑click]**: Set custom start / end (only on open cells)
  * **[R]**: Reset to a new random maze
  * **[Q]**: Quit application
* **Responsive Layout**
  Automatically scales cell size to fit current window dimensions.
* **Dynamic Sidebar**
  Clearly grouped sections:

  * **Maze Settings**: Size, obstacle rate
  * **Algorithm**: Current solver & status
  * **Performance**: Computation time
  * **Controls**: Key bindings reference

---

## 🚀 Installation

1. **Clone the repo**

   ```bash
   git clone https://github.com/kevinliu0605/maze_visualizer.git
   cd maze-visualizer
   ```
2. **Create a Python virtual environment**

   ```bash
   python3 -m venv venv
   source venv/bin/activate
   ```
3. **Install dependencies**

   ```bash
   pip install -r requirements.txt
   ```

> **Dependencies:**
>
> * Python 3.7+
> * [pygame](https://pypi.org/project/pygame/)

---

## ▶️ Usage

Run the main GUI script with optional parameters:

```bash
python main.py --size 20 --obstacle_rate 0.3
```

* `--size`: Number of cells per row/column (minimum 5, maximum 50). Default: 10.
* `--obstacle_rate`: Maze density between 0.0 (no walls) and 1.0 (all walls). Default: 0.2.

**Tip:** Resize the window to zoom in/out; the grid and sidebar will adjust automatically.

---

## 📂 Project Structure

```text
maze-visualizer/
├── main.py          # Pygame GUI and event loop
├── maze.py          # Maze generator with solvability check
├── algorithms.py    # bfs(), dfs(), astar() implementations
├── requirements.txt # pip dependencies
├── README.md        # This file
```

### maze.py

* `generate_maze(size: int, obstacle_rate: float) -> List[List[int]]`
  Creates a `size×size` grid of 0 (open) and 1 (wall) cells, ensuring at least one solution exists.
* `is_path_exist(maze: List[List[int]]) -> bool`
  Internal BFS check used during generation.

### algorithms.py

* `bfs(maze, start, end) -> (path, visited)`
  Finds shortest unweighted path, returns list of coordinates and set of visited cells.
* `dfs(maze, start, end) -> (path, visited)`
  Depth-first search; may not yield shortest path but explores quickly.
* `astar(maze, start, end) -> (path, visited)`
  Uses Manhattan-distance heuristic for efficient shortest-path computation.

*All solvers return a tuple `(path: List[Tuple[int,int]], visited: Set[Tuple[int,int]])`.*

---

*Developed by Hanwen Liu*
