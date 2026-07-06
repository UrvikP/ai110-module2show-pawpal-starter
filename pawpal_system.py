"""PawPal+ system classes.

Core classes for planning a pet owner's daily care tasks:
Owner -> Pets -> Tasks, with a Scheduler that builds the ordered plan.
"""

# Priority is a plain string attribute on Task. This rank map keeps sorting
# correct (lower rank = more important) without needing a Priority class.
PRIORITY_RANK = {"high": 1, "medium": 2, "low": 3}


class Task:
    def __init__(self, time_start, description, duration_min, priority, pet=None):
        # time_start stored as minutes since midnight (int) so tasks sort correctly.
        self.time_start = time_start
        self.description = description
        self.duration_min = duration_min  # int minutes, so durations can be summed
        self.priority = priority  # plain string: "high" | "medium" | "low"
        self.pet = pet  # back-reference to the owning Pet
        self.completed = False  # marked True once the owner finishes the task

    def mark_complete(self):
        # Flip this task's status to done so the plan/UI can show it as finished.
        self.completed = True  # set the flag; nothing else needs to change

    def __lt__(self, other):
        # Defines "less than" so sorting a list of Tasks is chronological by default.
        # Python calls this during sorted()/sort(); earlier start time comes first.
        return self.time_start < other.time_start  # compare the two start times


class Pet:
    def __init__(self, name, pet_type, owner=None):
        self.name = name
        self.pet_type = pet_type
        self.tasks = {}  # keyed by time_start -> Task (one task per start time)
        self.owner = owner  # back-reference to the owning Owner

    def add_task(self, task):
        # Register a task with this pet and wire up the back-reference.
        task.pet = self  # so the task knows which pet it belongs to
        self.tasks[task.time_start] = task  # store keyed by start time
        return task  # hand it back for convenience (e.g. chaining/testing)

    def get_tasks(self):
        # Return this pet's tasks as a list (callers don't need the dict keys).
        return list(self.tasks.values())  # dict values -> plain list of Tasks


class Owner:
    def __init__(self, name):
        self.name = name
        self.pets = []  # list of Pet objects this owner owns

    def add_pet(self, name, pet_type):
        # Create a Pet, link it back to this owner, and track it.
        pet = Pet(name, pet_type, owner=self)  # build the pet, owner = me
        self.pets.append(pet)  # remember it in this owner's list
        return pet  # return so caller can immediately add tasks to it

    def get_all_tasks(self):
        # Flatten tasks across every pet into one list.
        # Each task keeps its .pet back-reference, so the plan knows whose task it is.
        all_tasks = []  # start with an empty collection
        for pet in self.pets:  # visit each pet this owner has
            all_tasks.extend(pet.get_tasks())  # add that pet's tasks to the list
        return all_tasks  # one combined list across all pets


class Scheduler:
    def __init__(self, owner):
        self.owner = owner  # data source: the Owner whose pets' tasks we plan

    def build_plan(self, sort_by="time"):
        # Build the ordered daily plan from all of the owner's tasks.
        tasks = self.owner.get_all_tasks()  # gather every task across all pets

        if sort_by == "priority":
            # Most important first; ties broken by earlier start time.
            return sorted(tasks, key=lambda t: (PRIORITY_RANK[t.priority], t.time_start))

        # Default ("time"): chronological; ties broken by importance.
        return sorted(tasks, key=lambda t: (t.time_start, PRIORITY_RANK[t.priority]))
