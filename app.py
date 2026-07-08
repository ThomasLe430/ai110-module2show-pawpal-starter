import streamlit as st
from pawpal_system import Priority, Recurrence, Task, Pet, AvailabiltyWindow, User, ScheduledTask, Planner, DAY_ORDER
from datetime import time, date, datetime

DEFAULT_USER_ID = 1
DEFAULT_PET_ID = 10
DEFAULT_TASK_ID = 100

st.set_page_config(page_title="PawPal+", page_icon="🐾", layout="centered")

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

st.subheader("Sign Up")
st.caption("Enter your name and email to get started.")


# Planner to hold user, pets, and tasks
if "planner" not in st.session_state:
     st.session_state.planner = Planner()

# Sign up Form for the User
if "user" not in st.session_state:
    with st.form("signup_form"):
        name_input = st.text_input("Name", value="John Doe")
        email_input = st.text_input("Email", value="johnDoe@example.com")
        submitted = st.form_submit_button("Sign Up")

    if submitted:
        st.session_state.user = User(id=DEFAULT_USER_ID, name=name_input, email=email_input)
        st.session_state.planner.add_user(st.session_state.user)
        st.rerun()
else:
    user = st.session_state.user
    st.success(f"Signed in as **{user.name}** ({user.email})")
    if st.button("Sign out"):
        del st.session_state["user"]
        st.rerun()

st.divider()

# After sign up, continue to rest of site
if "user" not in st.session_state:
    st.info("Sign up above to continue.")
else:
    # Pet Registration
    st.subheader("Pets")

    if "pets" not in st.session_state:
        st.session_state.pets = []

    if "next_pet_id" not in st.session_state:
        st.session_state.next_pet_id = DEFAULT_PET_ID

    with st.form("add_pet", clear_on_submit=True):
        st.caption("Add information about your pet:")
        pet_name_input = st.text_input("Pet Name: ", value="[Enter Name]")
        species_input = st.text_input("Pet Species", value="[Enter Species]")
        breed_input = st.text_input("Pet Breed: ", value="[Enter Breed]")
        age_input = st.number_input("Age (Years): ", value=1)

        submitted = st.form_submit_button("Add Pet")

    if submitted:
        newPet = Pet(id=st.session_state.next_pet_id, name=pet_name_input, species=species_input,
                     breed=breed_input, age=age_input, owner_id=st.session_state["user"].id)
        st.session_state.next_pet_id += 1 # For Unique IDs

        st.session_state.pets.append(newPet)
        st.session_state.user.add_pet(newPet)
        st.session_state.planner.add_pet(newPet)
        st.success(f"Registered {pet_name_input}!")

    # Display table of pet information
    st.markdown("#### Pet Information:")
    petInfoCol1, petInfoCol2, petInfoCol3, petInfoCol4 = st.columns(4)
    with petInfoCol1:
        for pet in st.session_state.pets:
            st.markdown("**Name:**")
            st.write(pet.name)
    with petInfoCol2:
        for pet in st.session_state.pets:
            st.write("**Species:**")
            st.write(pet.species)
    with petInfoCol3:
        for pet in st.session_state.pets:
            st.write("**Breed:**")
            st.write(pet.breed)
    with petInfoCol4:
        for pet in st.session_state.pets:
            st.write("**Age:**")
            st.write(pet.age)

    st.markdown("### Tasks")
    st.caption("These tasks can include daily exercise, feeding, grooming, and vet appointments.")

    # Task Storage
    if "tasks" not in st.session_state:
        st.session_state.tasks = []

    # Task Input
    if "next_task_id" not in st.session_state:
        st.session_state.next_task_id = DEFAULT_TASK_ID

    if not st.session_state.pets:
        st.info("Add a pet above before creating tasks.")
    else:
        with st.form("add_task", clear_on_submit=True):
            task_pet = st.selectbox("Which Pet? ", st.session_state.pets, format_func=lambda pet: pet.name)
            task_title = st.text_input("Task Title: ", value="[Morning walk]")
            task_desc = st.text_input("Description: ", value="[]")
            task_priority = st.selectbox("Priority: ", ["low", "medium", "high"], index=1)
            task_recurrence = st.selectbox("Recurrence: ", ["one_time", "daily", "weekly", "monthly"], index=2)
            task_due_date = st.date_input("Due Date: ")
            task_duration = st.number_input("Duration (Min): ", min_value=1,max_value=240, value=30)
            task_submitted = st.form_submit_button("Add Task")

        if task_submitted:
            # st.selectbox can hand back a stale cached copy of the Pet rather than the
            # live object in st.session_state.pets, so look the pet up by id to mutate
            # the one everything else (planner, user) actually references.
            live_pet = next(pet for pet in st.session_state.pets if pet.id == task_pet.id)
            new_task = Task(
                id=st.session_state.next_task_id,
                name=task_title,
                description=task_desc,
                pet_id=live_pet.id,
                priority=Priority[task_priority.upper()],
                due_date=task_due_date.isoformat(),
                duration=task_duration,
                recurrence=Recurrence[task_recurrence.upper()],
            )
            live_pet.add_task(new_task)
            st.session_state.tasks.append(new_task)
            st.session_state.next_task_id += 1
            st.success(f"Added task '{task_title}' for {live_pet.name}!")
    # Display Current Tasks
    if st.session_state.tasks:
        st.write("Current tasks:")
        pet_names_by_id = {pet.id: pet.name for pet in st.session_state.pets}
        task_rows = [
            {
                "Pet": pet_names_by_id.get(task.pet_id, "Unknown"),
                "Task": task.name,
                "Description": task.description,
                "Priority": task.priority.name.title(),
                "Recurrence": task.recurrence.name.title(),
                "Due Date": task.due_date,
                "Duration (min)": task.duration,
                "Status": task.status.title(),
            }
            for task in st.session_state.tasks
        ]
        st.table(task_rows)
    else:
        st.info("No tasks yet. Add one above.")

    st.divider()

    st.subheader("Add Availabilty")
    st.caption(
        "Add the times you're free each week to take care of your pet(s). "
        "Windows repeat every week on the chosen day."
    )

    today = date.today()
    today_name = DAY_ORDER[today.weekday()]

    with st.form("add_availability", clear_on_submit=True):
        avail_day = st.selectbox("Day of Week: ", DAY_ORDER)
        avail_start = st.time_input("Start Time: ", value=time(9, 0))
        avail_end = st.time_input("End Time: ", value=time(17, 0))
        avail_submitted = st.form_submit_button("Add Availability")

    if avail_submitted:
        if avail_end <= avail_start:
            st.error("End time must be after start time.")
        else:
            duration_minutes = int(
                (datetime.combine(today, avail_end) - datetime.combine(today, avail_start)).total_seconds() // 60
            )
            new_window = AvailabiltyWindow(
                day=avail_day,
                start_time=avail_start,
                end_time=avail_end,
                duration=duration_minutes,
            )
            st.session_state.user.add_availability(new_window)
            st.success(f"Added availability: {avail_day} {avail_start.strftime('%H:%M')}-{avail_end.strftime('%H:%M')}")

    # Display Current Availability
    if st.session_state.user.availability_windows:
        st.write("Current availability:")
        avail_rows = [
            {
                "Day": window.day,
                "Start": window.start_time.strftime("%H:%M"),
                "End": window.end_time.strftime("%H:%M"),
                "Duration (min)": window.duration,
            }
            for window in sorted(
                st.session_state.user.availability_windows,
                key=lambda w: (DAY_ORDER.index(w.day), w.start_time),
            )
        ]
        st.table(avail_rows)
    else:
        st.info("No availability added yet. Add a window above.")

    st.subheader("Build Schedule")
    st.caption("Generate a schedule based on your availability, priority, and due date of the pet tasks.")

    if st.button("Generate schedule"):
        st.session_state.planner.create_schedule()

    planner = st.session_state.planner
    if planner.schedule or planner.unscheduled:
        user_entries = [entry for entry in planner.schedule if entry.user.id == st.session_state.user.id]

        st.markdown("#### Your Weekly Schedule")
        if user_entries:
            user_entries.sort(key=lambda e: (DAY_ORDER.index(e.day), e.start_time))
            schedule_rows = [
                {
                    "Day": entry.day,
                    "Start": entry.start_time.strftime("%H:%M"),
                    "End": entry.end_time.strftime("%H:%M"),
                    "Pet": planner.get_pet(entry.task.pet_id).name,
                    "Task": entry.task.name,
                    "Priority": entry.task.priority.name.title(),
                }
                for entry in user_entries
            ]
            st.table(schedule_rows)
        else:
            st.info("No tasks could be scheduled this week.")

        user_unscheduled = [task for task in planner.unscheduled if task.pet_id in {pet.id for pet in st.session_state.pets}]
        if user_unscheduled:
            st.markdown("#### Could Not Be Scheduled")
            st.caption("These tasks didn't fit in your available windows this week.")
            unscheduled_rows = [
                {
                    "Pet": planner.get_pet(task.pet_id).name,
                    "Task": task.name,
                    "Priority": task.priority.name.title(),
                    "Due Date": task.due_date,
                }
                for task in user_unscheduled
            ]
            st.table(unscheduled_rows)
