"""Demo script for PawPal+.

Builds an owner with two pets (three tasks each) and prints today's schedule.
Run with: python3 main.py
"""

from pawpal_system import Owner, Scheduler, Task


def format_time(minutes):
    # Convert minutes-since-midnight (int) into a readable HH:MM string.
    hours, mins = divmod(minutes, 60)
    return f"{hours:02d}:{mins:02d}"


# Create the owner and two pets.
owner = Owner("Alice")
biscuit = owner.add_pet("Biscuit", "Dog")
milo = owner.add_pet("Milo", "Cat")

# Three tasks for Biscuit, at different times.
biscuit.add_task(Task(480, "Morning walk", 30, "high"))   # 08:00
biscuit.add_task(Task(720, "Lunch feeding", 10, "medium"))  # 12:00
biscuit.add_task(Task(1080, "Evening walk", 30, "high"))  # 18:00

# Three tasks for Milo, at different times.
milo.add_task(Task(540, "Breakfast", 10, "high"))    # 09:00
milo.add_task(Task(600, "Litter box", 5, "low"))     # 10:00
milo.add_task(Task(1140, "Playtime", 15, "medium"))  # 19:00

# Build the plan (chronological by default) and print it.
scheduler = Scheduler(owner)
plan = scheduler.build_plan("time")

print("Today's schedule")
for task in plan:
    print(
        f"  {format_time(task.time_start)} — {task.description} "
        f"({task.duration_min} min) [priority: {task.priority}] for {task.pet.name}"
    )
