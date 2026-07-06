"""Tests for core PawPal+ behaviors."""

from pawpal_system import Owner, Task


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


def test_same_time_task_is_kept_not_overwritten():
    # Adding a second task at the same start time keeps BOTH tasks (a warning is
    # printed, but the existing task is not overwritten).
    owner = Owner("Alice")
    pet = owner.add_pet("Biscuit", "Dog")
    pet.add_task(Task(480, "Morning walk", 30, "high"))
    pet.add_task(Task(480, "Vet appointment", 45, "high"))  # same start time
    tasks = pet.get_tasks()
    assert len(tasks) == 2  # both tasks kept
    descriptions = [t.description for t in tasks]
    assert "Morning walk" in descriptions  # original still present
    assert "Vet appointment" in descriptions  # new one added alongside it


def test_overlapping_tasks_are_kept_with_warning(capsys):
    # A task that starts mid-way through another (partial overlap, not equal
    # start) should be detected: a warning prints and both tasks are kept.
    owner = Owner("Alice")
    pet = owner.add_pet("Biscuit", "Dog")
    pet.add_task(Task(480, "Morning walk", 60, "high"))   # 08:00-09:00
    pet.add_task(Task(510, "Vet appointment", 30, "high"))  # 08:30-09:00, overlaps
    assert len(pet.get_tasks()) == 2  # both kept despite the overlap
    warning = capsys.readouterr().out  # capture what add_task printed
    assert "overlaps" in warning  # an overlap warning was shown


def test_non_overlapping_tasks_no_warning(capsys):
    # Back-to-back tasks that do not overlap should NOT trigger a warning.
    owner = Owner("Alice")
    pet = owner.add_pet("Biscuit", "Dog")
    pet.add_task(Task(480, "Morning walk", 30, "high"))   # 08:00-08:30
    pet.add_task(Task(510, "Feeding", 10, "high"))        # 08:30-08:40, no overlap
    assert len(pet.get_tasks()) == 2
    warning = capsys.readouterr().out
    assert "overlaps" not in warning  # no false-positive warning
