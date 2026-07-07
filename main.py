"""Demo script for PawPal+.

Builds an owner with two pets (three tasks each) and prints the schedule,
then demonstrates a recurring task regenerating when marked complete.
Run with: python3 main.py
"""

import datetime

from pawpal_system import Owner, Scheduler, Task


def format_time(minutes):
    """Convert minutes-since-midnight (int) into a readable HH:MM string."""
    # Convert minutes-since-midnight (int) into a readable HH:MM string.
    hours, mins = divmod(minutes, 60)
    return f"{hours:02d}:{mins:02d}"


def show(plan, heading):
    """Print a heading followed by each task's date, time, and details."""
    print(heading)
    for task in plan:
        repeat = "" if task.frequency == "none" else f" (repeats {task.frequency})"
        print(
            f"  {task.date} {format_time(task.time_start)} — {task.description} "
            f"({task.duration_min} min) [priority: {task.priority}] "
            f"for {task.pet.name}{repeat}"
        )


today = datetime.date.today()

# Create the owner and two pets.
owner = Owner("Alice")
biscuit = owner.add_pet("Biscuit", "Dog")
milo = owner.add_pet("Milo", "Cat")

# Tasks for Biscuit, including a recurring daily walk.
biscuit.add_task(Task(480, "Morning walk", 30, "high", frequency="daily", date=today))
biscuit.add_task(Task(720, "Lunch feeding", 10, "medium", date=today))
biscuit.add_task(Task(1080, "Evening walk", 30, "high", date=today))

# Tasks for Milo, including a recurring weekly bath.
milo.add_task(Task(540, "Breakfast", 10, "high", date=today))
milo.add_task(Task(600, "Litter box", 5, "low", date=today))
milo.add_task(Task(1140, "Bath", 20, "medium", frequency="weekly", date=today))

# Build the plan (chronological by default) and print it.
scheduler = Scheduler(owner)
show(scheduler.build_plan("time"), "Schedule")

# Complete the recurring morning walk -> its next occurrence is auto-created.
biscuit.get_tasks()[0].mark_complete()
print()
show(scheduler.build_plan("time", completed=False), "Remaining tasks after completing the daily walk")
