from pawpal_system import Priority, Recurrence, Task, Pet, AvailabiltyWindow, User, ScheduledTask, Planner
from datetime import time

OWNER_ID = 1234
OWNER_NAME = "Thomas"
PET_ID = 123
TASK_ID_1 = 1
TASK_ID_2 = 2
TASK_ID_3 = 3

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

# Create availability windows and add pet
mondAvailability = [AvailabiltyWindow("Mon", time(8, 0, 0), time(9,0, 0), 60),
                    AvailabiltyWindow("Mon", time(12, 0, 0), time(13,0, 0), 60), 
                    AvailabiltyWindow("Mon", time(17, 0, 0), time(17,30, 0), 30)]
tuesAvailability = [AvailabiltyWindow("Tue", time(14, 0, 0), time(16,0, 0), 120)]
wedAvailability = [AvailabiltyWindow("Wed", time(12, 0, 0), time(3,0, 0), 180)]
thurAvailability = [AvailabiltyWindow("Thu", time(12, 0, 0), time(13,0, 0), 60)]
friAvailability = [AvailabiltyWindow("Fri", time(12, 0, 0), time(13,0, 0), 60)]
satAvailability = [AvailabiltyWindow("Sat", time(12, 0, 0), time(13,0, 0), 60)]
sunAvailability = [AvailabiltyWindow("Sun", time(12, 0, 0), time(16,0, 0), 240)]

ownerAvailability =  mondAvailability + tuesAvailability + wedAvailability + thurAvailability + friAvailability + satAvailability + sunAvailability
newOwner = User(OWNER_ID, OWNER_NAME, "thole@g.hmc.edu", ownerAvailability)
newOwner.add_pet(kiwiCat)

# Create Planner and add information
planner = Planner()
planner.add_user(newOwner)
planner.add_pet(kiwiCat)
newSched = planner.create_schedule()
planner.print_schedule()
