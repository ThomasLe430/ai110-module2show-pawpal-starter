import calendar
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


def _next_occurrence(base: date, recurrence: "Recurrence") -> date:
    """The date of the next occurrence after `base` for a recurring cadence."""
    if recurrence == Recurrence.DAILY:
        return base + timedelta(days=1)
    if recurrence == Recurrence.WEEKLY:
        return base + timedelta(weeks=1)
    if recurrence == Recurrence.MONTHLY:
        month = base.month % 12 + 1
        year = base.year + (base.month // 12)
        day = min(base.day, calendar.monthrange(year, month)[1])
        return date(year, month, day)
    raise ValueError("ONE_TIME tasks have no next occurrence")


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

    def mark_complete(self) -> None:
        """One-time tasks close for good; recurring tasks reset to pending
        with their due date advanced to the next occurrence (e.g. a daily
        task due today rolls over to tomorrow)."""
        if self.recurrence == Recurrence.ONE_TIME:
            self.status = "complete"
        else:
            try:
                base = date.fromisoformat(self.due_date)
            except ValueError:
                base = date.today()
            self.due_date = _next_occurrence(base, self.recurrence).isoformat()
            self.status = "pending"


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
class AvailabilityWindow:
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

    def add_availability(self, availability: AvailabilityWindow):
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
DAY_INDEX = {day: i for i, day in enumerate(DAY_ORDER)}

FREQUENCY_RANK = {
    Recurrence.MONTHLY: 0,
    Recurrence.WEEKLY: 1,
    Recurrence.DAILY: 2,
}


def _week_bounds(today: date) -> tuple:
    """Return (monday, sunday) for the week containing today."""
    monday = today - timedelta(days=today.weekday())
    return monday, monday + timedelta(days=6)


def _window_date(window: AvailabilityWindow, week_start: date) -> date:
    """The calendar date this availability window falls on, this week."""
    return week_start + timedelta(days=DAY_INDEX[window.day])


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
        self._users_by_id: dict = {}
        self._pets_by_id: dict = {}

    def add_user(self, user: User) -> None:
        """Register a user with the planner."""
        self.users.append(user)
        self._users_by_id[user.id] = user

    def add_pet(self, pet: Pet) -> None:
        """Track a pet in the planner."""
        self.pets.append(pet)
        self._pets_by_id[pet.id] = pet

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
                key=lambda w: (DAY_INDEX[w.day], w.start_time),
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

    def sort_by_time(self) -> list:
        """Return the current schedule's entries sorted by their task's due date.

        Recurring tasks awaiting their next due date (due_date == "TBD")
        sort last since they have no concrete date to compare.
        """
        def due_date_key(entry: ScheduledTask) -> date:
            try:
                return date.fromisoformat(entry.task.due_date)
            except ValueError:
                return date.max

        return sorted(self.schedule, key=due_date_key)

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
            entries.sort(key=lambda e: (DAY_INDEX[e.day], e.start_time))

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
        return self._users_by_id.get(id)

    def get_pet(self, id: int) -> Optional[Pet]:
        """Look up a pet by id."""
        return self._pets_by_id.get(id)

    def filter_by_pet(self, pet_id: int) -> list:
        """Return all tasks belonging to the given pet, or [] if the pet is unknown."""
        pet = self.get_pet(pet_id)
        return pet.tasks if pet is not None else []

    def get_task(self, id: int) -> Optional[Task]:
        """Look up a task by id across all tracked pets."""
        for pet in self.pets:
            for task in pet.tasks:
                if task.id == id:
                    return task
        return None



