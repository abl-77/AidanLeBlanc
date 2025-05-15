import numpy as np
import pyvista as pv

# Initialize colors for easier tracking
WHITE = "#f5f5f5"
BLUE = "#00008b"
ORANGE = "#ff6103"
GREEN = "#006400"
RED = "#8b0000"
YELLOW = "#e3cf57"

colors = np.array([WHITE, BLUE, ORANGE, GREEN, RED, YELLOW])

'''
Sides are defined as follows
0 - Top
1 - Facing user
2 - Right side
3 - Opposite user
4 - Left side
5 - Bottom
'''

class QuadCube:
    def __init__(self, cube=None):
        '''
        Method to initialize a 4x4 cube object
        Can be represent a specific configuration or default a solved cube

        Params:
        cube - (Optional) np.ndarray object of shape (6, 4, 4)
        '''
        if isinstance(cube, np.ndarray):
            self.cube = cube
        else:
            self.cube = []
            for c in colors:
                self.cube.append([[c, c, c, c],
                                [c, c, c, c],
                                [c, c, c, c],
                                [c, c, c, c]])
            self.cube = np.array(self.cube)

    def rotate_clockwise(self, side):
        '''
        Helper method to rotate a specified side clockwise

        Params:
        side - index of the target side according to the specifications
        '''
        temp = np.array(self.cube[side, 0])
        self.cube[side, 0] = self.cube[side, :, 0][::-1]
        self.cube[side, :, 0] = self.cube[side, 3]
        self.cube[side, 3] = self.cube[side, :, 3][::-1]
        self.cube[side, :, 3] = temp

        mid_temp = np.array(self.cube[side, 1, 1:3])
        self.cube[side, 1:3, 1] = self.cube[side, 2, 1:3]
        self.cube[side, 1:3, 2] = mid_temp

    def rotate_counter(self, side):
        '''
        Helper method to rotate a specified side counterclockwise

        Params:
        side - index of the target side according to the specifications
        '''
        temp = np.array(self.cube[side, 0])
        self.cube[side, 0] = self.cube[side, :, 3]
        self.cube[side, :, 3] = self.cube[side, 3][::-1]
        self.cube[side, 3] = self.cube[side, :, 0]
        self.cube[side, :, 0] = temp[::-1]

        mid_temp = np.array(self.cube[side, 1, 1:3])
        self.cube[side, 1:3, 2] = self.cube[side, 2, 1:3][::-1]
        self.cube[side, 1:3, 1] = mid_temp[::-1]

    def rotate_row(self, row, direction):
        '''
        Possible move that rotates a given row left or right

        Params:
        row - index of the target row on the front face (1)
        direction - direction of rotation (left or right)
        '''
        if direction == "R":
            if row == 0:
                self.rotate_counter(0)
            if row == 3:
                self.rotate_clockwise(5)
            temp = np.array(self.cube[4, row])
            self.cube[4, row] = self.cube[3, row]
            self.cube[3, row] = self.cube[2, row]
            self.cube[2, row] = self.cube[1, row]
            self.cube[1, row] = temp
        elif direction == "L":
            if row == 0:
                self.rotate_clockwise(0)
            elif row == 3:
                self.rotate_counter(5)
            temp = np.array(self.cube[2, row])
            self.cube[2, row] = self.cube[3, row]
            self.cube[3, row] = self.cube[4, row]
            self.cube[4, row] = self.cube[1, row]
            self.cube[1, row] = temp

    def rotate_col(self, col, direction):
        '''
        Possible move that rotates a given column up or down

        Params:
        col - index of the target col on the front face (1)
        direction - direction of rotation (up or down)
        '''
        if direction == "U":
            if col == 0:
                self.rotate_counter(4)
            elif col == 3:
                self.rotate_clockwise(2)
            temp = np.array(self.cube[5, :, col])
            self.cube[5, :, col] = self.cube[3, :, 3 - col]
            self.cube[3, :, 3 - col] = self.cube[0, :, col][::-1]
            self.cube[0, :, col] = self.cube[1, :, col]
            self.cube[1, :, col] = temp
        elif direction == "D":
            if col == 0:
                self.rotate_clockwise(4)
            elif col == 3:
                self.rotate_counter(2)
            temp = np.array(self.cube[0, :, col])
            self.cube[0, :, col] = self.cube[3, :, 3 - col]
            self.cube[3, :, 3 - col] = self.cube[5, :, col][::-1]
            self.cube[5, :, col] = self.cube[1, :, col]
            self.cube[1, :, col] = temp

    def rotate_slice(self, slice, direction):
        '''
        Possible move that rotates a given slice clockwise or counterclockwise

        Params:
        slice - index of the target slice with the front face starting at 0
        direction - direction of rotation (clockwise or counterclockwise)
        '''
        if direction == "CLOCK":
            if slice == 0:
                self.rotate_clockwise(1)
            elif slice == 3:
                self.rotate_counter(3)
            temp = np.array(self.cube[0, 3 - slice])
            self.cube[0, 3 - slice] = self.cube[4, :, 3 - slice][::-1]
            self.cube[4, :, 3 - slice] = self.cube[5, slice]
            self.cube[5, slice] = self.cube[2, :, slice][::-1]
            self.cube[2, :, slice] = temp
        elif direction == "COUNTER":
            if slice == 0:
                self.rotate_counter(1)
            elif slice == 3:
                self.rotate_clockwise(3)
            temp = np.array(self.cube[0, 3 - slice])
            self.cube[0, 3 - slice] = self.cube[2, :, slice][::-1]
            self.cube[2, :, slice] = self.cube[5, slice]
            self.cube[5, slice] = self.cube[4, :, 3 - slice][::-1]
            self.cube[4, :, 3 - slice] = temp
        

    def plot_cube(self):
        '''
        Method to visualize the current cube configuration using pyvista
        '''
        p = pv.Plotter()
        for side in range(self.cube.shape[0]):
            for row in range(self.cube[side].shape[0]):
                for col in range(self.cube[side, row].shape[0]):
                    if side == 0:
                        center = [col + 0.5, 0, -4 + (row + 0.5)]
                        direction = [0.0, 1.0, 0.0]
                    elif side == 1:
                        center = [col + 0.5, -row - 0.5, 0]
                        direction = [0.0, 0.0, 1.0]
                    elif side == 2:
                        center = [4, -row - 0.5, -col - 0.5]
                        direction = [1.0, 0.0, 0.0]
                    elif side == 3:
                        center = [4 - (col + 0.5), -row - 0.5, -4]
                        direction = [0.0, 0.0, 1.0]
                    elif side == 4:
                        center = [0, -row - 0.5, -4 + (col + 0.5)]
                        direction = [1.0, 0.0, 0.0]
                    elif side == 5:
                        center = [col + 0.5, -4, -row - 0.5]
                        direction = [0.0, 1.0, 0.0]
                    
                    plane = pv.Plane(center=center, direction=direction, i_resolution=1, j_resolution=1)
                    p.add_mesh(plane, color=self.cube[side, row, col], show_edges=True, line_width=5)
        p.show()


if __name__=="__main__":
    cube = np.array([[[ORANGE, ORANGE, ORANGE, ORANGE],
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
    c = QuadCube(cube)
    c.plot_cube()
    c.rotate_slice(0, "COUNTER")
    c.plot_cube()
