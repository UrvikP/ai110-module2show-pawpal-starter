# PawPal+ (Module 2 Project)

You are building **PawPal+**, a Streamlit app that helps a pet owner plan care tasks for their pet.

## Scenario

A busy pet owner needs help staying consistent with pet care. They want an assistant that can:

- Track pet care tasks (walks, feeding, meds, enrichment, grooming, etc.)
- Consider constraints (time available, priority, owner preferences)
- Produce a daily plan and explain why it chose that plan

Your job is to design the system first (UML), then implement the logic in Python, then connect it to the Streamlit UI.

## What you will build

Your final app should:

- Let a user enter basic owner + pet info
- Let a user add/edit tasks (duration + priority at minimum)
- Generate a daily schedule/plan based on constraints and priorities
- Display the plan clearly (and ideally explain the reasoning)
- Include tests for the most important scheduling behaviors

## Getting started

### Setup

```bash
python -m venv .venv
source .venv/bin/activate  # Windows: .venv\Scripts\activate
pip install -r requirements.txt
```

### Suggested workflow

1. Read the scenario carefully and identify requirements and edge cases.
2. Draft a UML diagram (classes, attributes, methods, relationships).
3. Convert UML into Python class stubs (no logic yet).
4. Implement scheduling logic in small increments.
5. Add tests to verify key behaviors.
6. Connect your logic to the Streamlit UI in `app.py`.
7. Refine UML so it matches what you actually built.

## 🖥️ Sample Output

Running `python3 main.py` builds an owner with two pets, prints the full schedule,
then completes the recurring daily walk to show its next occurrence being created:

```
Schedule
  2026-07-06 08:00 — Morning walk (30 min) [priority: high] for Biscuit (repeats daily)
  2026-07-06 09:00 — Breakfast (10 min) [priority: high] for Milo
  2026-07-06 10:00 — Litter box (5 min) [priority: low] for Milo
  2026-07-06 12:00 — Lunch feeding (10 min) [priority: medium] for Biscuit
  2026-07-06 18:00 — Evening walk (30 min) [priority: high] for Biscuit
  2026-07-06 19:00 — Bath (20 min) [priority: medium] for Milo (repeats weekly)

Remaining tasks after completing the daily walk
  2026-07-06 09:00 — Breakfast (10 min) [priority: high] for Milo
  2026-07-06 10:00 — Litter box (5 min) [priority: low] for Milo
  2026-07-06 12:00 — Lunch feeding (10 min) [priority: medium] for Biscuit
  2026-07-06 18:00 — Evening walk (30 min) [priority: high] for Biscuit
  2026-07-06 19:00 — Bath (20 min) [priority: medium] for Milo (repeats weekly)
  2026-07-07 08:00 — Morning walk (30 min) [priority: high] for Biscuit (repeats daily)
```

The completed 07-06 walk drops out of the remaining list, while a fresh 07-07 walk
appears automatically — demonstrating the recurring-task logic.

## 🧪 Testing PawPal+

```bash
# Run the full test suite:
pytest

# Run with coverage:
pytest --cov
```

Sample test output:

```
# Paste your pytest output here
============================= test session starts ==============================
platform darwin -- Python 3.11.1, pytest-9.1.1, pluggy-1.6.0 -- /usr/local/bin/python3
cachedir: .pytest_cache
rootdir: /Users/urvikpatel/Desktop/ai110-module2show-pawpal-starter
plugins: anyio-4.14.0
collecting ... collected 2 items

tests/test_pawpal.py::test_mark_complete_changes_status PASSED           [ 50%]
tests/test_pawpal.py::test_add_task_increases_pet_task_count PASSED      [100%]

============================== 2 passed in 0.02s ===============================
```

## 📐 Smarter Scheduling

> Fill in once you've implemented scheduling logic.

| Feature | Method(s) | Notes |
|---------|-----------|-------|
| Task sorting | def __lt__(self, other) | List is sorted by time, but you have the option to sort by priority afterwards |
| Filtering | def build_plan(self, sort_by="time", completed=None, pet_name=None) | I added in filter options to allow the user to sort by completion and or pet name if they have multiple pets |
| Conflict handling | def find_conflicts(self, task) , def add_task(self, task):, def replace_conflicts(self, task) | user has the option to replace, remove or not add a conflicting task |
| Recurring tasks | mark_complete() | If a daily task is marked complete, a new daily task spawns with the same task, but date being set to tomorrow. It will be filltered out. |

## 📸 Demo Walkthrough

Follow these numbered steps to reproduce the demo without watching a video:

1. **Launch the app.** From the project root run `streamlit run app.py`. Your browser opens to `http://localhost:8501`.
2. **Add an owner.** Under *Quick Demo Inputs*, type a name (e.g. `Jordan`) into **Add owner** and click **Add / select owner**. The owner becomes the active owner in the *Active owner* dropdown. (Add more owners to confirm each keeps its own pets.)
3. **Add a pet.** Enter a **Pet name** (e.g. `Mochi`) and pick a **Species**. The pet is created under the active owner.
4. **Add a task.** Fill in the task fields — **Title**, **Date**, **Start time**, **Duration**, **Priority**, and **Repeat** (`none`/`daily`/`weekly`) — then click **Add task**. It appears in *Current tasks*, showing its date, time, priority, and a 🔁 marker if it repeats.
5. **Trigger a conflict.** Add a second task that overlaps an existing one (same date, overlapping time). Instead of adding it, the app shows a red **Time conflict** error with two choices: **Replace existing task** or **Don't add**.
6. **Mark a task complete.** Click **Mark done** on a task. It shows struck-through with a ✅. If the task was `daily` or `weekly`, a new incomplete instance is automatically created for the next occurrence (a toast confirms the new date).
7. **Generate a schedule.** In *Build Schedule*, choose **Sort by** (`time` or `priority`), then optionally **Filter by status** (Complete/Incomplete) and **Filter by pet**. Click **Generate schedule** to see the ordered, filtered plan across the owner's pets.

**Screenshot or video** *(optional)*: <!-- Insert a screenshot or link to a demo video here -->
