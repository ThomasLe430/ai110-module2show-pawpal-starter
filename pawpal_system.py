from dataclasses import dataclass, field
from enum import Enum
from datetime import time

class Priority(Enum):
    LOW =  1
    MEDIUM = 2
    HIGH = 3

@dataclass
class Task:
    id: int
    name: str
    description: str
    pet_id: int
    priority: Priority       # "high", "medium", "low"
    due_date: str       # ISO date string, e.g. "2026-06-30"
    duration: int       # minutes
    status: str = "pending"

    def edit(self, fields: dict) -> None:
        """Update one or more fields on this task."""
        pass

    def mark_complete(self) -> None:
        """Set status to 'complete'."""
        pass


@dataclass
class Pet:
    id: int
    name: str
    species: str
    breed: str
    age: int
    owner_id: int
    tasks: list = field(default_factory=list)   # list[Task]

    def get_tasks(self) -> list:
        """Return all tasks associated with this pet."""
        pass

    def add_task(self, task: Task) -> None:
        """Attach a task to this pet."""
        pass

    def delete_task(self, task: Task) -> None:
        """Mark this task as deleted / remove from its pet's list."""
        pass

@dataclass
class AvailabiltyWindow:
    day: str # day of the week
    start_time: time
    end_time: time
    duration: int # minutes

@dataclass
class User:
    id: int
    name: str
    email: str
    availability_windows: list = field(default_factory=list)  # e.g. [("Mon", "09:00", "17:00"), ...]
    pets: list = field(default_factory=list)                  # list[Pet]               # list[Task]

    def add_pet(self, pet: Pet) -> None:
        """Register a pet under this user."""
        pass

    def add_availability(self, availability: AvailabiltyWindow):
        pass
    
@dataclass
class ScheduledTask:
    day: str # day of the week
    task: Task 
    user: User
    start_time: time 
    end_time: time
    duration: int 

class Planner:
    def __init__(self) -> None:
        self.users: list = []    # list[User]
        self.pets: list = []     # list[Pet]
        self.schedule: list = [] # generated schedule entries

    def add_user(self, user: User) -> None:
        """Register a user with the planner."""
        pass

    def add_pet(self, pet: Pet) -> None:
        """Track a pet in the planner."""
        pass

    def create_schedule(self) -> list:
        """Generate a schedule for all users based on availability and task priority."""
        pass

    def get_user(self, id: int) -> str:
        """Look up a user"""

    def get_pet(self, id: int) -> str:
        """Look up a user"""

    def get_task(self, id: int) -> str:
        """Look up a user"""



