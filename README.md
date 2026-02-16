# PawPal+ (Module 2 Project)

You are building **PawPal+**, a Streamlit app that helps a pet owner plan care tasks for their pet.

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

## Smarter Scheduling

PawPal+ includes intelligent algorithms to make scheduling more efficient:

- **Sorting**: Tasks can be sorted by scheduled time, priority, or duration
- **Filtering**: Filter tasks by completion status (complete/incomplete) or by pet name
- **Recurring Tasks**: Automatically create new task instances when daily or weekly tasks are marked complete
- **Conflict Detection**: Identifies scheduling conflicts where tasks overlap in time and provides warnings
- **Priority-Based Scheduling**: High-priority tasks are scheduled first, with shorter tasks prioritized within the same priority level

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

## Testing PawPal+

The PawPal+ system includes a comprehensive test suite to verify core functionality and edge cases.

### Running Tests

To run the test suite:

```bash
python -m pytest tests/test_pawpal.py -v
```

### Test Coverage

The test suite covers:

**Core Functionality:**
- Task completion and status changes
- Task addition to pets
- Owner task aggregation across multiple pets
- Schedule generation with priority-based ordering

**Sorting and Filtering:**
- Tasks sorted correctly by scheduled time (chronological order)
- Filtering by completion status (complete/incomplete)
- Filtering by pet name (case-insensitive)

**Recurring Tasks:**
- Daily tasks automatically create new instances when marked complete
- Non-recurring tasks do not create new instances
- Recurring task properties are preserved in new instances

**Conflict Detection:**
- Detects tasks scheduled at the exact same time
- Identifies overlapping task durations
- Returns appropriate warnings without crashing
- Correctly identifies when no conflicts exist

**Edge Cases:**
- Pet with no tasks generates empty schedule
- All completed tasks are filtered out from schedule
- Tasks exceeding available time window are handled correctly
- Empty schedules return appropriate results

### Confidence Level

**⭐⭐⭐⭐⭐ (5/5 stars)**

The test suite provides high confidence in system reliability:
- All core behaviors are tested with both happy paths and edge cases
- Sorting, filtering, and conflict detection algorithms are thoroughly verified
- Recurring task logic is validated to ensure automatic task creation works correctly
- Edge cases ensure the system handles boundary conditions gracefully
