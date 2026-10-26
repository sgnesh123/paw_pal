"""PawPal+ core system: Owner, Pet, Task, and Scheduler.

Class skeletons generated from diagrams/uml_draft.mmd. Method bodies are stubs.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from datetime import date


@dataclass
class Task:
    """A single pet care task (walk, feeding, meds, enrichment, grooming, ...)."""

    title: str
    duration_minutes: int
    priority: str = "medium"  # "low" | "medium" | "high"
    category: str = "general"
    frequency: str = "daily"  # "daily" | "weekly"
    preferred_time: str | None = None  # "HH:MM", optional
    completed: bool = False

    def priority_value(self) -> int:
        """Return a numeric rank for the priority (low=1, medium=2, high=3)."""
        pass

    def mark_complete(self) -> None:
        """Mark this task as done."""
        pass

    def is_due_today(self, today: date) -> bool:
        """Return True if this task should be scheduled on the given date."""
        pass


@dataclass
class Pet:
    """A pet and the care tasks it needs."""

    name: str
    species: str
    age: int = 0
    tasks: list[Task] = field(default_factory=list)

    def add_task(self, task: Task) -> None:
        """Add a care task for this pet."""
        pass

    def remove_task(self, title: str) -> None:
        """Remove the task with the given title."""
        pass

    def edit_task(self, title: str, **changes) -> None:
        """Update fields (e.g. duration_minutes, priority) on the task with the given title."""
        pass

    def get_pending_tasks(self) -> list[Task]:
        """Return tasks that are not yet completed."""
        pass


@dataclass
class Owner:
    """A pet owner, their daily constraints, and their pets."""

    name: str
    available_minutes: int = 120
    day_start_time: str = "08:00"  # "HH:MM"
    preferences: list[str] = field(default_factory=list)
    pets: list[Pet] = field(default_factory=list)

    def add_pet(self, pet: Pet) -> None:
        """Add a pet to this owner."""
        pass

    def remove_pet(self, name: str) -> None:
        """Remove the pet with the given name."""
        pass

    def get_all_tasks(self) -> list[Task]:
        """Return every task across all of this owner's pets."""
        pass


class Scheduler:
    """Builds and explains a daily care plan for an owner's pets."""

    def __init__(self, owner: Owner) -> None:
        self.owner = owner
        self.plan: list[tuple[str, Task, str]] = []  # (start_time, task, reason)
        self.skipped: list[Task] = []

    def generate_plan(self) -> list[tuple[str, Task, str]]:
        """Choose, order, and time-slot today's tasks within the owner's constraints."""
        pass

    def sort_tasks(self, tasks: list[Task]) -> list[Task]:
        """Return tasks ordered by priority (and any tie-break rules)."""
        pass

    def filter_by_time(self, tasks: list[Task]) -> list[Task]:
        """Keep tasks that fit in the available time; record the rest in self.skipped."""
        pass

    def detect_conflicts(self) -> list[str]:
        """Return warnings for overlapping or clashing tasks in the current plan."""
        pass

    def explain_plan(self) -> str:
        """Return a human-readable explanation of why each task was chosen or skipped."""
        pass
