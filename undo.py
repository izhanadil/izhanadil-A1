from __future__ import annotations
from action import PaintAction
from grid import Grid
from data_structures import queue_adt, array_sorted_list, stack_adt

class UndoTracker:

    def __init__(self,capacity=1000) -> None:
        """
        Initializes an instance of the UndoTracker class with a given capacity.

        Args:
        - capacity: The maximum number of actions that can be stored.

        Complexity:
        - Best case: O(1), as it simply initializes the instance variables.
        - Worst case: O(1), as it simply initializes the instance variables.
        """
        # Initialize an instance of the UndoTracker class.
        # :param capacity: The maximum number of actions that can be stored.
        self.capacity = capacity
        self.undo_stack = stack_adt.ArrayStack(self.capacity)
        self.redo_stack = stack_adt.ArrayStack(self.capacity)

    def add_action(self, action: PaintAction) -> None:
        """
        Adds an action to the undo tracker.

        Args: A PaintAction object to be added to the undo tracker.
        

        :return: None
        :rtype: None

        The function adds a given PaintAction object to the undo stack if it is not full. The maximum capacity
        of the undo stack is set when the UndoTracker object is created. If the undo stack is already full,
        the function exits early and does not add the action.

        Best Case Complexity: O(1)
        Worst Case Complexity: O(1)
        """
        # Add the given action to the undo stack if it is not full
        if (self.undo_stack.length) < self.capacity:
            self.undo_stack.push(action)

    def undo(self, grid: Grid) -> PaintAction|None:
        """
        Undo the most recent PaintAction on the undo stack and apply its inverse
        action to the given grid. If the undo stack is empty, do nothing.

        Args:
        - grid: A Grid object representing the current state of the painting.

        Returns:
        - The PaintAction object that was undone, or None if there were no actions
        on the undo stack.

        Raises:
        - None.

        Complexity:
        - Best case: O(1) if the undo stack is empty.
        - Worst case: O(1) if the undo stack is not empty.
        """
        # Pop the last action from the undo stack if it is not empty,
        # apply the action to the grid and return the action
        if self.undo_stack.length > 0:
            action_to_undo = self.undo_stack.pop()
            action_to_undo.undo_apply(grid)
            return action_to_undo
        else:
            return None

    def redo(self, grid: Grid) -> PaintAction|None:
        """
        Redo an operation that was previously undone.
        If there are no actions to redo, simply do nothing.

        Args:
        - grid: The grid to which the action should be applied.

        Returns:
        - The action that was redone, or None.

        Complexity:
        - Worst case: O(1) - this operation involves popping an element from the redo stack, applying it to the grid, pushing it to the undo stack, and returning the element. All of these operations take constant time. 
        - Best case: O(1) - same as worst case.
        """

        # Pop the last action from the redo stack if it is not empty,
        # apply the action to the grid, push it back to the undo stack and return the action
        if self.redo_stack.is_empty():
            return None

        action = self.redo_stack.pop()
        action.redo_apply(grid)
        self.undo_stack.push(action)
        return action
