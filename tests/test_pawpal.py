"""Tests for core PawPal+ behaviors."""

from pawpal_system import Owner, Task, Scheduler


def test_mark_complete_changes_status():
    # A new task starts incomplete; mark_complete() should flip it to True.
    task = Task(480, "Morning walk", 30, "high")
    assert task.completed is False  # sanity check: starts not done
    task.mark_complete()
    assert task.completed is True  # status changed after marking complete


def test_add_task_increases_pet_task_count():
    # Adding a task to a pet should increase that pet's task count by one.
    owner = Owner("Alice")
    pet = owner.add_pet("Biscuit", "Dog")
    assert len(pet.get_tasks()) == 0  # no tasks yet
    pet.add_task(Task(480, "Morning walk", 30, "high"))
    assert len(pet.get_tasks()) == 1  # count went up by one


def test_conflicting_task_is_not_added():
    # A task that overlaps an existing one is NOT added; add_task returns the
    # list of conflicting tasks so the caller can decide what to do.
    owner = Owner("Alice")
    pet = owner.add_pet("Biscuit", "Dog")
    pet.add_task(Task(480, "Morning walk", 60, "high"))   # 08:00-09:00
    conflicts = pet.add_task(Task(510, "Vet appointment", 30, "high"))  # overlaps
    assert len(pet.get_tasks()) == 1  # second task was NOT added
    assert len(conflicts) == 1  # the overlap was reported back
    assert conflicts[0].description == "Morning walk"  # names the conflict


def test_non_conflicting_task_is_added():
    # Back-to-back tasks that do not overlap are added, and add_task returns [].
    owner = Owner("Alice")
    pet = owner.add_pet("Biscuit", "Dog")
    pet.add_task(Task(480, "Morning walk", 30, "high"))   # 08:00-08:30
    conflicts = pet.add_task(Task(510, "Feeding", 10, "high"))  # 08:30-08:40, ok
    assert len(pet.get_tasks()) == 2  # both added
    assert conflicts == []  # no conflicts reported


def test_replace_conflicts_swaps_in_new_task():
    # replace_conflicts removes overlapping tasks and adds the new one instead.
    owner = Owner("Alice")
    pet = owner.add_pet("Biscuit", "Dog")
    pet.add_task(Task(480, "Morning walk", 60, "high"))   # 08:00-09:00
    pet.replace_conflicts(Task(510, "Vet appointment", 30, "high"))  # overlaps
    tasks = pet.get_tasks()
    assert len(tasks) == 1  # old removed, new added -> still one task
    assert tasks[0].description == "Vet appointment"  # the new task won


def _owner_with_mixed_tasks():
    # Helper: one owner, two pets, a mix of complete/incomplete tasks.
    owner = Owner("Alice")
    dog = owner.add_pet("Biscuit", "Dog")
    cat = owner.add_pet("Milo", "Cat")
    walk = Task(480, "Morning walk", 30, "high")
    dog.add_task(walk)
    dog.add_task(Task(600, "Feeding", 10, "medium"))
    cat.add_task(Task(540, "Litter box", 5, "low"))
    walk.mark_complete()  # exactly one completed task
    return owner


def test_filter_by_completion_status():
    # completed=False returns only incomplete tasks; completed=True only complete.
    scheduler = Scheduler(_owner_with_mixed_tasks())
    incomplete = scheduler.build_plan(completed=False)
    complete = scheduler.build_plan(completed=True)
    assert all(not t.completed for t in incomplete)  # none are done
    assert len(incomplete) == 2
    assert all(t.completed for t in complete)  # all are done
    assert len(complete) == 1


def test_filter_by_pet_name():
    # pet_name limits the plan to that pet's tasks only.
    scheduler = Scheduler(_owner_with_mixed_tasks())
    plan = scheduler.build_plan(pet_name="Milo")
    assert len(plan) == 1  # Milo has a single task
    assert all(t.pet.name == "Milo" for t in plan)  # nothing from other pets


def test_filter_by_pet_and_status_combined():
    # Filters combine: incomplete tasks for Biscuit only.
    scheduler = Scheduler(_owner_with_mixed_tasks())
    plan = scheduler.build_plan(completed=False, pet_name="Biscuit")
    assert len(plan) == 1  # Biscuit's walk is complete, only Feeding remains
    assert plan[0].description == "Feeding"
