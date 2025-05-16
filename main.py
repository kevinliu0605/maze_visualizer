import pygame
import sys
import argparse
import time
from maze import generate_maze
from algorithms import bfs, dfs, astar

# Parse command-line arguments for initial maze size and obstacle rate
def parse_args():
    parser = argparse.ArgumentParser(description="Maze Pathfinding Visualization")
    parser.add_argument('--size', type=int, default=10,
                        help='Initial number of cells per row/column')
    parser.add_argument('--obstacle_rate', type=float, default=0.2,
                        help='Initial probability of an obstacle in each cell')
    return parser.parse_args()

# Read user inputs
args = parse_args()
DEFAULT_SIZE = args.size
DEFAULT_OBSTACLE_RATE = args.obstacle_rate
SIDEBAR_WIDTH = 200  # Sidebar width in pixels

# Display colors
COLORS = {
    'background': (255, 255, 255),
    'grid':       (200, 200, 200),
    'wall':       (0, 0, 0),
    'path':       (0, 150, 0),
    'ball':       (0, 200, 0),
    'explored':   (220, 220, 220),
    'start':      (255, 0, 0),
    'end':        (0, 0, 255),
    'sidebar_bg': (240, 240, 240),
    'text':       (20, 20, 20)
}

class MazeGame:
    def __init__(self):
        pygame.init()
        self.size = DEFAULT_SIZE
        self.obstacle_rate = DEFAULT_OBSTACLE_RATE
        self.clock = pygame.time.Clock()
        self.font = pygame.font.SysFont('Arial', 20)
        self.running = False
        self.step = 0
        self.speed = 10
        self.last_runtime = 0.0
        self.start_pt = (0, 0)
        self.end_pt = (self.size - 1, self.size - 1)
        self.path = []
        self.explored = set()
        self.algorithm = 'A*'
        self.width, self.height = 900, 600
        self.screen = pygame.display.set_mode((self.width, self.height), pygame.RESIZABLE)
        pygame.display.set_caption(
            f"Maze Pathfinding (Size={self.size}, ObsRate={self.obstacle_rate:.2f})"
        )
        self.reset_game()

    def calculate_path(self):
        start_time = time.perf_counter()
        if self.algorithm == 'A*':
            self.path, self.explored = astar(self.maze, self.start_pt, self.end_pt)
        elif self.algorithm == 'BFS':
            self.path, self.explored = bfs(self.maze, self.start_pt, self.end_pt)
        else:
            self.path, self.explored = dfs(self.maze, self.start_pt, self.end_pt)
        self.last_runtime = time.perf_counter() - start_time
        self.step = 0

    def reset_game(self):
        self.maze = generate_maze(self.size, self.obstacle_rate)
        self.path = []
        self.explored = set()
        self.running = False
        self.step = 0
        pygame.display.set_caption(
            f"Maze Pathfinding (Size={self.size}, ObsRate={self.obstacle_rate:.2f})"
        )

    def draw(self):
        self.width, self.height = self.screen.get_size()
        maze_w = self.width - SIDEBAR_WIDTH
        maze_h = self.height
        cell_size = int(min(maze_w / self.size, maze_h / self.size))
        grid_w = max(1, cell_size // 20)
        path_w = max(2, cell_size // 8)
        ball_r = max(2, cell_size // 4)
        hl = max(1, cell_size // 10)

        # Draw background
        self.screen.fill(COLORS['sidebar_bg'])
        pygame.draw.rect(
            self.screen, COLORS['background'],
            (0, 0, cell_size * self.size, cell_size * self.size)
        )
        # Draw grid
        for i in range(self.size + 1):
            pygame.draw.line(
                self.screen, COLORS['grid'],
                (0, i * cell_size), (cell_size * self.size, i * cell_size), grid_w
            )
            pygame.draw.line(
                self.screen, COLORS['grid'],
                (i * cell_size, 0), (i * cell_size, cell_size * self.size), grid_w
            )
        # Draw walls and explored
        for r in range(self.size):
            for c in range(self.size):
                rect = pygame.Rect(c * cell_size, r * cell_size, cell_size, cell_size)
                if self.maze[r][c] == 1:
                    pygame.draw.rect(self.screen, COLORS['wall'], rect)
                elif (r, c) in self.explored:
                    pygame.draw.rect(self.screen, COLORS['explored'], rect)
        # Draw path
        if self.step > 1:
            points = [
                (c * cell_size + cell_size // 2,
                 r * cell_size + cell_size // 2)
                for (r, c) in self.path[:self.step]
            ]
            pygame.draw.lines(
                self.screen, COLORS['path'], False, points, path_w
            )
        # Draw ball
        br, bc = self.start_pt if not self.running or self.step == 0 else self.path[self.step - 1]
        pygame.draw.circle(
            self.screen, COLORS['ball'],
            (bc * cell_size + cell_size // 2,
             br * cell_size + cell_size // 2), ball_r
        )
        # Highlight start/end
        for pt, col in [(self.start_pt, COLORS['start']), (self.end_pt, COLORS['end'])]:
            rr, cc = pt
            pygame.draw.rect(
                self.screen, col,
                pygame.Rect(
                    cc * cell_size + hl,
                    rr * cell_size + hl,
                    cell_size - 2 * hl,
                    cell_size - 2 * hl
                ), hl
            )
        # Draw sidebar
        self.draw_sidebar(cell_size)
        pygame.display.flip()

    def draw_sidebar(self, cell_size):
        x0 = cell_size * self.size + 10
        y = 10
        # Section: Maze Settings
        header = self.font.render("Maze Settings", True, COLORS['text'])
        self.screen.blit(header, (x0, y)); y += header.get_height() + 5
        settings = [
            f"Size: {self.size}",
            f"ObsRate: {self.obstacle_rate:.2f}"
        ]
        for line in settings:
            surf = self.font.render(line, True, COLORS['text'])
            self.screen.blit(surf, (x0 + 10, y)); y += surf.get_height() + 3
        y += 5
        # Section: Algorithm
        header = self.font.render("Algorithm", True, COLORS['text'])
        self.screen.blit(header, (x0, y)); y += header.get_height() + 5
        algo_info = [
            f"Algo: {self.algorithm}",
            f"Running: {self.running}",
            f"Step: {self.step}/{len(self.path)}",
            f"Speed: {self.speed} spd",
            f"Time: {self.last_runtime:.6f}s"
        ]
        for line in algo_info:
            surf = self.font.render(line, True, COLORS['text'])
            self.screen.blit(surf, (x0 + 10, y)); y += surf.get_height() + 3
        y += 5
        # Section: Controls
        header = self.font.render("Controls", True, COLORS['text'])
        self.screen.blit(header, (x0, y)); y += header.get_height() + 5
        controls = [
            "[SPACE]: start/pause",
            "[A]/[B]/[D]: select algo",
            "[UP]/[DOWN]: speed +/-",
            "[LEFT]/[RIGHT]: density +/-",
            "[<],[>]: size +/-",
            "[LeftClick]: set start",
            "[RightClick]: set end",
            "[R]: regenerate maze",
            "[Q]: quit"
        ]
        for line in controls:
            surf = self.font.render(f"• {line}", True, COLORS['text'])
            self.screen.blit(surf, (x0 + 10, y)); y += surf.get_height() + 3

    def run(self):
        while True:
            self.width, self.height = self.screen.get_size()
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit(); sys.exit()
                elif event.type == pygame.KEYDOWN:
                    key = event.key
                    if key == pygame.K_q:
                        pygame.quit(); sys.exit()
                    elif key == pygame.K_r: 
                        self.reset_game()
                    elif key == pygame.K_SPACE:
                        if not self.running and not self.path:
                            self.calculate_path()
                        self.running = not self.running
                    elif key in (pygame.K_a, pygame.K_b, pygame.K_d):
                        self.algorithm = {'a':'A*','b':'BFS','d':'DFS'}[pygame.key.name(key)]
                        if self.running:
                            self.calculate_path()
                    elif key == pygame.K_UP: 
                        self.speed = min(self.speed + 1, 60)
                    elif key == pygame.K_DOWN: 
                        self.speed = max(self.speed - 1, 1)
                    elif key == pygame.K_LEFT:
                        self.obstacle_rate = max(self.obstacle_rate - 0.05, 0.0); self.reset_game()
                    elif key == pygame.K_RIGHT:
                        self.obstacle_rate = min(self.obstacle_rate + 0.05, 1.0); self.reset_game()
                    elif key in (pygame.K_COMMA, pygame.K_LESS):
                        self.size = max(self.size - 1, 5); self.reset_game()
                    elif key in (pygame.K_PERIOD, pygame.K_GREATER):
                        self.size = min(self.size + 1, 50); self.reset_game()
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    mx, my = event.pos
                    cell_size = min((self.width - SIDEBAR_WIDTH) / self.size,
                                     self.height / self.size)
                    if mx < cell_size * self.size and my < cell_size * self.size:
                        r, c = int(my // cell_size), int(mx // cell_size)
                        if self.maze[r][c] == 0:
                            if event.button == 1: self.start_pt = (r, c)
                            elif event.button == 3: self.end_pt = (r, c)
                            self.running = False; self.path = []; self.step = 0
            if self.running and self.step < len(self.path):
                self.step += 1; self.clock.tick(self.speed)
            self.draw()

if __name__ == '__main__':
    MazeGame().run()