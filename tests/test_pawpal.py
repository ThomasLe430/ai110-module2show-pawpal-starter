import sys
from pathlib import Path
from datetime import time

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from pawpal_system import (
    Task,
    Pet,
    Priority,
    Recurrence,
    Planner,
    User,
    ScheduledTask,
)


def test_mark_complete_one_time_task_sets_status_complete():
    task = Task(
        id=1,
        name="Vet visit",
        description="Annual checkup",
        pet_id=1,
        priority=Priority.HIGH,
        due_date="2026-07-10",
        duration=30,
        recurrence=Recurrence.ONE_TIME,
    )

    task.mark_complete()

    assert task.status == "complete"


def test_add_task_increases_pet_task_count():
    pet = Pet(
        id=1,
        name="Rex",
        species="Dog",
        breed="Labrador",
        age=3,
        owner_id=1,
    )
    task = Task(
        id=1,
        name="Walk",
        description="Evening walk",
        pet_id=pet.id,
        priority=Priority.LOW,
        due_date="2026-07-10",
        duration=20,
    )

    pet.add_task(task)

    assert pet.numTasks == 1
    assert task in pet.get_tasks()


def test_sort_by_time_orders_schedule_entries_by_due_date():
    user = User(id=1, name="Alex", email="alex@example.com")

    task_later = Task(
        id=1,
        name="Grooming",
        description="Trim nails",
        pet_id=1,
        priority=Priority.LOW,
        due_date="2026-07-20",
        duration=15,
    )
    task_earlier = Task(
        id=2,
        name="Vet visit",
        description="Checkup",
        pet_id=1,
        priority=Priority.HIGH,
        due_date="2026-07-08",
        duration=30,
    )
    task_middle = Task(
        id=3,
        name="Walk",
        description="Evening walk",
        pet_id=2,
        priority=Priority.MEDIUM,
        due_date="2026-07-12",
        duration=20,
    )

    planner = Planner()
    planner.schedule = [
        ScheduledTask(day="Mon", task=task_later, user=user, start_time=time(9, 0), end_time=time(9, 15), duration=15),
        ScheduledTask(day="Tue", task=task_earlier, user=user, start_time=time(10, 0), end_time=time(10, 30), duration=30),
        ScheduledTask(day="Wed", task=task_middle, user=user, start_time=time(17, 0), end_time=time(17, 20), duration=20),
    ]

    sorted_entries = planner.sort_by_time()

    assert [entry.task.id for entry in sorted_entries] == [2, 3, 1]


def test_filter_by_pet_returns_only_that_pets_tasks():
    rex = Pet(id=1, name="Rex", species="Dog", breed="Labrador", age=3, owner_id=1)
    whiskers = Pet(id=2, name="Whiskers", species="Cat", breed="Tabby", age=2, owner_id=1)

    rex_task = Task(
        id=1,
        name="Walk",
        description="Evening walk",
        pet_id=rex.id,
        priority=Priority.LOW,
        due_date="2026-07-10",
        duration=20,
    )
    whiskers_task = Task(
        id=2,
        name="Litter box",
        description="Clean litter box",
        pet_id=whiskers.id,
        priority=Priority.MEDIUM,
        due_date="2026-07-09",
        duration=10,
    )
    rex.add_task(rex_task)
    whiskers.add_task(whiskers_task)

    planner = Planner()
    planner.add_pet(rex)
    planner.add_pet(whiskers)

    assert planner.filter_by_pet(rex.id) == [rex_task]
    assert planner.filter_by_pet(whiskers.id) == [whiskers_task]
    assert planner.filter_by_pet(999) == []
