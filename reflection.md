# PawPal+ Project Reflection

## 1. System Design

**Core Actions:**
1. **Add/Manage Pet Information**: Users should be able to enter basic information about their pet (name, species) and link it to an owner profile with preferences and available time slots.
2. **Add/Edit Tasks**: Users should be able to create and modify pet care tasks (e.g., walks, feeding, medications, enrichment, grooming) with attributes like duration, priority level, and task type.
3. **Generate Daily Schedule**: Users should be able to request a daily plan that intelligently schedules tasks based on constraints (available time, priority levels, owner preferences) and displays the plan with explanations for why tasks were scheduled at specific times.

**a. Initial design**

The initial UML design includes four main classes:

1. **Owner**: Represents the pet owner with their availability constraints and preferences. Responsibilities include:
   - Storing owner name and available time window (start/end hours)
   - Managing owner preferences (e.g., preferred walk times)
   - Providing access to availability information

2. **Pet**: Represents a pet with basic information. Responsibilities include:
   - Storing pet name and species
   - Maintaining a reference to the owner
   - Providing pet information when needed

3. **Task**: Represents individual pet care tasks using a dataclass. Responsibilities include:
   - Storing task details (title, duration, priority, type)
   - Converting priority strings to numeric values for sorting
   - Providing task duration information

4. **Scheduler**: The core scheduling engine that generates daily plans. Responsibilities include:
   - Managing a collection of tasks
   - Maintaining references to owner and pet
   - Generating daily schedules based on constraints (time availability, priority)
   - Explaining the reasoning behind the generated schedule
   - Adding and removing tasks

The relationships are: Owner owns one or more Pets, Pet belongs to one Owner, and Scheduler uses Owner and Pet information to manage and schedule Tasks.

**b. Design changes**

- Did your design change during implementation?
- If yes, describe at least one change and why you made it.

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
