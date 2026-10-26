# PawPal+ Project Reflection

## 1. System Design

**a. Initial design** 

- Briefly describe your initial UML design.
- What classes did you include, and what responsibilities did you assign to each?

My initial UML design has four classes: `Owner`, `Pet`, `Task`, and `Scheduler`. An `Owner` has one or more pets, 
and each `Pet` keeps its own list of tasks. The `Scheduler` takes an `Owner` and reads that data to build a plan 
without changing it. `Task` represents one unit of pet care, such as a walk, feeding, or medication, and stores 
its title, duration, priority, category, frequency, an optional preferred time, and whether it's done. It can also 
turn its priority into a number for sorting, and check whether it is due on a given day. `Pet` stores basic info
like name, species, and age, and lets you add, edit, and remove its tasks. `Owner` stores the owner's name and the 
constraints that shape the schedule, such as how many minutes they have, when their day starts, and their preferences, 
and it can collect every task across all of their pets. `Scheduler` does the planning: it sorts tasks by priority, 
drops the ones that won't fit in the available time, gives each remaining task a start time, checks for conflicts, 
and explains why each task was included or skipped. I used Python dataclasses for `Owner`, `Pet`, and `Task` because 
they mainly hold data, and I kept the scheduling logic separate in Scheduler so I can change the rules and test them 
without touching how pets and tasks are stored.

**b. Design changes**

- Did your design change during implementation?
- If yes, describe at least one change and why you made it.

Yes, my design changed after I reviewed the first skeleton. The biggest change was determining how tasks relate to pets. 
At first, `Owner.get_all_tasks()` returned a flat list of tasks, so the scheduler couldn't tell which pet a task was for, 
and two pets with a "Feeding" task looked the same. I changed it to return (pet, task) pairs, so the plan can say whose task 
is whose. I also replaced the completed flag with a "last_completed date", because a true/false value can't tell when a 
weekly task is due again. I stored times as "minutes since midnight" instead of "HH:MM" strings to make time math simpler. Finally, I changed tasks and pets to be looked up by the object itself rather than by name, so duplicate names don't cause 
the wrong one to be edited or removed.

---

## 2. Scheduling Logic and Tradeoffs

**a. Constraints and priorities**

- What constraints does your scheduler consider (for example: time, priority, preferences)?
- How did you decide which constraints mattered most?

**b. Tradeoffs**

- Describe one tradeoff your scheduler makes.
- Why is that tradeoff reasonable for this scenario?

---

## 3. AI Collaboration

**a. How you used AI**

- How did you use AI tools during this project (for example: design brainstorming, debugging, refactoring)?
- What kinds of prompts or questions were most helpful?

**b. Judgment and verification**

- Describe one moment where you did not accept an AI suggestion as-is.
- How did you evaluate or verify what the AI suggested?

---

## 4. Testing and Verification

**a. What you tested**

- What behaviors did you test?
- Why were these tests important?

**b. Confidence**

- How confident are you that your scheduler works correctly?
- What edge cases would you test next if you had more time?

---

## 5. Reflection

**a. What went well**

- What part of this project are you most satisfied with?

**b. What you would improve**

- If you had another iteration, what would you improve or redesign?

**c. Key takeaway**

- What is one important thing you learned about designing systems or working with AI on this project?
