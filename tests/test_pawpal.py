"""
Tests for PawPal+ system.

Tests cover task completion and task addition functionality.
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
