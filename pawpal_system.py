"""PawPal+ core system: Owner, Pet, Task, and Scheduler.

Class skeletons generated from diagrams/uml_draft.mmd. Method bodies are stubs.
Times are stored as minutes since midnight (e.g. 8:00 AM -> 480).
"""

from __future__ import annotations

from dataclasses import dataclass, field
from datetime import date


def to_minutes(hhmm: str) -> int:
    """Convert an "HH:MM" string to minutes since midnight."""
    pass


def format_time(minutes: int) -> str:
    """Convert minutes since midnight to an "HH:MM" string."""
    pass


# eq=False keeps identity-based equality, so lookups and removals match the
# exact object rather than any task/pet with the same field values.
@dataclass(eq=False)
class Task:
    """A single pet care task (walk, feeding, meds, enrichment, grooming, ...)."""

    title: str
    duration_minutes: int
    priority: str = "medium"  # "low" | "medium" | "high"
    category: str = "general"
    frequency: str = "daily"  # "daily" | "weekly"
    preferred_start: int | None = None  # minutes since midnight; pins the task to this time
    last_completed: date | None = None

    def priority_value(self) -> int:
        """Return a numeric rank for the priority (low=1, medium=2, high=3)."""
        pass

    def mark_complete(self, on: date) -> None:
        """Record that this task was completed on the given date."""
        pass

    def is_due_today(self, today: date) -> bool:
        """Return True if the task is due on the given date, based on frequency and last_completed."""
        pass


@dataclass(eq=False)
class Pet:
    """A pet and the care tasks it needs."""

    name: str
    species: str
    age: int = 0
    tasks: list[Task] = field(default_factory=list)

    def add_task(self, task: Task) -> None:
        """Add a care task for this pet."""
        pass

    def remove_task(self, task: Task) -> None:
        """Remove the given task from this pet."""
        pass

    def edit_task(self, task: Task, **changes) -> None:
        """Update fields (e.g. duration_minutes, priority) on the given task."""
        pass

    def get_due_tasks(self, today: date) -> list[Task]:
        """Return tasks that are due on the given date."""
        pass


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
        pass

    def remove_pet(self, pet: Pet) -> None:
        """Remove the given pet from this owner."""
        pass

    def get_all_tasks(self) -> list[tuple[Pet, Task]]:
        """Return every (pet, task) pair across all of this owner's pets."""
        pass


class Scheduler:
    """Builds and explains a daily care plan for an owner's pets."""

    def __init__(self, owner: Owner) -> None:
        self.owner = owner
        self.plan: list[tuple[int, Pet, Task, str]] = []  # (start minute, pet, task, reason)
        self.skipped: list[tuple[Pet, Task]] = []

    def generate_plan(self, today: date) -> list[tuple[int, Pet, Task, str]]:
        """Choose, order, and time-slot the tasks due today within the owner's constraints.

        Tasks with a preferred_start are pinned to that time; the rest fill the
        open gaps starting at owner.day_start.
        """
        self.plan = []
        self.skipped = []
        pass

    def sort_tasks(self, tasks: list[tuple[Pet, Task]]) -> list[tuple[Pet, Task]]:
        """Return tasks ordered by priority, breaking ties with owner.preferred_categories."""
        pass

    def filter_by_time(self, tasks: list[tuple[Pet, Task]]) -> list[tuple[Pet, Task]]:
        """Keep tasks that fit in the available time; record the rest in self.skipped.

        Keeps checking after a task doesn't fit, so shorter tasks later in the
        list can still use the remaining time.
        """
        pass

    def detect_conflicts(self) -> list[str]:
        """Return warnings for pinned tasks in the current plan whose times overlap."""
        pass

    def explain_plan(self) -> str:
        """Return a human-readable explanation of why each task was chosen or skipped."""
        pass
