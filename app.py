from datetime import time

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
owner_name = st.text_input("Owner name", value="Jordan")
pet_name = st.text_input("Pet name", value="Mochi")
species = st.selectbox("Species", ["dog", "cat", "other"])

# Persist a single Owner across reruns. Guarding with the "not in" check means
# it is created once, not rebuilt (and emptied) on every rerun.
if "owner" not in st.session_state:
    st.session_state.owner = Owner(owner_name)
owner = st.session_state.owner
owner.name = owner_name  # keep the owner's name in sync with the UI field

# Get (or create) the pet the tasks will be added to.
pet = get_or_create_pet(owner, pet_name, species)

st.markdown("### Tasks")
st.caption("Add tasks for the pet above. They persist across reruns via session_state.")

col1, col2, col3, col4 = st.columns(4)
with col1:
    task_title = st.text_input("Task title", value="Morning walk")
with col2:
    start = st.time_input("Start time", value=time(8, 0))
with col3:
    duration = st.number_input("Duration (minutes)", min_value=1, max_value=240, value=20)
with col4:
    priority = st.selectbox("Priority", ["low", "medium", "high"], index=2)

if st.button("Add task"):
    time_start = start.hour * 60 + start.minute  # minutes since midnight
    pet.add_task(Task(time_start, task_title, int(duration), priority))

if pet.get_tasks():
    st.write(f"Current tasks for {pet.name}:")
    st.table(
        [
            {
                "time": format_time(t.time_start),
                "title": t.description,
                "duration_min": t.duration_min,
                "priority": t.priority,
                "done": t.completed,
            }
            for t in pet.get_tasks()
        ]
    )
else:
    st.info("No tasks yet. Add one above.")

st.divider()

st.subheader("Build Schedule")
st.caption("Builds a plan across all of the owner's pets using the Scheduler.")

sort_by = st.selectbox("Sort by", ["time", "priority"], index=0)

if st.button("Generate schedule"):
    scheduler = Scheduler(owner)  # data source: the persisted Owner
    plan = scheduler.build_plan(sort_by)
    if plan:
        st.write(f"Today's schedule for {owner.name}:")
        for t in plan:
            st.write(
                f"- {format_time(t.time_start)} — {t.description} "
                f"({t.duration_min} min) [priority: {t.priority}] for {t.pet.name}"
            )
    else:
        st.info("No tasks to schedule yet. Add some above.")
