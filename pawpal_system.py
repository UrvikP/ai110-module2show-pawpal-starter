"""PawPal+ system classes (skeleton).

Class stubs based on diagrams/uml.draft.mmd. No logic yet — just names,
attributes, and empty method stubs.
"""

from enum import Enum


class Priority(Enum):
    HIGH = "high"
    MEDIUM = "medium"
    LOW = "low"


class Task:
    def __init__(self, time_start, description, duration, priority):
        self.time_start = time_start
        self.description = description
        self.duration = duration
        self.priority = priority

    def __lt__(self, other):
        pass


class Pet:
    def __init__(self, name, pet_type):
        self.name = name
        self.pet_type = pet_type
        self.tasks = {}

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

    def daily_plan(self, sort_by):
        pass
