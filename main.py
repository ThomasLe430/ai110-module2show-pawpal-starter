from pawpal_system import Priority, Recurrence, Task, Pet, AvailabilityWindow, User, ScheduledTask, Planner
from datetime import time

OWNER_ID = 1234
OWNER_NAME = "Thomas"
PET_ID = 123
PET_ID_2 = PET_ID + 1
TASK_ID_1 = 1
TASK_ID_2 = TASK_ID_1 + 1
TASK_ID_3 = TASK_ID_1 + 2
TASK_ID_4 = TASK_ID_1 + 3

# Create Pet cat and add tasks
kiwiCat = Pet(PET_ID, "Kiwi", "Cat", "American Shorthair", 3, OWNER_ID)

task1 = Task(TASK_ID_1, "Feed", "Give cat wet food.", PET_ID, Priority.MEDIUM, 
             due_date="2026-07-06", duration=5, recurrence=Recurrence.DAILY)
task2 = Task(TASK_ID_2, "Vet Appointment", "Check up and medicine", PET_ID, Priority.HIGH, 
             due_date="2026-07-10", duration=120, recurrence=Recurrence.ONE_TIME)
task3 = Task(TASK_ID_3, "Bath", "She quite stinky", PET_ID, Priority.LOW, 
             due_date="2026-07-29", duration=60, recurrence=Recurrence.MONTHLY)

kiwiCat.add_task(task1)
kiwiCat.add_task(task2)
kiwiCat.add_task(task3)

# Create Pet Dog and add tasks
myDog = Pet(id=PET_ID_2, name="Lucky", species="Dog", breed="Yorkie",
            age=10, owner_id=OWNER_ID)
task4 = Task(id=TASK_ID_4, name="Walk dog", description="Walk dog around park", pet_id=PET_ID_2,
             priority=Priority.MEDIUM, due_date="2026-07-07", duration=30, recurrence=Recurrence.DAILY)

myDog.add_task(task4)

# Create availability windows and add pet
mondAvailability = [AvailabilityWindow("Mon", time(8, 0, 0), time(9,0, 0), 60),
                    AvailabilityWindow("Mon", time(12, 0, 0), time(13,0, 0), 60), 
                    AvailabilityWindow("Mon", time(17, 0, 0), time(17,30, 0), 30)]
tuesAvailability = [AvailabilityWindow("Tue", time(14, 0, 0), time(16,0, 0), 120)]
wedAvailability = [AvailabilityWindow("Wed", time(12, 0, 0), time(3,0, 0), 180)]
thurAvailability = [AvailabilityWindow("Thu", time(12, 0, 0), time(13,0, 0), 60)]
friAvailability = [AvailabilityWindow("Fri", time(12, 0, 0), time(13,0, 0), 60)]
satAvailability = [AvailabilityWindow("Sat", time(12, 0, 0), time(13,0, 0), 60)]
sunAvailability = [AvailabilityWindow("Sun", time(12, 0, 0), time(16,0, 0), 240)]

ownerAvailability =  mondAvailability + tuesAvailability + wedAvailability + thurAvailability + friAvailability + satAvailability + sunAvailability
newOwner = User(OWNER_ID, OWNER_NAME, "thole@g.hmc.edu", ownerAvailability)
newOwner.add_pet(kiwiCat)
newOwner.add_pet(myDog)

# Create Planner and add information
planner = Planner()
planner.add_user(newOwner)
planner.add_pet(kiwiCat)
planner.add_pet(myDog)

# Print Schedule
newSched = planner.create_schedule()
planner.print_schedule()

# Test Sorting and Filtering capabilities
sortedTasks = planner.sort_by_time()
print("Tasks Sorted by Time:")
for task in sortedTasks:
    print(task.task.name,"-", task.task.due_date)
print()


print("Task sorted by Pet")

filterByKiwi = planner.filter_by_pet(kiwiCat.id)
print("Kiwi:")
for task in filterByKiwi:
    print(task.name)

filterByLucky = planner.filter_by_pet(myDog.id)
print("Lucky:")
for task in filterByLucky:
    print(task.name)

