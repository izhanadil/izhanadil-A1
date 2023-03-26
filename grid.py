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

    DEFAULT_BRUSH_SIZE = 2
    MAX_BRUSH = 5
    MIN_BRUSH = 0

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
        #raise NotImplementedError()

        # if draw_style in Grid.DRAW_STYLE_OPTIONS:
        #     self.draw_style = draw_style
        # else:
        #     raise ValueError("Invalid")
        
        self.x = x
        self.y = y
        
        self.grid = ArrayR(self.x)
        for i in range (self.x):
            self.grid[i] = ArrayR(self.y)
            for k in range (self.y):
                self.grid[i][k] = SetLayerStore() 

        
        self.brush_size = self.DEFAULT_BRUSH_SIZE

    def increase_brush_size(self):
        """
        Increases the size of the brush by 1,
        if the brush size is already MAX_BRUSH,
        then do nothing.
        """
       # raise NotImplementedError()
       # self.brush_size = min(self.brush_size + 1, self.MAX_BRUSH)
        if self.brush_size != Grid.MAX_BRUSH:
            self.brush_size = self.brush_size + 1



    def decrease_brush_size(self):
        """
        Decreases the size of the brush by 1,
        if the brush size is already MIN_BRUSH,
        then do nothing.
        """
       # raise NotImplementedError()
       # self.brush_size = max(self.brush_size - 1, self.MIN_BRUSH)
        if self.brush_size != Grid.MAX_BRUSH:
            self.brush_size = self.brush_size - 1
 
    def special(self):
        """
        Activate the special affect on all grid squares.
        """
        for row in self.grid:
            for square in row:
                square.special()

    def __getitem__(self, index):
         return self.grid[index]
    
    def manhattan_distance(self, layer, x, y):
        brush = self.brush_size
        for i in range(-brush, brush+1):
            for j in range(-brush, brush+1):
                if abs(i) + abs(j) <= brush:
                    if (0 <= x + i < self.x) and (0 <= y + j < self.y):
                       self.grid[x + i][y + j].add(layer)

