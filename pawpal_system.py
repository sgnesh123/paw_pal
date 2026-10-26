"""PawPal+ core system: Owner, Pet, Task, and Scheduler.

Classes follow diagrams/uml_draft.mmd.
Times are stored as minutes since midnight (e.g. 8:00 AM -> 480).
"""

from __future__ import annotations

from dataclasses import dataclass, field
from datetime import date

PRIORITY_RANK = {"low": 1, "medium": 2, "high": 3}


def to_minutes(hhmm: str) -> int:
    """Convert an "HH:MM" string to minutes since midnight."""
    hours, minutes = hhmm.strip().split(":")
    return int(hours) * 60 + int(minutes)


def format_time(minutes: int) -> str:
    """Convert minutes since midnight to an "HH:MM" string."""
    return f"{minutes // 60:02d}:{minutes % 60:02d}"


# eq=False keeps identity-based equality, so lookups and removals match the
# exact object rather than any task/pet with the same field values.
@dataclass(eq=False)
class Task:
    """A single pet care task (walk, feeding, meds, enrichment, grooming, ...)."""

    description: str
    duration_minutes: int
    priority: str = "medium"  # "low" | "medium" | "high"
    category: str = "general"
    frequency: str = "daily"  # "daily" | "weekly"
    preferred_start: int | None = None  # minutes since midnight; pins the task to this time
    last_completed: date | None = None

    def priority_value(self) -> int:
        """Return a numeric rank for the priority (low=1, medium=2, high=3)."""
        return PRIORITY_RANK.get(self.priority.lower(), 0)

    def mark_complete(self, on: date) -> None:
        """Record that this task was completed on the given date."""
        self.last_completed = on

    def is_complete(self, today: date) -> bool:
        """Return True if this task was completed on the given date."""
        return self.last_completed == today

    def is_due_today(self, today: date) -> bool:
        """Return True if the task is due on the given date, based on frequency and last_completed."""
        if self.last_completed is None:
            return True
        days_since = (today - self.last_completed).days
        if self.frequency == "weekly":
            return days_since >= 7
        return days_since >= 1


@dataclass(eq=False)
class Pet:
    """A pet and the care tasks it needs."""

    name: str
    species: str
    age: int = 0
    tasks: list[Task] = field(default_factory=list)

    def add_task(self, task: Task) -> None:
        """Add a care task for this pet."""
        self.tasks.append(task)

    def remove_task(self, task: Task) -> None:
        """Remove the given task from this pet."""
        self.tasks.remove(task)

    def edit_task(self, task: Task, **changes) -> None:
        """Update fields (e.g. duration_minutes, priority) on the given task."""
        if task not in self.tasks:
            raise ValueError(f"{task.description!r} is not one of {self.name}'s tasks")
        for name, value in changes.items():
            if not hasattr(task, name):
                raise AttributeError(f"Task has no field {name!r}")
            setattr(task, name, value)

    def get_due_tasks(self, today: date) -> list[Task]:
        """Return tasks that are due on the given date."""
        return [task for task in self.tasks if task.is_due_today(today)]


@dataclass(eq=False)
class Owner:
    """A pet owner, their daily constraints, and their pets."""

    name: str
    available_minutes: int = 120
    day_start: int = 8 * 60  # minutes since midnight
    preferred_categories: list[str] = field(default_factory=list)  # tie-breaker when sorting
    pets: list[Pet] = field(default_factory=list)

    def add_pet(self, pet: Pet) -> None:
        """Add a pet to this owner."""
        self.pets.append(pet)

    def remove_pet(self, pet: Pet) -> None:
        """Remove the given pet from this owner."""
        self.pets.remove(pet)

    def get_all_tasks(self) -> list[tuple[Pet, Task]]:
        """Return every (pet, task) pair across all of this owner's pets."""
        return [(pet, task) for pet in self.pets for task in pet.tasks]


class Scheduler:
    """Builds and explains a daily care plan for an owner's pets."""

    def __init__(self, owner: Owner) -> None:
        self.owner = owner
        self.plan: list[tuple[int, Pet, Task, str]] = []  # (start minute, pet, task, reason)
        self.skipped: list[tuple[Pet, Task]] = []

    def generate_plan(self, today: date) -> list[tuple[int, Pet, Task, str]]:
        """Choose, order, and time-slot the tasks due today within the owner's constraints.

        Reads tasks from self.owner.get_all_tasks() (never from a single pet) so
        every pet is covered, then keeps only those where is_due_today(today).

        Tasks with a preferred_start are pinned to that time; the rest fill the
        open gaps starting at owner.day_start.
        """
        self.plan = []
        self.skipped = []

        due = [(pet, task) for pet, task in self.owner.get_all_tasks() if task.is_due_today(today)]
        selected = self.filter_by_time(self.sort_tasks(due))

        pinned = [(pet, task) for pet, task in selected if task.preferred_start is not None]
        flexible = [(pet, task) for pet, task in selected if task.preferred_start is None]

        busy = []  # (start, end) of pinned tasks, which flexible tasks must avoid
        for pet, task in pinned:
            start = task.preferred_start
            busy.append((start, start + task.duration_minutes))
            self.plan.append((start, pet, task, f"pinned to {format_time(start)}, {self._reason(task)}"))

        cursor = self.owner.day_start
        for pet, task in flexible:
            start = self._next_open_slot(cursor, task.duration_minutes, busy)
            self.plan.append((start, pet, task, self._reason(task)))
            cursor = start + task.duration_minutes

        self.plan.sort(key=lambda entry: entry[0])
        return self.plan

    def sort_tasks(self, tasks: list[tuple[Pet, Task]]) -> list[tuple[Pet, Task]]:
        """Return tasks ordered by priority, breaking ties with owner.preferred_categories."""
        preferred = self.owner.preferred_categories

        def key(pair: tuple[Pet, Task]) -> tuple[int, int]:
            task = pair[1]
            category_rank = preferred.index(task.category) if task.category in preferred else len(preferred)
            return (-task.priority_value(), category_rank)

        return sorted(tasks, key=key)

    def filter_by_time(self, tasks: list[tuple[Pet, Task]]) -> list[tuple[Pet, Task]]:
        """Keep tasks that fit in the available time; record the rest in self.skipped.

        Keeps checking after a task doesn't fit, so shorter tasks later in the
        list can still use the remaining time.
        """
        remaining = self.owner.available_minutes
        kept = []
        for pet, task in tasks:
            if task.duration_minutes <= remaining:
                kept.append((pet, task))
                remaining -= task.duration_minutes
            else:
                self.skipped.append((pet, task))
        return kept

    def detect_conflicts(self) -> list[str]:
        """Return warnings for pinned tasks in the current plan whose times overlap."""
        warnings = []
        for i, (start_a, pet_a, task_a, _) in enumerate(self.plan):
            end_a = start_a + task_a.duration_minutes
            for start_b, pet_b, task_b, _ in self.plan[i + 1:]:
                if start_b < end_a and start_a < start_b + task_b.duration_minutes:
                    warnings.append(
                        f"{pet_a.name}: {task_a.description} ({format_time(start_a)}) overlaps "
                        f"{pet_b.name}: {task_b.description} ({format_time(start_b)})"
                    )
        return warnings

    def explain_plan(self) -> str:
        """Return a human-readable explanation of why each task was chosen or skipped."""
        if not self.plan and not self.skipped:
            return f"No tasks are due for {self.owner.name}'s pets."

        used = sum(task.duration_minutes for _, _, task, _ in self.plan)
        lines = [f"Daily plan for {self.owner.name} ({used} of {self.owner.available_minutes} min used):"]
        for start, pet, task, reason in self.plan:
            end = start + task.duration_minutes
            lines.append(
                f"  {format_time(start)}-{format_time(end)}  {pet.name}: {task.description} "
                f"({task.duration_minutes} min) - {reason}"
            )

        if self.skipped:
            lines.append("Skipped (not enough time left):")
            for pet, task in self.skipped:
                lines.append(f"  {pet.name}: {task.description} ({task.duration_minutes} min, {task.priority} priority)")

        conflicts = self.detect_conflicts()
        if conflicts:
            lines.append("Conflicts:")
            lines.extend(f"  {warning}" for warning in conflicts)

        return "\n".join(lines)

    def _reason(self, task: Task) -> str:
        """Describe why a task was placed where it was."""
        reason = f"{task.priority} priority"
        if task.category in self.owner.preferred_categories:
            reason += f", preferred category ({task.category})"
        return reason

    @staticmethod
    def _next_open_slot(start: int, duration: int, busy: list[tuple[int, int]]) -> int:
        """Return the earliest time at or after start where duration fits between busy blocks."""
        moved = True
        while moved:
            moved = False
            for busy_start, busy_end in busy:
                if start < busy_end and busy_start < start + duration:
                    start = busy_end
                    moved = True
        return start
