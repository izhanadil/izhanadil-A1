from __future__ import annotations
from layer_store import SetLayerStore
from data_structures.referential_array import ArrayR

class Grid:
    DRAW_STYLE_SET = "SET"
    DRAW_STYLE_ADD = "ADD"
    DRAW_STYLE_SEQUENCE = "SEQUENCE"
    DRAW_STYLE_OPTIONS = (
        DRAW_STYLE_SET,
        DRAW_STYLE_ADD,
        DRAW_STYLE_SEQUENCE
    )

    DEFAULT_BRUSH_SIZE = 2 # The default brush size, set to 2
    MAX_BRUSH = 5 # The maximum brush size, set to 5
    MIN_BRUSH = 0 # The minimum brush size, set to 0

    def __init__(self, draw_style, x, y) -> None:
        """
        Initialise the grid object.
        - draw_style:
            The style with which colours will be drawn.
            Should be one of DRAW_STYLE_OPTIONS
            This draw style determines the LayerStore used on each grid square.
        - x, y: The dimensions of the grid.

        Should also intialise the brush size to the DEFAULT provided as a class variable.
        """
        # Check if the draw_style is valid
        if draw_style in Grid.DRAW_STYLE_OPTIONS:
            self.draw_style = draw_style
        else:
            raise ValueError("Invalid") # If draw_style is not valid, raise ValueError
        
        self.x = x # The x dimension of the grid
        self.y = y # The y dimension of the grid

        # Creating a 2D array with dimensions x and y and assigning a SetLayerStore object to each element of the grid
        self.grid = ArrayR(self.x)
        for i in range (self.x):
            self.grid[i] = ArrayR(self.y)
            for k in range (self.y):
                self.grid[i][k] = SetLayerStore() 

        self.brush_size = self.DEFAULT_BRUSH_SIZE # Assigning the default brush size to the brush_size variable

    def increase_brush_size(self):
        """
        Increases the size of the brush by 1,
        if the brush size is already MAX_BRUSH,
        then do nothing.
        """
        if self.brush_size != Grid.MAX_BRUSH: # Check if brush_size is not already equal to MAX_BRUSH
            self.brush_size = self.brush_size + 1 # Increase the brush size by 1

    def decrease_brush_size(self):
        """
        Decreases the size of the brush by 1,
        if the brush size is already MIN_BRUSH,
        then do nothing.
        """
        if self.brush_size != Grid.MIN_BRUSH: # Check if brush_size is not already equal to MIN_BRUSH
            self.brush_size = self.brush_size - 1 # Decrease the brush size by 1

    def special(self):
        """
        Activate the special affect on all grid squares.
        """
        # Loop through all the elements of the grid and activate the special effect
        for row in self.grid:
            for square in row:
                square.special()

    def __getitem__(self, index):
        """
        Overriding the __getitem__ method to allow direct indexing of the grid.
        """
        return self.grid[index] # Return the element of the grid at the given index
    
    def manhattan_distance(self, layer, x, y):
        # Set brush size to grid's current brush size
        brush = self.brush_size
        # Loop through cells surrounding the target cell
        for i in range(x-brush, x+brush+1):
            for j in range(y-brush, y+brush+1):
                # Check if the cell is within the brush range
                if abs(x - i) + abs(y - j) <= brush:
                    # Check if the cell is within the grid boundaries
                    if (0 <= i < self.x) and (0 <= j < self.y):
                        # Add the layer to the cell's layer store
                        self.grid[i][j].add(layer)

if __name__ == '__main__':
    grid = Grid(Grid.DRAW_STYLE_SET, 5, 5)
    print(grid.brush_size)
    grid.increase_brush_size()
    print(grid.brush_size)
    grid.increase_brush_size()
    print(grid.brush_size)
    grid.increase_brush_size()
    print(grid.brush_size)
    grid.increase_brush_size()
    print(grid.brush_size)
    grid.decrease_brush_size()
    print(grid.brush_size)
    grid.decrease_brush_size()
    print(grid.brush_size)
    grid.decrease_brush_size()
    print(grid.brush_size)
    grid.decrease_brush_size()
    print(grid.brush_size)
    grid.decrease_brush_size()
    print(grid.brush_size)
    grid.decrease_brush_size()
    print(grid.brush_size)