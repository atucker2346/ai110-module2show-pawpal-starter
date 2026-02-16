"""
Tests for PawPal+ system.

Tests cover:
- Task completion and addition
- Sorting correctness
- Recurring task logic
- Conflict detection
- Edge cases (empty schedules, pets with no tasks, etc.)
"""

import pytest
from pawpal_system import Owner, Pet, Task, Scheduler


def test_task_completion():
    """Verify that calling mark_complete() actually changes the task's status."""
    # Create a task
    task = Task(
        title="Morning walk",
        duration_minutes=30,
        priority="high",
        task_type="walk"
    )
    
    # Initially, task should not be completed
    assert task.completed == False
    
    # Mark task as complete
    task.mark_complete()
    
    # Task should now be completed
    assert task.completed == True
    
    # Mark task as incomplete
    task.mark_incomplete()
    
    # Task should now be incomplete again
    assert task.completed == False


def test_task_addition():
    """Verify that adding a task to a Pet increases that pet's task count."""
    # Create owner and pet
    owner = Owner(name="Jordan")
    pet = Pet(name="Mochi", species="dog", owner=owner)
    
    # Initially, pet should have no tasks
    assert len(pet.get_tasks()) == 0
    
    # Create a task
    task = Task(
        title="Morning walk",
        duration_minutes=30,
        priority="high",
        task_type="walk"
    )
    
    # Add task to pet
    pet.add_task(task)
    
    # Pet should now have one task
    assert len(pet.get_tasks()) == 1
    assert pet.get_tasks()[0].title == "Morning walk"
    
    # Add another task
    task2 = Task(
        title="Breakfast feeding",
        duration_minutes=15,
        priority="high",
        task_type="feeding"
    )
    pet.add_task(task2)
    
    # Pet should now have two tasks
    assert len(pet.get_tasks()) == 2


def test_owner_get_all_tasks():
    """Test that Owner can retrieve all tasks from all pets."""
    owner = Owner(name="Jordan")
    pet1 = Pet(name="Mochi", species="dog", owner=owner)
    pet2 = Pet(name="Whiskers", species="cat", owner=owner)
    
    owner.add_pet(pet1)
    owner.add_pet(pet2)
    
    task1 = Task(title="Walk", duration_minutes=30, priority="high", task_type="walk")
    task2 = Task(title="Feed", duration_minutes=15, priority="high", task_type="feeding")
    
    pet1.add_task(task1)
    pet2.add_task(task2)
    
    all_tasks = owner.get_all_tasks()
    assert len(all_tasks) == 2
    assert task1 in all_tasks
    assert task2 in all_tasks


def test_scheduler_generates_schedule():
    """Test that scheduler can generate a schedule from owner's pets."""
    owner = Owner(name="Jordan", available_start_hour=8, available_end_hour=20)
    pet = Pet(name="Mochi", species="dog", owner=owner)
    owner.add_pet(pet)
    
    task = Task(title="Morning walk", duration_minutes=30, priority="high", task_type="walk")
    pet.add_task(task)
    
    scheduler = Scheduler(owner=owner)
    schedule = scheduler.generate_schedule()
    
    assert len(schedule) == 1
    assert schedule[0]["task"] == "Morning walk"
    assert schedule[0]["pet"] == "Mochi"


def test_sorting_correctness():
    """Verify tasks are returned in chronological order when sorted by time."""
    owner = Owner(name="Jordan")
    scheduler = Scheduler(owner=owner)
    
    # Create tasks with different scheduled times (out of order)
    task1 = Task(title="Evening task", duration_minutes=30, priority="high", task_type="walk")
    task1.scheduled_time = 18  # 6 PM
    
    task2 = Task(title="Morning task", duration_minutes=15, priority="high", task_type="feeding")
    task2.scheduled_time = 8  # 8 AM
    
    task3 = Task(title="Afternoon task", duration_minutes=20, priority="medium", task_type="enrichment")
    task3.scheduled_time = 14  # 2 PM
    
    task4 = Task(title="Unscheduled task", duration_minutes=10, priority="low", task_type="grooming")
    # task4 has no scheduled_time (None)
    
    tasks = [task1, task2, task3, task4]
    sorted_tasks = scheduler.sort_by_time(tasks)
    
    # Verify chronological order
    assert sorted_tasks[0].scheduled_time == 8  # Morning first
    assert sorted_tasks[0].title == "Morning task"
    assert sorted_tasks[1].scheduled_time == 14  # Afternoon second
    assert sorted_tasks[1].title == "Afternoon task"
    assert sorted_tasks[2].scheduled_time == 18  # Evening third
    assert sorted_tasks[2].title == "Evening task"
    assert sorted_tasks[3].scheduled_time is None  # Unscheduled last
    assert sorted_tasks[3].title == "Unscheduled task"


def test_recurrence_logic():
    """Confirm that marking a daily task complete creates a new task for the following day."""
    owner = Owner(name="Jordan")
    pet = Pet(name="Mochi", species="dog", owner=owner)
    owner.add_pet(pet)
    
    # Create a daily recurring task
    daily_task = Task(
        title="Daily medication",
        duration_minutes=5,
        priority="high",
        task_type="meds",
        frequency="daily"
    )
    
    pet.add_task(daily_task)
    initial_task_count = len(pet.get_tasks())
    assert initial_task_count == 1
    
    # Mark the task as complete
    pet.mark_task_complete("Daily medication")
    
    # Should now have 2 tasks: one completed, one new incomplete
    assert len(pet.get_tasks()) == 2
    
    # Find the completed and new tasks
    completed_tasks = [t for t in pet.get_tasks() if t.completed]
    incomplete_tasks = [t for t in pet.get_tasks() if not t.completed]
    
    assert len(completed_tasks) == 1
    assert len(incomplete_tasks) == 1
    assert completed_tasks[0].title == "Daily medication"
    assert incomplete_tasks[0].title == "Daily medication"
    assert incomplete_tasks[0].frequency == "daily"
    assert incomplete_tasks[0].completed == False


def test_recurrence_non_recurring_task():
    """Verify that marking a non-recurring task complete does NOT create a new task."""
    owner = Owner(name="Jordan")
    pet = Pet(name="Mochi", species="dog", owner=owner)
    owner.add_pet(pet)
    
    # Create a non-recurring task
    one_time_task = Task(
        title="One-time grooming",
        duration_minutes=30,
        priority="medium",
        task_type="grooming"
        # No frequency set
    )
    
    pet.add_task(one_time_task)
    assert len(pet.get_tasks()) == 1
    
    # Mark the task as complete
    pet.mark_task_complete("One-time grooming")
    
    # Should still have only 1 task (completed)
    assert len(pet.get_tasks()) == 1
    assert pet.get_tasks()[0].completed == True


def test_conflict_detection_duplicate_times():
    """Verify that the Scheduler flags duplicate times."""
    owner = Owner(name="Jordan")
    scheduler = Scheduler(owner=owner)
    
    # Create a schedule with two tasks at the same time
    schedule = [
        {
            "task": "Morning walk",
            "pet": "Mochi",
            "type": "walk",
            "duration": 30,
            "priority": "high",
            "scheduled_time": "10:00",
            "scheduled_hour": 10
        },
        {
            "task": "Morning feeding",
            "pet": "Whiskers",
            "type": "feeding",
            "duration": 15,
            "priority": "high",
            "scheduled_time": "10:00",  # Same time!
            "scheduled_hour": 10
        }
    ]
    
    conflicts = scheduler.detect_conflicts(schedule)
    
    # Should detect conflict
    assert len(conflicts) > 0
    assert "10:00" in conflicts[0]
    assert "Conflict" in conflicts[0] or "conflict" in conflicts[0].lower()


def test_conflict_detection_overlapping_durations():
    """Verify that overlapping task durations are detected."""
    owner = Owner(name="Jordan")
    scheduler = Scheduler(owner=owner)
    
    # Create a schedule with overlapping durations
    # Task 1: 10:00-10:30 (30 min)
    # Task 2: 10:15-10:45 (30 min) - overlaps!
    schedule = [
        {
            "task": "Long walk",
            "pet": "Mochi",
            "type": "walk",
            "duration": 30,
            "priority": "high",
            "scheduled_time": "10:00",
            "scheduled_hour": 10
        },
        {
            "task": "Playtime",
            "pet": "Whiskers",
            "type": "enrichment",
            "duration": 30,
            "priority": "medium",
            "scheduled_time": "10:15",  # Starts during first task
            "scheduled_hour": 10
        }
    ]
    
    conflicts = scheduler.detect_conflicts(schedule)
    
    # Should detect overlap
    assert len(conflicts) > 0
    assert "Overlap" in conflicts[0] or "overlap" in conflicts[0].lower()


def test_conflict_detection_no_conflicts():
    """Verify that no conflicts are detected when tasks don't overlap."""
    owner = Owner(name="Jordan")
    scheduler = Scheduler(owner=owner)
    
    # Create a schedule with non-overlapping tasks
    schedule = [
        {
            "task": "Morning walk",
            "pet": "Mochi",
            "type": "walk",
            "duration": 30,
            "priority": "high",
            "scheduled_time": "08:00",
            "scheduled_hour": 8
        },
        {
            "task": "Afternoon feeding",
            "pet": "Whiskers",
            "type": "feeding",
            "duration": 15,
            "priority": "medium",
            "scheduled_time": "14:00",  # Different time, no overlap
            "scheduled_hour": 14
        }
    ]
    
    conflicts = scheduler.detect_conflicts(schedule)
    
    # Should have no conflicts
    assert len(conflicts) == 0


def test_edge_case_pet_with_no_tasks():
    """Test edge case: pet with no tasks should generate empty schedule."""
    owner = Owner(name="Jordan", available_start_hour=8, available_end_hour=20)
    pet = Pet(name="Mochi", species="dog", owner=owner)
    owner.add_pet(pet)
    
    scheduler = Scheduler(owner=owner)
    schedule = scheduler.generate_schedule()
    
    # Should return empty schedule
    assert len(schedule) == 0
    assert schedule == []


def test_edge_case_all_tasks_completed():
    """Test edge case: all tasks completed should generate empty schedule."""
    owner = Owner(name="Jordan", available_start_hour=8, available_end_hour=20)
    pet = Pet(name="Mochi", species="dog", owner=owner)
    owner.add_pet(pet)
    
    task1 = Task(title="Morning walk", duration_minutes=30, priority="high", task_type="walk")
    task1.mark_complete()
    task2 = Task(title="Feeding", duration_minutes=15, priority="high", task_type="feeding")
    task2.mark_complete()
    
    pet.add_task(task1)
    pet.add_task(task2)
    
    scheduler = Scheduler(owner=owner)
    schedule = scheduler.generate_schedule()
    
    # Should return empty schedule (completed tasks are filtered out)
    assert len(schedule) == 0


def test_edge_case_tasks_exceed_available_time():
    """Test edge case: tasks that exceed available time window."""
    owner = Owner(name="Jordan", available_start_hour=8, available_end_hour=10)  # Only 2 hours
    pet = Pet(name="Mochi", species="dog", owner=owner)
    owner.add_pet(pet)
    
    # Add tasks that total more than 2 hours
    task1 = Task(title="Long walk", duration_minutes=90, priority="high", task_type="walk")
    task2 = Task(title="Feeding", duration_minutes=30, priority="high", task_type="feeding")
    task3 = Task(title="Playtime", duration_minutes=30, priority="medium", task_type="enrichment")
    
    pet.add_task(task1)  # 90 min
    pet.add_task(task2)  # 30 min
    pet.add_task(task3)  # 30 min
    # Total: 150 min, but only 120 min available
    
    scheduler = Scheduler(owner=owner)
    schedule = scheduler.generate_schedule()
    
    # Should schedule as many as fit (priority-based)
    assert len(schedule) > 0
    # First task should be highest priority
    assert schedule[0]["priority"] == "high"
    
    # Verify total scheduled time doesn't exceed available window
    total_scheduled_minutes = sum(item["duration"] for item in schedule)
    available_minutes = (owner.available_end_hour - owner.available_start_hour) * 60
    assert total_scheduled_minutes <= available_minutes


def test_filter_tasks_by_completion():
    """Test filtering tasks by completion status."""
    owner = Owner(name="Jordan")
    pet = Pet(name="Mochi", species="dog", owner=owner)
    owner.add_pet(pet)
    
    task1 = Task(title="Task 1", duration_minutes=30, priority="high", task_type="walk")
    task2 = Task(title="Task 2", duration_minutes=15, priority="medium", task_type="feeding")
    task2.mark_complete()
    task3 = Task(title="Task 3", duration_minutes=20, priority="low", task_type="enrichment")
    
    pet.add_task(task1)
    pet.add_task(task2)
    pet.add_task(task3)
    
    scheduler = Scheduler(owner=owner)
    all_tasks = owner.get_all_tasks()
    
    # Filter incomplete tasks
    incomplete = scheduler.filter_tasks(all_tasks, completed=False)
    assert len(incomplete) == 2
    assert task1 in incomplete
    assert task3 in incomplete
    assert task2 not in incomplete
    
    # Filter completed tasks
    completed = scheduler.filter_tasks(all_tasks, completed=True)
    assert len(completed) == 1
    assert task2 in completed


def test_filter_tasks_by_pet_name():
    """Test filtering tasks by pet name."""
    owner = Owner(name="Jordan")
    pet1 = Pet(name="Mochi", species="dog", owner=owner)
    pet2 = Pet(name="Whiskers", species="cat", owner=owner)
    owner.add_pet(pet1)
    owner.add_pet(pet2)
    
    task1 = Task(title="Mochi's walk", duration_minutes=30, priority="high", task_type="walk")
    task2 = Task(title="Whiskers' feeding", duration_minutes=15, priority="medium", task_type="feeding")
    
    pet1.add_task(task1)
    pet2.add_task(task2)
    
    scheduler = Scheduler(owner=owner)
    all_tasks = owner.get_all_tasks()
    
    # Filter by pet name (case-insensitive)
    mochi_tasks = scheduler.filter_tasks(all_tasks, pet_name="Mochi")
    assert len(mochi_tasks) == 1
    assert task1 in mochi_tasks
    
    whiskers_tasks = scheduler.filter_tasks(all_tasks, pet_name="whiskers")  # lowercase
    assert len(whiskers_tasks) == 1
    assert task2 in whiskers_tasks
