"""PawPal+ system classes.

Core classes for planning a pet owner's daily care tasks:
Owner -> Pets -> Tasks, with a Scheduler that builds the ordered plan.
"""

import datetime

# Priority is a plain string attribute on Task. This rank map keeps sorting
# correct (lower rank = more important) without needing a Priority class.
PRIORITY_RANK = {"high": 1, "medium": 2, "low": 3}

# How far ahead the next occurrence of a recurring task is scheduled.
FREQUENCY_DELTAS = {
    "daily": datetime.timedelta(days=1),
    "weekly": datetime.timedelta(days=7),
}


class Task:
    def __init__(
        self, time_start, description, duration_min, priority,
        pet=None, frequency="none", date=None,
    ):
        """Create a care task with a date, start time, duration, and priority."""
        # time_start stored as minutes since midnight (int) so tasks sort correctly.
        self.time_start = time_start
        self.description = description
        self.duration_min = duration_min  # int minutes, so durations can be summed
        self.priority = priority  # plain string: "high" | "medium" | "low"
        self.pet = pet  # back-reference to the owning Pet
        self.completed = False  # marked True once the owner finishes the task
        self.frequency = frequency  # "none" | "daily" | "weekly"
        # Calendar date the task occurs on; defaults to today when not given.
        self.date = date or datetime.date.today()

    def mark_complete(self):
        """Mark done; if recurring, spawn the next occurrence and return it (else None)."""
        self.completed = True  # flip this instance to done
        delta = FREQUENCY_DELTAS.get(self.frequency)  # None for non-recurring tasks
        if delta is None or self.pet is None:
            return None  # nothing to regenerate
        # Build the next occurrence: same time/duration/priority/frequency, later date.
        next_task = Task(
            self.time_start, self.description, self.duration_min, self.priority,
            pet=self.pet, frequency=self.frequency, date=self.date + delta,
        )
        # Add directly: the future date can't collide with this just-completed one,
        # and a recurring instance should always be created.
        self.pet.tasks.append(next_task)
        return next_task

    def __lt__(self, other):
        """Order tasks chronologically by date, then start time (used when sorting)."""
        # Python calls this during sorted()/sort(); earlier date/time comes first.
        return (self.date, self.time_start) < (other.date, other.time_start)


class Pet:
    def __init__(self, name, pet_type, owner=None):
        """Create a pet with a name, type, and an empty task list."""
        self.name = name
        self.pet_type = pet_type
        self.tasks = []  # list of Tasks (allows multiple tasks at the same time)
        self.owner = owner  # back-reference to the owning Owner

    def find_conflicts(self, task):
        """Return existing tasks on the same date whose time overlaps the given task."""
        # Two tasks overlap when they share a date AND each starts before the other
        # ends. Duration-aware, so it catches partial overlaps, not just equal starts.
        new_end = task.time_start + task.duration_min  # when the given task finishes
        return [
            t
            for t in self.tasks
            if t.date == task.date  # only same-day tasks can conflict
            and task.time_start < t.time_start + t.duration_min  # task starts before t ends
            and t.time_start < new_end  # t starts before task ends
        ]

    def add_task(self, task):
        """Add a task only if it doesn't overlap; return the list of conflicts (empty if added)."""
        task.pet = self  # so the task knows which pet it belongs to
        conflicts = self.find_conflicts(task)  # any existing tasks it overlaps
        if conflicts:
            return conflicts  # not added — caller decides to replace or skip
        self.tasks.append(task)  # no conflict, safe to add
        return []  # empty list signals a successful add

    def replace_conflicts(self, task):
        """Remove any tasks that overlap the given task, then add it."""
        for t in self.find_conflicts(task):  # every task the new one overlaps
            self.tasks.remove(t)  # drop the old conflicting task
        task.pet = self  # wire up the back-reference
        self.tasks.append(task)  # add the replacement
        return task

    def get_tasks(self):
        """Return this pet's tasks as a list."""
        # Return this pet's tasks as a list.
        return self.tasks


class Owner:
    def __init__(self, name):
        """Create an owner with a name and no pets yet."""
        self.name = name
        self.pets = []  # list of Pet objects this owner owns

    def add_pet(self, name, pet_type):
        """Create a pet owned by this owner and return it."""
        # Create a Pet, link it back to this owner, and track it.
        pet = Pet(name, pet_type, owner=self)  # build the pet, owner = me
        self.pets.append(pet)  # remember it in this owner's list
        return pet  # return so caller can immediately add tasks to it

    def get_all_tasks(self):
        """Return every task across all of this owner's pets as one list."""
        # Flatten tasks across every pet into one list.
        # Each task keeps its .pet back-reference, so the plan knows whose task it is.
        all_tasks = []  # start with an empty collection
        for pet in self.pets:  # visit each pet this owner has
            all_tasks.extend(pet.get_tasks())  # add that pet's tasks to the list
        return all_tasks  # one combined list across all pets


class Scheduler:
    def __init__(self, owner):
        """Create a scheduler that plans for the given owner."""
        self.owner = owner  # data source: the Owner whose pets' tasks we plan

    def build_plan(self, sort_by="time", completed=None, pet_name=None):
        """Return the owner's tasks, optionally filtered by completion/pet, then sorted."""
        # Build the ordered daily plan from all of the owner's tasks.
        tasks = self.owner.get_all_tasks()  # gather every task across all pets

        # Optional filter: completion status. None = all, True/False = that status.
        if completed is not None:
            tasks = [t for t in tasks if t.completed == completed]

        # Optional filter: only tasks belonging to the named pet. None = all pets.
        if pet_name is not None:
            tasks = [t for t in tasks if t.pet is not None and t.pet.name == pet_name]

        if sort_by == "priority":
            # Most important first; ties broken by date then start time.
            return sorted(
                tasks, key=lambda t: (PRIORITY_RANK[t.priority], t.date, t.time_start)
            )

        # Default ("time"): chronological by date then time; ties broken by importance.
        return sorted(
            tasks, key=lambda t: (t.date, t.time_start, PRIORITY_RANK[t.priority])
        )
