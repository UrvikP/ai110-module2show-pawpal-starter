from datetime import time, date

import streamlit as st

from pawpal_system import Owner, Pet, Task, Scheduler

st.set_page_config(page_title="PawPal+", page_icon="🐾", layout="centered")


def format_time(minutes):
    """Convert minutes-since-midnight (int) into a readable HH:MM string."""
    hours, mins = divmod(minutes, 60)
    return f"{hours:02d}:{mins:02d}"


def get_or_create_pet(owner, name, pet_type):
    """Return the owner's pet with this name, creating it if it doesn't exist."""
    for pet in owner.pets:
        if pet.name == name:
            pet.pet_type = pet_type  # keep type in sync with the UI selection
            return pet
    return owner.add_pet(name, pet_type)

st.title("🐾 PawPal+")

st.markdown(
    """
Welcome to the PawPal+ starter app.

This file is intentionally thin. It gives you a working Streamlit app so you can start quickly,
but **it does not implement the project logic**. Your job is to design the system and build it.

Use this app as your interactive demo once your backend classes/functions exist.
"""
)

with st.expander("Scenario", expanded=True):
    st.markdown(
        """
**PawPal+** is a pet care planning assistant. It helps a pet owner plan care tasks
for their pet(s) based on constraints like time, priority, and preferences.

You will design and implement the scheduling logic and connect it to this Streamlit UI.
"""
    )

with st.expander("What you need to build", expanded=True):
    st.markdown(
        """
At minimum, your system should:
- Represent pet care tasks (what needs to happen, how long it takes, priority)
- Represent the pet and the owner (basic info and preferences)
- Build a plan/schedule for a day that chooses and orders tasks based on constraints
- Explain the plan (why each task was chosen and when it happens)
"""
    )

st.divider()

st.subheader("Quick Demo Inputs")

# Persist MANY owners across reruns, keyed by name. Each name maps to its own
# Owner object with its own pets, so pets never leak between owners.
if "owners" not in st.session_state:
    st.session_state.owners = {}

# Create a new owner by name.
new_owner_name = st.text_input("Add owner", value="Jordan")
if st.button("Add / select owner") and new_owner_name:
    if new_owner_name not in st.session_state.owners:
        st.session_state.owners[new_owner_name] = Owner(new_owner_name)
    st.session_state.active_owner = new_owner_name

# Choose which owner is active. Everything below operates on this owner only.
if not st.session_state.owners:
    st.info("Add an owner above to get started.")
    st.stop()

owner_names = list(st.session_state.owners.keys())
default_index = (
    owner_names.index(st.session_state.active_owner)
    if st.session_state.get("active_owner") in st.session_state.owners
    else 0
)
selected_owner = st.selectbox("Active owner", owner_names, index=default_index)
owner = st.session_state.owners[selected_owner]  # the ONE chosen owner

pet_name = st.text_input("Pet name", value="Mochi")
species = st.selectbox("Species", ["dog", "cat", "other"])

# Get (or create) the pet under THIS owner only.
pet = get_or_create_pet(owner, pet_name, species)

st.markdown("### Tasks")
st.caption("Add tasks for the pet above. They persist across reruns via session_state.")

row1_col1, row1_col2, row1_col3 = st.columns(3)
with row1_col1:
    task_title = st.text_input("Task title", value="Morning walk")
with row1_col2:
    task_date = st.date_input("Date", value=date.today())
with row1_col3:
    start = st.time_input("Start time", value=time(8, 0))

row2_col1, row2_col2, row2_col3 = st.columns(3)
with row2_col1:
    duration = st.number_input("Duration (minutes)", min_value=1, max_value=240, value=20)
with row2_col2:
    priority = st.selectbox("Priority", ["low", "medium", "high"], index=2)
with row2_col3:
    frequency = st.selectbox("Repeat", ["none", "daily", "weekly"])

if st.button("Add task"):
    time_start = start.hour * 60 + start.minute  # minutes since midnight
    new_task = Task(
        time_start, task_title, int(duration), priority,
        frequency=frequency, date=task_date,
    )
    conflicts = pet.add_task(new_task)  # returns conflicts (and skips adding) on overlap
    if conflicts:
        # Stash the blocked task so the user can choose replace vs. skip.
        st.session_state.pending_task = new_task
        st.session_state.pending_pet = pet
    # (No conflict -> add_task already added it; nothing more to do.)

# Conflict resolution: shown only when an add was blocked by an overlap.
pending_task = st.session_state.get("pending_task")
if pending_task is not None:
    conflict_pet = st.session_state.get("pending_pet")
    conflicts = conflict_pet.find_conflicts(pending_task)
    conflict_desc = ", ".join(
        f"'{c.description}' at {c.date} {format_time(c.time_start)}" for c in conflicts
    )
    st.error(
        f"Time conflict: '{pending_task.description}' at "
        f"{pending_task.date} {format_time(pending_task.time_start)} overlaps with "
        f"{conflict_desc}. Choose how to resolve it."
    )
    replace_col, skip_col = st.columns(2)
    with replace_col:
        if st.button("Replace existing task"):
            conflict_pet.replace_conflicts(pending_task)  # swap old out, new in
            st.session_state.pending_task = None
            st.rerun()
    with skip_col:
        if st.button("Don't add"):
            st.session_state.pending_task = None  # discard the new task
            st.rerun()

tasks = pet.get_tasks()
if tasks:
    st.write(f"Current tasks for {pet.name}:")
    for i, t in enumerate(tasks):
        info_col, action_col = st.columns([4, 1])
        # Strike-through completed tasks so their status is visually clear.
        repeat = "" if t.frequency == "none" else f" 🔁 {t.frequency}"
        label = (
            f"{t.date} {format_time(t.time_start)} — {t.description} "
            f"({t.duration_min} min) [priority: {t.priority}]{repeat}"
        )
        with info_col:
            st.markdown(f"~~{label}~~ ✅" if t.completed else label)
        with action_col:
            if t.completed:
                st.write("Done")
            # Unique key per task so Streamlit tracks each button separately.
            elif st.button("Mark done", key=f"done_{selected_owner}_{pet.name}_{i}"):
                # Recurring tasks spawn their next occurrence here.
                spawned = t.mark_complete()  # wire Task.mark_complete()
                if spawned is not None:
                    st.toast(f"Next '{spawned.description}' scheduled for {spawned.date}.")
                st.rerun()  # refresh so the row shows as completed immediately
else:
    st.info("No tasks yet. Add one above.")

st.divider()

st.subheader("Build Schedule")
st.caption("Builds a plan across all of the owner's pets using the Scheduler.")

sort_by = st.selectbox("Sort by", ["time", "priority"], index=0)

# Filter controls. "All" maps to None so build_plan skips that filter.
status_choice = st.selectbox("Filter by status", ["All", "Incomplete", "Complete"])
completed = {"All": None, "Incomplete": False, "Complete": True}[status_choice]

pet_options = ["All"] + [p.name for p in owner.pets]
pet_choice = st.selectbox("Filter by pet", pet_options)
pet_filter = None if pet_choice == "All" else pet_choice

if st.button("Generate schedule"):
    scheduler = Scheduler(owner)  # data source: the persisted Owner
    plan = scheduler.build_plan(sort_by, completed=completed, pet_name=pet_filter)
    if plan:
        st.write(f"Schedule for {owner.name}:")
        for t in plan:
            repeat = "" if t.frequency == "none" else f" 🔁 {t.frequency}"
            st.write(
                f"- {t.date} {format_time(t.time_start)} — {t.description} "
                f"({t.duration_min} min) [priority: {t.priority}] for {t.pet.name}{repeat}"
            )
    else:
        st.info("No tasks match the current filters (or none added yet).")
