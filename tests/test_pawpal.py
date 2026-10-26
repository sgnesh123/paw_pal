from datetime import date

from pawpal_system import Pet, Task


def test_mark_complete_changes_task_status():
    today = date(2026, 10, 26)
    task = Task("Morning walk", 30, "high", "walk")
    assert not task.is_complete(today)

    task.mark_complete(today)

    assert task.is_complete(today)
    assert task.last_completed == today


def test_add_task_increases_pet_task_count():
    pet = Pet("Mochi", "dog")
    assert len(pet.tasks) == 0

    pet.add_task(Task("Breakfast", 10, "high", "feeding"))

    assert len(pet.tasks) == 1
