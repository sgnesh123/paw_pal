"""Demo script: build a sample owner with two pets and print today's schedule."""

from datetime import date

from pawpal_system import Owner, Pet, Scheduler, Task, format_time, to_minutes


def build_owner() -> Owner:
    """Create a sample owner with two pets and a mix of pinned and flexible tasks."""
    owner = Owner(
        name="Jordan",
        available_minutes=120,
        day_start=to_minutes("07:30"),
        preferred_categories=["meds", "feeding"],
    )

    mochi = Pet(name="Mochi", species="dog", age=3)
    luna = Pet(name="Luna", species="cat", age=5)
    owner.add_pet(mochi)
    owner.add_pet(luna)

    mochi.add_task(Task("Breakfast", 10, "high", "feeding", preferred_start=to_minutes("07:30")))
    mochi.add_task(Task("Morning walk", 30, "high", "walk", preferred_start=to_minutes("08:00")))
    mochi.add_task(Task("Fetch in the yard", 20, "medium", "enrichment"))
    luna.add_task(Task("Thyroid pill", 5, "high", "meds", preferred_start=to_minutes("09:00")))
    luna.add_task(Task("Litter box", 10, "medium", "cleaning"))
    luna.add_task(Task("Brushing", 15, "low", "grooming", frequency="weekly"))
    luna.add_task(Task("Laser toy play", 45, "low", "enrichment"))

    return owner


def print_schedule(scheduler: Scheduler, today: date) -> None:
    """Print the generated plan as a readable table."""
    owner = scheduler.owner
    width = 72
    used = sum(task.duration_minutes for _, _, task, _ in scheduler.plan)
    pets = ", ".join(f"{pet.name} ({pet.species})" for pet in owner.pets)

    print("=" * width)
    print(f"Today's Schedule - {today.strftime('%A, %B %d, %Y')}".center(width))
    print("=" * width)
    print(f"Owner: {owner.name}    Pets: {pets}")
    print(f"Time used: {used} of {owner.available_minutes} min")
    print("-" * width)
    print(f"{'Time':<13} {'Pet':<7} {'Task':<20} Why")
    print("-" * width)
    for start, pet, task, reason in scheduler.plan:
        time_range = f"{format_time(start)}-{format_time(start + task.duration_minutes)}"
        print(f"{time_range:<13} {pet.name:<7} {task.description:<20} {reason}")

    if scheduler.skipped:
        print("-" * width)
        print("Skipped (not enough time left today):")
        for pet, task in scheduler.skipped:
            print(f"  - {pet.name}: {task.description} ({task.duration_minutes} min, {task.priority} priority)")

    conflicts = scheduler.detect_conflicts()
    if conflicts:
        print("-" * width)
        print("Conflicts:")
        for warning in conflicts:
            print(f"  ! {warning}")

    print("=" * width)


def main() -> None:
    today = date.today()
    scheduler = Scheduler(build_owner())
    scheduler.generate_plan(today)
    print_schedule(scheduler, today)


if __name__ == "__main__":
    main()
