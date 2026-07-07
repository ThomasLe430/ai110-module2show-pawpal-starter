import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from pawpal_system import Task, Pet, Priority, Recurrence


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
