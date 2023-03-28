from __future__ import annotations
from action import PaintAction
from grid import Grid
from data_structures import queue_adt, array_sorted_list, stack_adt

class UndoTracker:

    def __init__(self,capacity=1000) -> None:
        # Initialize an instance of the UndoTracker class.
        # :param capacity: The maximum number of actions that can be stored.
        self.capacity = capacity
        self.undo_stack = stack_adt.ArrayStack(self.capacity)
        self.redo_stack = stack_adt.ArrayStack(self.capacity)

    def add_action(self, action: PaintAction) -> None:
        """
        Adds an action to the undo tracker.

        If your collection is already full,
        feel free to exit early and not add the action.
        """
        # Add the given action to the undo stack if it is not full
        if (self.undo_stack.length) < self.capacity:
            self.undo_stack.push(action)

    def undo(self, grid: Grid) -> PaintAction|None:
        """
        Undo an operation, and apply the relevant action to the grid.
        If there are no actions to undo, simply do nothing.

        :return: The action that was undone, or None.
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

        :return: The action that was redone, or None.
        """
        # Pop the last action from the redo stack if it is not empty,
        # apply the action to the grid, push it back to the undo stack and return the action
        if self.redo_stack.is_empty():
            return None

        action = self.redo_stack.pop()
        action.redo_apply(grid)
        self.undo_stack.push(action)
        return action
