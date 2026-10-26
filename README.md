# PawPal+ (Module 2 Project)

You are building **PawPal+**, a Streamlit app that helps pet owners track and manage "care tasks" for their pet.

## Scenario

A busy pet owner needs help staying consistent with pet care. They want an assistant that can:

- Track pet care tasks (walks, feeding, meds, enrichment, grooming, etc.)
- Consider constraints (time available, priority, owner preferences)
- Produce a daily plan and explain why it chose that plan

Your job is to design the system first (UML), then implement the logic in Python, then connect it to the Streamlit UI.

## What you will build

Your final app should:

- Let a user enter basic owner + pet info
- Let a user add/edit tasks (duration + priority at minimum)
- Generate a daily schedule/plan based on constraints and priorities
- Display the plan clearly (and ideally explain the reasoning)
- Include tests for the most important scheduling behaviors

## Getting started

### Setup

```bash
python -m venv .venv
source .venv/bin/activate  # Windows: .venv\Scripts\activate
pip install -r requirements.txt
```

### Suggested workflow

1. Read the scenario carefully and identify requirements and edge cases.
2. Draft a UML diagram (classes, attributes, methods, relationships).
3. Convert UML into Python class stubs (no logic yet).
4. Implement scheduling logic in small increments.
5. Add tests to verify key behaviors.
6. Connect your logic to the Streamlit UI in `app.py`.
7. Refine UML so it matches what you actually built.

## 🏗️ Implementation Summary

The core logic lives in `pawpal_system.py` and is built from four classes (see `diagrams/uml_draft.mmd`):

- **`Task`**: one care activity, with its description, duration, priority, category, frequency (daily/weekly), an optional 
pinned start time, and the date it was last completed. It knows whether it's done today and whether it's due again.
- **`Pet`**: a pet's details plus its own list of tasks, with methods to add, edit, and remove them.
- **`Owner`**: the owner's daily constraints (minutes available, day start time, preferred categories) and their pets. `get_all_tasks()` returns every `(pet, task)` pair across all pets.
- **`Scheduler`**: the planner. `generate_plan(today)` reads tasks from `Owner.get_all_tasks()`, keeps the ones due today, 
sorts them by priority (ties go to preferred categories), and drops any that don't fit the time budget. It then places 
pinned tasks at their set times and fits the rest into the open gaps. `detect_conflicts()` flags overlapping pinned tasks, 
and `explain_plan()` describes why each task was scheduled or skipped.

Times are stored as minutes since midnight and converted to `HH:MM` for display with `to_minutes()` and `format_time()`. 
Run `python main.py` to see a sample schedule for two pets.

## 🖥️ Sample Output

Paste a sample of your app's CLI or Streamlit output here so a reader can see what a generated plan looks like:

```
========================================================================
              Today's Schedule - Monday, October 26, 2026               
========================================================================
Owner: Jordan    Pets: Mochi (dog), Luna (cat)
Time used: 90 of 120 min
------------------------------------------------------------------------
Time          Pet     Task                 Why
------------------------------------------------------------------------
07:30-07:40   Mochi   Breakfast            pinned to 07:30, high priority, preferred category (feeding)
07:40-08:00   Mochi   Fetch in the yard    medium priority
08:00-08:30   Mochi   Morning walk         pinned to 08:00, high priority
08:30-08:40   Luna    Litter box           medium priority
08:40-08:55   Luna    Brushing             low priority
09:00-09:05   Luna    Thyroid pill         pinned to 09:00, high priority, preferred category (meds)
------------------------------------------------------------------------
Skipped (not enough time left today):
  - Luna: Laser toy play (45 min, low priority)
========================================================================
```

## 🧪 Testing PawPal+

```bash
# Run the full test suite:
pytest

# Run with coverage:
pytest --cov
```

Sample test output:

```
# Paste your pytest output here
```

## 📐 Smarter Scheduling

> Fill in once you've implemented scheduling logic.

| Feature | Method(s) | Notes |
|---------|-----------|-------|
| Task sorting | | e.g., by priority, duration |
| Filtering | | e.g., skip tasks if time runs out |
| Conflict handling | | e.g., overlapping time slots |
| Recurring tasks | | e.g., daily vs. weekly |

## 📸 Demo Walkthrough

Describe your app in numbered steps so a reader can follow along without watching a video:

1. <!-- Describe this step -->
2. <!-- Describe this step -->
3. <!-- Describe this step -->
4. <!-- Describe this step -->
5. <!-- Add more steps as needed -->

**Screenshot or video** *(optional)*: <!-- Insert a screenshot or link to a demo video here -->
