from heapq import heappush, heappop
from collections import deque

def bfs(maze, start, end):
    """
    Breadth-First Search (BFS) on a grid maze.
    Returns the shortest path from start to end (if one exists) and the set of all visited nodes.
    """
    # Initialize queue with tuple: (current_position, path_so_far)
    queue = deque([(start, [start])])
    # Keep track of visited positions to avoid revisiting
    visited = set([start])

    while queue:
        (x, y), path = queue.popleft()
        # If we've reached the end, return the path and visited set
        if (x, y) == end:
            return path, visited

        # Explore four neighboring cells (up, down, left, right)
        for dx, dy in [(-1, 0), (1, 0), (0, -1), (0, 1)]:
            nx, ny = x + dx, y + dy
            # Check bounds, open cell (0), and not yet visited
            if (0 <= nx < len(maze) and
                0 <= ny < len(maze[0]) and
                maze[nx][ny] == 0 and
                (nx, ny) not in visited):
                visited.add((nx, ny))                  # Mark as visited
                queue.append(((nx, ny), path + [(nx, ny)]))  # Enqueue with updated path

    # No path found
    return [], visited

def dfs(maze, start, end):
    """
    Depth-First Search (DFS) on a grid maze.
    Returns a path (not necessarily shortest) from start to end and the set of all visited nodes.
    """
    # Use a stack for DFS, each entry is (current_position, path_so_far)
    stack = [(start, [start])]
    visited = set([start])  # Track visited positions

    while stack:
        (x, y), path = stack.pop()
        # Check if we've reached the goal
        if (x, y) == end:
            return path, visited

        # Explore neighbors in the same order as BFS
        for dx, dy in [(-1, 0), (1, 0), (0, -1), (0, 1)]:
            nx, ny = x + dx, y + dy
            if (0 <= nx < len(maze) and
                0 <= ny < len(maze[0]) and
                maze[nx][ny] == 0 and
                (nx, ny) not in visited):
                visited.add((nx, ny))                   # Mark as visited
                stack.append(((nx, ny), path + [(nx, ny)]))  # Push onto stack

    # No path found
    return [], visited

def astar(maze, start, end):
    """
    A* Search on a grid maze.
    Returns the optimal path from start to end and the set of all nodes that were ever enqueued.
    """
    def heuristic(a, b):
        # Manhattan distance between two points
        return abs(a[0] - b[0]) + abs(a[1] - b[1])

    # Priority queue entries: (f_score, g_score, current_position, path_so_far)
    # f_score = g_score + heuristic estimate to goal
    heap = [(0 + heuristic(start, end), 0, start, [start])]
    # Keep track of the best g_score found so far for each position
    g_scores = {start: 0}

    while heap:
        f_score, cost, (x, y), path = heappop(heap)
        # If goal reached, return path and all positions ever visited
        if (x, y) == end:
            return path, g_scores.keys()

        # Explore neighbors
        for dx, dy in [(-1, 0), (1, 0), (0, -1), (0, 1)]:
            nx, ny = x + dx, y + dy
            if 0 <= nx < len(maze) and 0 <= ny < len(maze[0]) and maze[nx][ny] == 0:
                new_cost = cost + 1  # All moves cost 1 in a grid
                # If this path to neighbor is better than any previous one
                if (nx, ny) not in g_scores or new_cost < g_scores[(nx, ny)]:
                    g_scores[(nx, ny)] = new_cost
                    # Compute new priority = g + h
                    priority = new_cost + heuristic((nx, ny), end)
                    heappush(heap, (priority, new_cost, (nx, ny), path + [(nx, ny)]))

    # No path found
    return [], g_scores.keys()