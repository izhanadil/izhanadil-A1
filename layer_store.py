from __future__ import annotations
from abc import ABC, abstractmethod
from layer_util import Layer
from data_structures.queue_adt import CircularQueue
from data_structures import queue_adt, array_sorted_list, stack_adt

class LayerStore(ABC):

    def __init__(self) -> None:
        pass

    @abstractmethod
    def add(self, layer: Layer) -> bool:
        """
        Add a layer to the store.
        Returns true if the LayerStore was actually changed.
        """
        pass

    @abstractmethod
    def get_color(self, start, timestamp, x, y) -> tuple[int, int, int]:
        """
        Returns the colour this square should show, given the current layers.
        """
        pass

    @abstractmethod
    def erase(self, layer: Layer) -> bool:
        """
        Complete the erase action with this layer
        Returns true if the LayerStore was actually changed.
        """
        pass

    @abstractmethod
    def special(self):
        """
        Special mode. Different for each store implementation.
        """
        pass

class SetLayerStore(LayerStore):
    """
    Set layer store. A single layer can be stored at a time (or nothing at all)
    - add: Set the single layer.
    - erase: Remove the single layer. Ignore what is currently selected.
    - special: Invert the colour output.
    """

    def __init__(self) -> None:
        self.array_sorted = None
        self.inverts = None

    def add(self, layer: Layer) -> bool:
        """
        Add a layer to the store.
        Returns true if the LayerStore was actually changed.
        """
        self.array_sorted = layer
        return True

    def get_color(self, start, timestamp, x, y) -> tuple[int, int, int]:
        """
        Returns the colour this square should show, given the current layers.
        """
        if self.array_sorted is not None:
            color = self.array_sorted.apply(start, timestamp, x, y)
            if self.inverts:
                color = (255 - color[0], 255 - color[1], 255 - color[2])
            return color
        else:
            return start  

    def erase(self, layer: Layer) -> bool:
        """
        Complete the erase action with this layer
        Returns true if the LayerStore was actually changed.
        """
        self.array_sorted = None
        return True

    def special(self):
        """
        Special mode. Different for each store implementation.
        """
        self.inverts = not self.inverts

class AdditiveLayerStore(LayerStore):
    """
    Additive layer store. Each added layer applies after all previous ones.
    - add: Add a new layer to be added last.
    - erase: Remove the first layer that was added. Ignore what is currently selected.
    - special: Reverse the order of current layers (first becomes last, etc.)
    """

    def __init__(self) -> None:
        self.layers = CircularQueue(2000)
        self.temp_queue = CircularQueue(2000)

    def add(self, layer: Layer) -> bool:
        """
        Add a layer to the store.
        Returns true if the LayerStore was actually changed.
        """
        self.layers.append(layer)
        return True

    def get_color(self, start, timestamp, x, y) -> tuple[int, int, int]:
        """
        Returns the colour this square should show, given the current layers.
        """
        color = start

       

        for me in range(self.layers.length):
            first = self.layers.serve()
            color = first.apply(color, timestamp, x, y)
            self.add(first)

        return color

    
    def erase(self, layer: Layer) -> bool:
        """
        Complete the erase action with this layer
        Returns true if the LayerStore was actually changed.
        """
        self.layers.serve()
        return True

    
    def special(self):
        """
        Special mode. Different for each store implementation.
        """
        STACK = stack_adt.ArrayStack(2000)

        for ind in range(len(self.layers)):
            qlayer = self.layers.serve()
            STACK.push(qlayer)

        for Ind in range(STACK.length):
            layer = STACK.pop()
            self.layers.append(layer)

        return self.layers
    
class SequenceLayerStore(LayerStore):
    """
    Sequential layer store. Each layer type is either applied / not applied, and is applied in order of index.
    - add: Ensure this layer type is applied.
    - erase: Ensure this layer type is not applied.
    - special:
        Of all currently applied layers, remove the one with median `name`.
        In the event of two layers being the median names, pick the lexicographically smaller one.
    """

    def __init__(self):
        pass
        # super().__init__()
        # self.layers = {}
        # self.index = 0

    def add(self, layer: Layer):
        pass
        # layer.index = self.index
        # self.layers[layer.name] = layer
        # self.index += 1

    def erase(self, layer_name: str):
        pass
        # if layer_name in self.layers:
        #     del self.layers[layer_name]

    def get_layers(self):
    #  -> List[Layer]:
        pass
        #return list(self.layers.values())

    def apply_layers(self, grid: Grid) -> None:
        pass
        # color_counts = defaultdict(lambda: [0, 0, 0])
        # for layer in sorted(self.layers.values(), key=attrgetter('index')):
        #     if layer.applying:
        #         for x in range(grid.width):
        #             for y in range(grid.height):
        #                 if grid.is_within_bounds(x, y):
        #                     color_counts[(x, y)] = [
        #                         color_counts[(x, y)][i] + layer.color[i]
        #                         for i in range(3)
        #                     ]
        # for (x, y), color_sum in color_counts.items():
        #     color = [min(int(c), 255) for c in color_sum]
        #     grid[x][y].set_color(color)

    def special(self):
        pass
        # num_applying = sum(layer.applying for layer in self.layers.values())
        # if num_applying % 2 == 0:
        #     median_name = sorted(self.layers.keys())[num_applying // 2 - 1]
        # else:
        #     median_name = sorted(self.layers.keys())[num_applying // 2]
        # self.layers[median_name].applying = False

