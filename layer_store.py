from __future__ import annotations
from abc import ABC, abstractmethod
from layer_util import Layer
from layer_util import get_layers
from data_structures.queue_adt import CircularQueue
from data_structures import queue_adt, stack_adt
from data_structures.array_sorted_list import ArraySortedList, ListItem

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
        # Initialize the array_sorted and inverts to None
        # time complexity O(1)
        self.array_sorted = None
        self.inverts = None

    def add(self, layer: Layer) -> bool:
        """
        Add a layer to the store.
        Returns true if the LayerStore was actually changed.
        
        Args:
        - layer: An instance of the Layer class to be added.

        Returns:
        - bool: A boolean value indicating whether the LayerStore was actually changed.
        
        Description:
        This method adds a single layer to the SetLayerStore instance. It sets the current layer to the layer 
        parameter and returns True indicating that the change was made. 
        The best case time complexity of this method is O(1) as it only needs to set the layer and return True.
        The worst case time complexity is also O(1) because the operation does not depend on the size of the input.
        """
        # Set the current layer to the array_sorted and return True indicating the change was made.
        self.array_sorted = layer
        return True

    def get_color(self, start, timestamp, x, y) -> tuple[int, int, int]:
        """
        Returns the colour this square should show, given the current layers.
         Arguments:
        - start: A tuple of integers representing the RGB value of the starting color.
        - timestamp: An integer representing the current timestamp.
        - x: An integer representing the x-coordinate of the square.
        - y: An integer representing the y-coordinate of the square.

        Returns:
        A tuple of integers representing the RGB value of the final color.

        
        Best case: O(1) if self.array_sorted is None.
        Worst case: O(L) where L is the complexity of applying the layer self.array_sorted on the given input.
            """
        # If array_sorted is not None, apply the layer on the specified start, timestamp, x and y 
        # to get the color and store it in 'color' variable
        if self.array_sorted is not None:
            color = self.array_sorted.apply(start, timestamp, x, y)
            
            # If inverts is True, invert the color output
            if self.inverts:
                color = (255 - color[0], 255 - color[1], 255 - color[2])
            return color
        else:
            # If array_sorted is None, return start (default color)
            return start  

    def erase(self, layer: Layer) -> bool:
        """
        Complete the erase action with this layer
        Returns true if the LayerStore was actually changed.
        Args:
        layer (Layer): The layer to be removed.
        
        Returns:
            bool: True if the LayerStore was actually changed.
            
        Complexity:
            Best case: O(1)
                When the layer is removed successfully, it only requires setting the value of 
                `array_sorted` to None, which is an O(1) operation.
            Worst case: O(1)
                Similarly, when the layer is not present in the LayerStore, it still only requires 
                setting the value of `array_sorted` to None, which is an O(1) operation.
        """
        # Set the array_sorted to None indicating the layer has been removed and return True indicating change was made.
        self.array_sorted = None
        return True

    def special(self):
        """
        Special mode. Different for each store implementation.
        This function has a constant time complexity of O(1), as it only performs a single operation regardless of the size of the input.
        """
        # Invert the color output by toggling the inverts flag.
        self.inverts = not self.inverts


class AdditiveLayerStore(LayerStore):
    """
    Additive layer store. Each added layer applies after all previous ones.
    - add: Add a new layer to be added last.
    - erase: Remove the first layer that was added. Ignore what is currently selected.
    - special: Reverse the order of current layers (first becomes last, etc.)
    """

    def __init__(self) -> None:
        #Complexity:
        #O(1), as this method simply initializes the two queues with a maximum capacity of 2000.
        # Initialize a new circular queue for layers with a maximum capacity of 2000
        self.layers = CircularQueue(2000)
        # Initialize a new temporary circular queue for processing
        self.temp_queue = CircularQueue(2000)

    def add(self, layer: Layer) -> bool:
        """
        Add a layer to the store.
        Returns true if the LayerStore was actually changed.
         Args:
            layer: An instance of the Layer class to add to the store.
        
        Returns:
            A boolean value indicating whether the LayerStore was actually changed.
            
        Complexity:
            Time: O(1) - appending an item to a circular queue takes constant time.
        """
        # Append the new layer to the end of the layers queue
        self.layers.append(layer)
        # Return True as the LayerStore was changed
        return True

    def get_color(self, start, timestamp, x, y) -> tuple[int, int, int]:
        """
        Returns the colour this square should show, given the current layers.
        Args:
        - start: tuple of 3 integers representing the starting RGB color of the square
        - timestamp: integer representing the timestamp of the query
        - x: integer representing the x coordinate of the square
        - y: integer representing the y coordinate of the square
    
        Returns:
        - A tuple of 3 integers representing the final RGB color of the square after applying all layers
        
        Time Complexity:
        - Best case: O(1) when there are no layers in the store or when the first layer changes the color of the square to the final color
        - Worst case: O(N) where N is the number of layers in the store. This happens when all the layers change the color of the square
        """
        # Set color to the starting color
        color = start

        # Iterate through all the layers
        for me in range(self.layers.length):
            # Dequeue the first layer
            first = self.layers.serve()
            # Apply the layer to the current color
            color = first.apply(color, timestamp, x, y)
            # Enqueue the layer to the temporary queue
            self.temp_queue.append(first)

        # Swap the layers queue with the temporary queue
        self.layers, self.temp_queue = self.temp_queue, self.layers

        # Return the final color
        return color

    
    def erase(self, layer: Layer) -> bool:
        """
        Complete the erase action with this layer
        Returns true if the LayerStore was actually changed.
        Args:
            layer (Layer): The layer to be removed from the store.

        Returns:
            bool: True if the LayerStore was actually changed.

        Complexity:
            - Time:
                - Best Case: O(1), when the layer to be removed is at the front of the queue.
                - Worst Case: O(n), when the layer to be removed is at the end of the queue or not in the queue at all,
                  and all layers need to be dequeued and re-enqueued.
        """
        # Dequeue the first layer
        self.layers.serve()
        # Return True as the LayerStore was changed
        return True

    
    def special(self):
        """
        Special mode. Different for each store implementation.
        Best case time complexity: O(1)
        Worst case time complexity: O(n)
        where n is the number of layers in the queue.
        """
        # Create a new stack with a maximum capacity of 2000
        STACK = stack_adt.ArrayStack(2000)

        # Iterate through all the layers
        for ind in range(len(self.layers)):
            # Dequeue the current layer
            qlayer = self.layers.serve()
            # Push the layer to the stack
            STACK.push(qlayer)

        # Iterate through all the layers
        for Ind in range(STACK.length):
            # Pop the top layer from the stack
            layer = STACK.pop()
            # Enqueue the layer to the layers queue
            self.layers.append(layer)

        # Return the updated layers queue
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

    def __init__(self) -> None:
        """
        Initializes a LayerStore object with an ArraySortedList to store the layers
        and adds a ListItem for each layer with a value of False (layer is not applied).

        Args:
            None

        Returns:
            None

        Complexity:
            Best Case: O(1)
                When the length of get_layers() is 0, the for loop is not executed and the time complexity is constant.
            Worst Case: O(n)
                When the length of get_layers() is maximum and all elements need to be processed by the for loop,
                the time complexity is linear with respect to the length of get_layers().
    
         """
        # Initialize an ArraySortedList to store the layers.
        self.array_sorted_list = ArraySortedList(len(get_layers())*100)

        # Add a ListItem for each layer with a value of False (layer is not applied).
        for element in range(0, len(get_layers())):
            if get_layers()[element] == None:
                break
            else:
                item_list = ListItem(False, element)
                self.array_sorted_list.add(item_list)

    def add(self, layer: Layer) -> bool:
        """
        Add element layer to the store.
        Returns true if the LayerStore was actually changed.
        Args:
         - layer: a Layer object representing the layer to be added.
    
        Returns:
        - A boolean indicating whether the LayerStore was actually changed.
        
        Best case time complexity: O(log n), where n is the number of elements in the ArraySortedList.
        Worst case time complexity: O(n), where n is the number of elements in the ArraySortedList.
        The complexity is determined by the `add` method of the ArraySortedList class,
        which performs binary search to find the correct position to insert the new item. In the worst case scenario,
        the binary search will have to go through all n elements in the list before inserting the new item at the end.
        """
        # Remove the current ListItem for the layer's index.
        self.array_sorted_list.delete_at_index(layer.index)

        # Create a new ListItem for the layer with a value of True (layer is applied).
        item_list = ListItem(True, layer.index)

        # Add the new ListItem to the ArraySortedList.
        self.array_sorted_list.add(item_list)

        return True

    def get_color(self, start, timestamp, x, y) -> tuple[int, int, int]:
        """
        Returns the color this square should show, given the current layers.

        start = RGB
        
        Args:
        - start: a tuple of three integers representing the starting RGB color value of the square
        - timestamp: a float representing the current timestamp
        - x: an integer representing the x-coordinate of the square
        - y: an integer representing the y-coordinate of the square

        Returns:
        - a tuple of three integers representing the final RGB color value of the square after applying all applicable layers

        Complexity:
        - Worst case time complexity: O(n) where n is the number of layers in the ArraySortedList.
        - Best case time complexity: O(1) if there are no layers applied.
        """
        # Set the color to the starting RGB value.
        color = start

        # Iterate through each layer in the ArraySortedList.
        for x in range(len(self.array_sorted_list)):
            layer = self.array_sorted_list[x]

            # If the layer is applied, apply it to the color.
            if layer.value:
                color = get_layers()[layer.key].apply(color, timestamp, x, y)

        return color

    def erase(self, layer: Layer) -> bool:
        """
        Complete the erase action with this layer
        Returns true if the LayerStore was actually changed.
        Arguments:

            layer: an instance of the Layer class representing the layer to be removed.
        Return:

            A boolean value indicating whether the LayerStore was actually changed or not.
        Best case: O(1) if the layer to be erased is at the beginning of the ArraySortedList.
        Worst case: O(N) if the layer to be erased is at the end of the ArraySortedList, where N is the number of layers in the LayerStore.
        """
        # Create a new ListItem for the layer with a value of False (layer is not applied).
        item_list = ListItem(False, layer.index)

        # Remove the current ListItem for the layer.
        self.array_sorted_list.delete_at_index(item_list.key)

        return True

    def special(self):
        """
        Special mode. Different for each store implementation.
        Special mode. Reorders the layer store to prioritize the median layer alphabetically.
        This function takes no arguments and returns nothing.

        Best case time complexity: O(n), where n is the number of layers in the layer store.
        Worst case time complexity: O(n^2), where n is the number of layers in the layer store.
        This is because of the time complexity of adding elements to the lexi_sorted_layers
        array, which can be O(n^2) if all elements need to be compared.
        """

        # Create a new ArraySortedList to store the layers in lexicographically sorted order.
        lexi_sorted_layers = ArraySortedList(len(get_layers()) * 100)

        # Iterate through each layer in the ArraySortedList.
        for index in range(self.array_sorted_list.length):
            cur_layer = self.array_sorted_list[index]

            # If the layer is applied, add a new ListItem to lexi_sorted_layers with the layer's name.
            if cur_layer.value:
               layer_replace = ListItem(cur_layer.key, get_layers()[cur_layer.key].name)
               lexi_sorted_layers.add(layer_replace)

        # Determine the index of the median layer in lexi_sorted_layers.
        if lexi_sorted_layers.length % 2 == 1:
            median_index = (lexi_sorted_layers.length + 1) // 2
        else:
            median_index = lexi_sorted_layers.length // 2

        


        self.array_sorted_list.delete_at_index(
        get_layers()[lexi_sorted_layers.delete_at_index(median_index - 1).value].index)