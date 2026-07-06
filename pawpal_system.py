"""PawPal+ system classes (skeleton).

Class stubs based on diagrams/uml.draft.mmd. No logic yet — just names,
attributes, and empty method stubs.
"""

from enum import IntEnum


class Priority(IntEnum):
    # IntEnum so tasks can be sorted by importance.
    # Lower rank = more important, so ascending sort puts HIGH first.
    HIGH = 1
    MEDIUM = 2
    LOW = 3


class Task:
    def __init__(self, time_start, description, duration_min, priority, pet=None):
        # time_start stored as minutes since midnight (int) so tasks sort correctly.
        self.time_start = time_start
        self.description = description
        self.duration_min = duration_min  # int minutes, so durations can be summed
        self.priority = priority
        self.pet = pet  # back-reference to the owning Pet

    def __lt__(self, other):
        # Natural order for a schedule is chronological (by start time).
        pass


class Pet:
    def __init__(self, name, pet_type, owner=None):
        self.name = name
        self.pet_type = pet_type
        self.tasks = {}
        self.owner = owner  # back-reference to the owning Owner

    def add_task(self, task):
        pass

    def get_tasks(self):
        pass


class Owner:
    def __init__(self, name):
        self.name = name
        self.pets = []

    def add_pet(self, name, pet_type):
        pass

    def daily_plan(self, sort_by="time"):
        # Collect every task across all pets, then sort by explicit key:
        #   sort_by="time"     -> key (time_start, priority)  chronological, ties by importance
        #   sort_by="priority" -> key (priority, time_start)  most important first, ties by time
        pass
