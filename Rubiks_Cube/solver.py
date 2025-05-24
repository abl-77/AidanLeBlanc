from quad_cube import QuadCube
from priority_queue import PriorityQueue
import numpy as np

# Initialize colors for easier tracking
WHITE = "#f5f5f5"
BLUE = "#00008b"
ORANGE = "#ff6103"
GREEN = "#006400"
RED = "#8b0000"
YELLOW = "#e3cf57"

class Node:
    def __init__(self, cube, moves, parent=None):
        self.parent = parent
        self.cube = cube
        self.moves = moves
        self.score = cube.heuristic() + 10 * moves

class Solver:
    def __init__(self, cube):
        self.root = Node(cube, 0)
        self.solved = None

    def solve(self):
        leaves = PriorityQueue()
        leaves.add(self.root)
        while leaves.size > 0:
            current = leaves.pop()
            print(f"Current score: {current.score}, Number of moves to get here: {current.moves}")
            # current.cube.plot_cube()
            if current.score == 10 * current.moves:
                self.solved = current
                return
            children = self.get_children(current.cube)
            for child in children:
                node = Node(child, current.moves + 1, current)
                if current.score == 36 and current.moves == 2:
                    print(f"Node score: {node.score}, Number of moves to get here: {node.moves}")
                leaves.add(node)
                
    def solution_path(self):
        if not isinstance(self.solved, Node):
            return -1
        path = []
        current = self.solved

        while isinstance(current.parent, Node):
            path.append(current.cube)
            print(f"Solved score: {current.score}, Number of moves to get here: {current.moves}")
            current = current.parent

        path.append(current.cube)
        print(f"Solved score: {current.score}, Number of moves to get here: {current.moves}")
        return path[::-1]

    def get_children(self, cube):
        children = []
        for i in range(4):
            copy = QuadCube(cube)
            copy.rotate_row(i, "L")
            children.append(copy)

            copy = QuadCube(cube)
            copy.rotate_row(i, "R")
            children.append(copy)

            copy = QuadCube(cube)
            copy.rotate_col(i, "U")
            children.append(copy)

            copy = QuadCube(cube)
            copy.rotate_col(i, "D")
            children.append(copy)

            copy = QuadCube(cube)
            copy.rotate_slice(i, "CLOCK")
            children.append(copy)

            copy = QuadCube(cube)
            copy.rotate_slice(i, "COUNTER")
            children.append(copy)

        return children

if __name__ == "__main__":
    real_cube = np.array([[[ORANGE, ORANGE, ORANGE, ORANGE],
                     [WHITE, BLUE, BLUE, WHITE],
                     [WHITE, BLUE, BLUE, WHITE],
                     [WHITE, BLUE, BLUE, WHITE]],
                     [[BLUE, YELLOW, YELLOW, BLUE],
                     [BLUE, YELLOW, YELLOW, BLUE],
                     [BLUE, YELLOW, YELLOW, BLUE],
                     [BLUE, YELLOW, YELLOW, BLUE]],
                     [[ORANGE, ORANGE, ORANGE, YELLOW],
                     [ORANGE, ORANGE, ORANGE, GREEN],
                     [ORANGE, ORANGE, ORANGE, GREEN],
                     [ORANGE, ORANGE, ORANGE, YELLOW]],
                     [[GREEN, GREEN, GREEN, GREEN],
                     [WHITE, WHITE, WHITE, WHITE],
                     [WHITE, WHITE, WHITE, WHITE],
                     [GREEN, RED, RED, GREEN]],
                     [[WHITE, RED, RED, RED],
                     [BLUE, RED, RED, RED],
                     [BLUE, RED, RED, RED],
                     [WHITE, RED, RED, RED]],
                     [[YELLOW, GREEN, GREEN, YELLOW],
                     [YELLOW, GREEN, GREEN, YELLOW],
                     [YELLOW, GREEN, GREEN, YELLOW],
                     [RED, GREEN, GREEN, RED]]])
    c = QuadCube()
    c.rotate_row(0, "R")
    c.rotate_slice(2, "CLOCK")
    c.rotate_col(1, "D")
    # c.rotate_row(2, "R")
    # c.rotate_slice(2, "CLOCK")
    # c.rotate_col(3, "U")
    solver = Solver(c)
    solver.solve()
    path = solver.solution_path()
    for step in path:
        step.plot_cube()
