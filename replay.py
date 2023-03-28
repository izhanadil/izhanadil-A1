# from __future__ import annotations
# from action import PaintAction
# from grid import Grid
# from data_structures import queue_adt
# from undo import UndoTracker

# class ReplayTracker:

#     def __init__(self, capacity=10000) -> None:
#         """
#         Initialize an instance of the UndoTracker class.

#         :param capacity: The maximum number of actions that can be stored.
#         """
#         # pass
#         self.replay_queue = queue_adt.CircularQueue(capacity)


#     def start_replay(self) -> None:
#         """
#         Called whenever we should stop taking actions, and start playing them back.

#         Useful if you have any setup to do before `play_next_action` should be called.
#         """
#         #pass


#     def add_action(self, action: PaintAction, is_undo: bool=False) -> None:
#         """
#         Adds an action to the replay.

#         `is_undo` specifies whether the action was an undo action or not.
#         Special, Redo, and Draw all have this is False.
#         """
#         #pass
#         if not is_undo:
#             self.replay_queue.append(action)
#         else:
#             undo = ReplayTracker()
#             undo.add_action(action)
#             self.replay_queue.append(undo)

#     def play_next_action(self, grid: Grid) -> bool:
#         """
#         Plays the next replay action on the grid.
#         Returns a boolean.
#             - If there were no more actions to play, and so nothing happened, return True.
#             - Otherwise, return False.
#         """
#         #pass
#         if self.replay_queue.is_empty():
#             return True
#         else:
#             next_action = self.replay_queue.serve()
#             if isinstance(next_action, UndoTracker):
#                 next_action.undo(grid)
#             elif isinstance(next_action, PaintAction):
#                  next_action.redo_apply(grid)
#             return False

# if __name__ == "__main__":
#     action1 = PaintAction([], is_special=True)
#     action2 = PaintAction([])

#     g = Grid(Grid.DRAW_STYLE_SET, 5, 5)

#     r = ReplayTracker()
#     # add all actions
#     r.add_action(action1)
#     r.add_action(action2)
#     r.add_action(action2, is_undo=True)
#     # Start the replay.
#     r.start_replay()
#     f1 = r.play_next_action(g) # action 1, special
#     f2 = r.play_next_action(g) # action 2, draw
#     f3 = r.play_next_action(g) # action 2, undo
#     t = r.play_next_action(g)  # True, nothing to do.
#     assert (f1, f2, f3, t) == (False, False, False, True)

from __future__ import annotations
from action import PaintAction
from grid import Grid
from data_structures import queue_adt
from undo import UndoTracker


class ReplayTracker:
    def __init__(self, capacity=10000) -> None:
        """
        Initialize an instance of the ReplayTracker class.

        :param capacity: The maximum number of actions that can be stored.
        """
        self.replay_queue = queue_adt.CircularQueue(capacity)  # Create a circular queue for storing actions
        self.undo_tracker = UndoTracker(capacity)  # Create an undo tracker to keep track of undo actions

    def start_replay(self) -> None:
        """
        Called whenever we should stop taking actions, and start playing them back.

        Useful if you have any setup to do before `play_next_action` should be called.
        """
        pass

    def add_action(self, action: PaintAction, is_undo: bool = False) -> None:
        """
        Adds an action to the replay.

        `is_undo` specifies whether the action was an undo action or not.
        Special, Redo, and Draw all have this is False.
        """
        if not is_undo:
            self.replay_queue.append(action)  # Add the action to the replay queue
            self.undo_tracker.add_action(action)  # Add the action to the undo tracker
        else:
            self.undo_tracker.add_action(action)  # Add the action to the undo tracker
            undo = ReplayTracker()  # Create a new replay tracker
            undo.add_action(action)  # Add the action to the new replay tracker
            self.replay_queue.append(undo)  # Add the new replay tracker to the replay queue

    def play_next_action(self, grid: Grid) -> bool:
        """
        Plays the next replay action on the grid.
        Returns a boolean.
            - If there were no more actions to play, and so nothing happened, return True.
            - Otherwise, return False.
        """
        if self.replay_queue.is_empty():  # If the replay queue is empty, return True
            return True
        else:
            next_action = self.replay_queue.serve()  # Get the next action from the replay queue
            if isinstance(next_action, ReplayTracker):  # If the next action is a replay tracker
                next_action.undo(grid)  # Undo the action on the grid
            elif isinstance(next_action, PaintAction):  # If the next action is a paint action
                next_action.redo_apply(grid)  # Redo the action on the grid
            return False

    def undo(self, grid: Grid) -> bool:
        """
        Undo the last action.
        Returns a boolean.
            - If there were no more actions to undo, and so nothing happened, return True.
            - Otherwise, return False.
        """
        # Call the `undo` method of the `UndoTracker` object to undo the last action
        # and return the boolean value indicating whether anything was undone or not
        return self.undo_tracker.undo(grid)


if __name__ == "__main__":
    action1 = PaintAction([], is_special=True)
    action2 = PaintAction([])

    g = Grid(Grid.DRAW_STYLE_SET, 5, 5)

    r = ReplayTracker()
    # add all actions
    r.add_action(action1)
    r.add_action(action2)
    r.add_action(action2, is_undo=True)
    # Start the replay.
    r.start_replay()
    f1 = r.play_next_action(g)  # action 1, special
    f2 = r.play_next_action(g)  # action 2, draw
    f3 = r.play_next_action(g)  # action 2, undo
    t = r.play_next_action(g)   # True, nothing to do.
    assert (f1, f2, f3, t) == (False, False, False, True)

    # undo the last action
    f4 = r.undo(g)
    assert f4 == False
