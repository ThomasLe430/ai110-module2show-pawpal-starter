from dataclasses import dataclass, field
from enum import Enum
from datetime import time, date, datetime, timedelta
from typing import Optional

class Priority(Enum):
    LOW =  1
    MEDIUM = 2
    HIGH = 3

class Recurrence(Enum):
    ONE_TIME = 1
    DAILY = 2
    WEEKLY = 3
    MONTHLY = 4

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
    recurrence: Recurrence = Recurrence.ONE_TIME

    def edit(self, fields: dict) -> None:
        """Update one or more fields on this task."""
        pass

    def mark_complete(self) -> None:
        """One-time tasks close for good; recurring tasks reset to pending
        for their next occurrence instead of staying complete."""
        if self.recurrence == Recurrence.ONE_TIME:
            self.status = "complete"
        else:
            self.status = "pending"
            self.due_date = "TBD"  # placeholder until recurrence-based date math is added


@dataclass
class Pet:
    id: int
    name: str
    species: str
    breed: str
    age: int
    owner_id: int
    numTasks: int = 0
    tasks: list = field(default_factory=list)   # list[Task]

    def get_tasks(self) -> list:
        """Return all tasks associated with this pet."""
        return self.tasks

    def add_task(self, task: Task) -> None:
        """Attach a task to this pet."""
        self.tasks.append(task)
        self.numTasks = len(self.tasks)

    def delete_task(self, task: Task) -> None:
        """Mark this task as deleted / remove from its pet's list."""
        self.tasks.remove(task)
        self.numTasks = len(self.tasks)

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
        self.pets.append(pet)

    def add_availability(self, availability: AvailabiltyWindow):
        """Add an availability window for this user."""
        self.availability_windows.append(availability)
    
@dataclass
class ScheduledTask:
    day: str # day of the week
    task: Task 
    user: User
    start_time: time 
    end_time: time
    duration: int 

DAY_ORDER = ["Mon", "Tue", "Wed", "Thu", "Fri", "Sat", "Sun"]

FREQUENCY_RANK = {
    Recurrence.MONTHLY: 0,
    Recurrence.WEEKLY: 1,
    Recurrence.DAILY: 2,
}


def _week_bounds(today: date) -> tuple:
    """Return (monday, sunday) for the week containing today."""
    monday = today - timedelta(days=today.weekday())
    return monday, monday + timedelta(days=6)


def _window_date(window: AvailabiltyWindow, week_start: date) -> date:
    """The calendar date this availability window falls on, this week."""
    return week_start + timedelta(days=DAY_ORDER.index(window.day))


def _advance_time(t: time, minutes: int) -> time:
    """Add minutes to a time-of-day value."""
    return (datetime.combine(date(2000, 1, 1), t) + timedelta(minutes=minutes)).time()


def _fit_task(task, windows, windows_state, week_start, user, deadline):
    """First-fit task into the earliest candidate window with room left.

    Windows must already be in chronological order. If deadline is given,
    only windows on or before that date are considered. Returns the
    resulting ScheduledTask, or None if the task doesn't fit anywhere.
    """
    for window in windows:
        if deadline is not None and _window_date(window, week_start) > deadline:
            break
        state = windows_state[id(window)]
        if state["remaining"] >= task.duration:
            start = state["cursor"]
            end = _advance_time(start, task.duration)
            state["cursor"] = end
            state["remaining"] -= task.duration
            return ScheduledTask(
                day=window.day,
                task=task,
                user=user,
                start_time=start,
                end_time=end,
                duration=task.duration,
            )
    return None


class Planner:
    def __init__(self) -> None:
        """Initialize an empty planner with no users, pets, or schedule."""
        self.users: list = []       # list[User]
        self.pets: list = []        # list[Pet]
        self.schedule: list = []    # generated schedule entries
        self.unscheduled: list = [] # tasks that didn't fit anywhere this week

    def add_user(self, user: User) -> None:
        """Register a user with the planner."""
        self.users.append(user)

    def add_pet(self, pet: Pet) -> None:
        """Track a pet in the planner."""
        self.pets.append(pet)

    def create_schedule(self, today: Optional[date] = None) -> list:
        """Generate this week's schedule for all users.

        Tasks are scheduled in two tiers: one-time tasks due this week
        first (by priority, then due date), then recurring tasks (by
        frequency - monthly, weekly, daily - then priority). Within each
        tier, tasks are greedily first-fit into the user's availability
        windows in chronological order. Tasks that don't fit anywhere are
        recorded in self.unscheduled rather than displacing anything
        already placed.
        """
        if today is None:
            today = date.today()
        week_start, week_end = _week_bounds(today)

        self.schedule = []
        self.unscheduled = []

        for user in self.users:
            pending_tasks = [
                task for pet in user.pets for task in pet.tasks
                if task.status == "pending"
            ]

            due_this_week = [
                task for task in pending_tasks
                if task.recurrence == Recurrence.ONE_TIME
                and date.fromisoformat(task.due_date) <= week_end
            ]
            due_this_week.sort(key=lambda t: (-t.priority.value, t.due_date))

            recurring = [
                task for task in pending_tasks
                if task.recurrence != Recurrence.ONE_TIME
            ]
            recurring.sort(key=lambda t: (FREQUENCY_RANK[t.recurrence], -t.priority.value))

            windows = sorted(
                user.availability_windows,
                key=lambda w: (DAY_ORDER.index(w.day), w.start_time),
            )
            windows_state = {
                id(w): {"remaining": w.duration, "cursor": w.start_time}
                for w in windows
            }

            for task in due_this_week:
                due = date.fromisoformat(task.due_date)
                # Overdue tasks (due before this week) get no deadline cutoff -
                # schedule them as soon as there's room, rather than excluding them.
                deadline = due if due >= week_start else None
                self._place(task, windows, windows_state, week_start, user, deadline)

            for task in recurring:
                if task.recurrence == Recurrence.DAILY:
                    for day in DAY_ORDER:
                        day_windows = [w for w in windows if w.day == day]
                        self._place(task, day_windows, windows_state, week_start, user, None)
                else:
                    self._place(task, windows, windows_state, week_start, user, None)

        return self.schedule

    def _place(self, task, candidate_windows, windows_state, week_start, user, deadline) -> None:
        """Schedule the task if it fits, otherwise record it as unscheduled."""
        scheduled = _fit_task(task, candidate_windows, windows_state, week_start, user, deadline)
        if scheduled is not None:
            self.schedule.append(scheduled)
        else:
            self.unscheduled.append(task)

    def print_schedule(self) -> None:
        """Print the most recently generated schedule, grouped by user and
        by day, plus a list of anything that didn't fit this week."""
        if not self.schedule:
            print("No tasks scheduled.")

        by_user = {}
        for entry in self.schedule:
            by_user.setdefault(entry.user.id, []).append(entry)

        for user in self.users:
            entries = by_user.get(user.id)
            if not entries:
                continue
            entries.sort(key=lambda e: (DAY_ORDER.index(e.day), e.start_time))

            print(f"=== {user.name}'s Weekly Schedule ===")
            current_day = None
            for entry in entries:
                if entry.day != current_day:
                    current_day = entry.day
                    print(f"\n{current_day}:")
                start = entry.start_time.strftime("%H:%M")
                end = entry.end_time.strftime("%H:%M")
                print(f"  {self.get_pet(entry.task.pet_id).name}: {start}-{end}  {entry.task.name} ({entry.task.priority.name})")
            print()

        if self.unscheduled:
            print("--- Could not be scheduled this week ---")
            for task in self.unscheduled:
                print(f"  {task.name} ({task.priority.name})")

    def get_user(self, id: int) -> Optional[User]:
        """Look up a user by id."""
        for user in self.users:
            if user.id == id:
                return user
        return None

    def get_pet(self, id: int) -> Optional[Pet]:
        """Look up a pet by id."""
        for pet in self.pets:
            if pet.id == id:
                return pet
        return None

    def get_task(self, id: int) -> Optional[Task]:
        """Look up a task by id across all tracked pets."""
        for pet in self.pets:
            for task in pet.tasks:
                if task.id == id:
                    return task
        return None



