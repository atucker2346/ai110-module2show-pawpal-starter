import streamlit as st
from pawpal_system import Owner, Pet, Task, Scheduler

st.set_page_config(page_title="PawPal+", page_icon="🐾", layout="centered")

st.title("🐾 PawPal+")

st.markdown(
    """
Welcome to PawPal+ - Your pet care planning assistant!

Add your pets and their care tasks, then generate a daily schedule optimized for your availability.
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

# Initialize session state for Owner if it doesn't exist
if "owner" not in st.session_state:
    st.session_state.owner = Owner(
        name="Jordan",
        available_start_hour=8,
        available_end_hour=20
    )

# Owner Information Section
st.subheader("👤 Owner Information")
col1, col2 = st.columns(2)
with col1:
    owner_name = st.text_input("Owner name", value=st.session_state.owner.name, key="owner_name_input")
    if owner_name != st.session_state.owner.name:
        st.session_state.owner.name = owner_name

with col2:
    available_hours = st.slider(
        "Available hours",
        min_value=0,
        max_value=23,
        value=(st.session_state.owner.available_start_hour, st.session_state.owner.available_end_hour),
        format="%d:00"
    )
    st.session_state.owner.available_start_hour = available_hours[0]
    st.session_state.owner.available_end_hour = available_hours[1]

st.divider()

# Pet Management Section
st.subheader("🐾 Pets")

# Display existing pets
if st.session_state.owner.pets:
    st.write("**Your Pets:**")
    for i, pet in enumerate(st.session_state.owner.pets):
        col1, col2, col3 = st.columns([3, 2, 1])
        with col1:
            st.write(f"- **{pet.name}** ({pet.species}) - {len(pet.tasks)} task(s)")
        with col2:
            if st.button(f"View Tasks", key=f"view_tasks_{i}"):
                st.session_state[f"show_tasks_{i}"] = not st.session_state.get(f"show_tasks_{i}", False)
        with col3:
            if st.button(f"Remove", key=f"remove_pet_{i}"):
                st.session_state.owner.pets.pop(i)
                st.rerun()
        
        if st.session_state.get(f"show_tasks_{i}", False):
            if pet.tasks:
                task_data = []
                for task in pet.tasks:
                    task_data.append({
                        "Task": task.title,
                        "Type": task.task_type,
                        "Duration": f"{task.duration_minutes} min",
                        "Priority": task.priority,
                        "Completed": "✅" if task.completed else "❌"
                    })
                st.dataframe(task_data, use_container_width=True)
            else:
                st.info("No tasks for this pet yet.")
else:
    st.info("No pets added yet. Add one below!")

# Add Pet Form
with st.expander("➕ Add New Pet", expanded=not st.session_state.owner.pets):
    col1, col2 = st.columns(2)
    with col1:
        new_pet_name = st.text_input("Pet name", key="new_pet_name")
    with col2:
        new_pet_species = st.selectbox("Species", ["dog", "cat", "bird", "rabbit", "other"], key="new_pet_species")
    
    if st.button("Add Pet", key="add_pet_button"):
        if new_pet_name:
            new_pet = Pet(name=new_pet_name, species=new_pet_species, owner=st.session_state.owner)
            st.session_state.owner.add_pet(new_pet)
            st.success(f"Added {new_pet_name}!")
            st.rerun()
        else:
            st.error("Please enter a pet name.")

st.divider()

# Task Management Section
st.subheader("📋 Tasks")

if not st.session_state.owner.pets:
    st.warning("Please add a pet first before adding tasks.")
else:
    # Select pet for task
    pet_options = {f"{pet.name} ({pet.species})": pet for pet in st.session_state.owner.pets}
    selected_pet_display = st.selectbox("Select pet for this task", options=list(pet_options.keys()))
    selected_pet = pet_options[selected_pet_display]
    
    col1, col2, col3, col4 = st.columns(4)
    with col1:
        task_title = st.text_input("Task title", value="Morning walk", key="task_title_input")
    with col2:
        task_type = st.selectbox(
            "Task type",
            ["walk", "feeding", "meds", "enrichment", "grooming", "other"],
            key="task_type_input"
        )
    with col3:
        duration = st.number_input("Duration (minutes)", min_value=1, max_value=240, value=20, key="duration_input")
    with col4:
        priority = st.selectbox("Priority", ["low", "medium", "high"], index=2, key="priority_input")
    
    if st.button("Add Task", key="add_task_button"):
        if task_title:
            new_task = Task(
                title=task_title,
                duration_minutes=int(duration),
                priority=priority,
                task_type=task_type
            )
            selected_pet.add_task(new_task)
            st.success(f"Added '{task_title}' for {selected_pet.name}!")
            st.rerun()
        else:
            st.error("Please enter a task title.")

st.divider()

# Schedule Generation Section
st.subheader("📅 Generate Schedule")

if not st.session_state.owner.pets:
    st.info("Add pets and tasks to generate a schedule.")
elif not any(pet.tasks for pet in st.session_state.owner.pets):
    st.info("Add tasks to your pets to generate a schedule.")
else:
    if st.button("Generate Schedule", type="primary"):
        scheduler = Scheduler(owner=st.session_state.owner)
        schedule = scheduler.generate_schedule()
        
        # Store schedule and explanation in session state
        st.session_state.schedule = schedule
        st.session_state.schedule_explanation = scheduler.explain_plan()
        st.session_state.scheduler = scheduler
        
        st.rerun()
    
    # Display schedule if it exists in session state
    if "schedule" in st.session_state and st.session_state.schedule:
        st.success("✅ Schedule generated!")
        
        # Display schedule
        st.markdown("### Today's Schedule")
        schedule_data = []
        for item in st.session_state.schedule:
            schedule_data.append({
                "Time": item["scheduled_time"],
                "Task": item["task"],
                "Pet": item["pet"],
                "Type": item["type"],
                "Duration": f"{item['duration']} min",
                "Priority": item["priority"]
            })
        st.dataframe(schedule_data, use_container_width=True)
        
        # Display explanation
        with st.expander("📝 Schedule Explanation"):
            st.text(st.session_state.schedule_explanation)
