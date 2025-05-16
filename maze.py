import random
from collections import deque

def generate_maze(size=10, obstacle_rate=0.2):
    """
    Generate a random maze of the given size where each cell has a chance to be an obstacle.
    Ensures there is at least one valid path from the top-left corner (start) to the
    bottom-right corner (end) by repeatedly regenerating until a path exists.
    
    Args:
        size (int): Number of rows and columns in the square maze.
        obstacle_rate (float): Probability that any given cell is an obstacle.
    
    Returns:
        list[list[int]]: A 2D list representing the maze (0 = free, 1 = obstacle).
    """
    while True:
        # Create a size×size grid: 1 = obstacle, 0 = free
        maze = [
            [1 if random.random() < obstacle_rate else 0 for _ in range(size)]
            for _ in range(size)
        ]
        # Guarantee start and end are open
        maze[0][0] = 0           # Start cell
        maze[-1][-1] = 0         # End cell

        # Verify solvability with BFS
        if is_path_exist(maze):
            return maze

def is_path_exist(maze):
    """
    Use Breadth-First Search (BFS) to check if there's a path from (0,0) to (n-1,n-1).
    
    Args:
        maze (list[list[int]]): 2D grid where 0 = free, 1 = obstacle.
    
    Returns:
        bool: True if a path exists, False otherwise.
    """
    size = len(maze)
    visited = [[False] * size for _ in range(size)]
    queue = deque([(0, 0)])
    visited[0][0] = True

    # Standard BFS loop
    while queue:
        x, y = queue.popleft()
        # Check if we've reached the goal
        if (x, y) == (size - 1, size - 1):
            return True

        # Explore four directions: up, down, left, right
        for dx, dy in [(-1, 0), (1, 0), (0, -1), (0, 1)]:
            nx, ny = x + dx, y + dy
            # Validate bounds, visit status, and obstacle check
            if (0 <= nx < size and
                0 <= ny < size and
                not visited[nx][ny] and
                maze[nx][ny] == 0):
                visited[nx][ny] = True
                queue.append((nx, ny))

    # No path found
    return False
