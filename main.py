"""
Demo script for PawPal+ system.

This script demonstrates the core functionality including:
- Sorting tasks by time
- Filtering tasks by completion status and pet name
- Recurring task automation
- Conflict detection
"""

from pawpal_system import Owner, Pet, Task, Scheduler


def main():
    """Main demo function."""
    # Create an owner
    owner = Owner(
        name="Jordan",
        available_start_hour=8,
        available_end_hour=20
    )
    
    # Create pets
    pet1 = Pet(name="Mochi", species="dog", owner=owner)
    pet2 = Pet(name="Whiskers", species="cat", owner=owner)
    
    # Add pets to owner
    owner.add_pet(pet1)
    owner.add_pet(pet2)
    
    # Create tasks OUT OF ORDER to test sorting
    task1 = Task(
        title="Evening walk",
        duration_minutes=45,
        priority="high",
        task_type="walk"
    )
    
    task2 = Task(
        title="Breakfast feeding",
        duration_minutes=15,
        priority="high",
        task_type="feeding"
    )
    
    task3 = Task(
        title="Morning walk",
        duration_minutes=30,
        priority="high",
        task_type="walk"
    )
    
    # Create recurring daily task
    task4 = Task(
        title="Daily medication",
        duration_minutes=5,
        priority="high",
        task_type="meds",
        frequency="daily"
    )
    
    # Create tasks for Whiskers (cat)
    task5 = Task(
        title="Morning feeding",
        duration_minutes=10,
        priority="medium",
        task_type="feeding"
    )
    
    task6 = Task(
        title="Playtime",
        duration_minutes=20,
        priority="low",
        task_type="enrichment"
    )
    
    # Add tasks to pets (out of order)
    pet1.add_task(task1)  # Evening walk
    pet1.add_task(task2)  # Breakfast feeding
    pet1.add_task(task3)  # Morning walk
    pet1.add_task(task4)  # Daily medication (recurring)
    pet2.add_task(task5)  # Morning feeding
    pet2.add_task(task6)  # Playtime
    
    # Mark one task as complete to test filtering
    task6.mark_complete()
    
    # Create scheduler
    scheduler = Scheduler(owner=owner)
    
    # Test filtering: Get incomplete tasks
    all_tasks = owner.get_all_tasks()
    incomplete_tasks = scheduler.filter_tasks(all_tasks, completed=False)
    print("=" * 60)
    print("📋 Filtering Demo: Incomplete Tasks Only")
    print("=" * 60)
    for task in incomplete_tasks:
        status = "✅" if task.completed else "❌"
        print(f"{status} {task.title} ({task.priority})")
    print()
    
    # Test filtering: Get tasks for specific pet
    mochi_tasks = scheduler.filter_tasks(all_tasks, pet_name="Mochi")
    print("=" * 60)
    print("🐕 Filtering Demo: Mochi's Tasks")
    print("=" * 60)
    for task in mochi_tasks:
        print(f"- {task.title} ({task.task_type}, {task.duration_minutes} min)")
    print()
    
    # Generate schedule
    schedule = scheduler.generate_schedule()
    
    # Test sorting: Sort scheduled tasks by time
    if schedule:
        sorted_schedule = scheduler.sort_by_time([task for task in all_tasks if task.scheduled_time is not None])
        print("=" * 60)
        print("⏰ Sorting Demo: Tasks Sorted by Scheduled Time")
        print("=" * 60)
        for task in sorted_schedule:
            print(f"{task.get_scheduled_time_str()}: {task.title}")
        print()
    
    # Print today's schedule
    print("=" * 60)
    print("🐾 PawPal+ - Today's Schedule")
    print("=" * 60)
    print()
    
    if schedule:
        print(f"Owner: {owner.name}")
        print(f"Available: {owner.available_start_hour:02d}:00 - {owner.available_end_hour:02d}:00")
        print()
        
        # Display conflict warnings if any
        if scheduler.conflict_warnings:
            print("⚠️  CONFLICT WARNINGS:")
            for warning in scheduler.conflict_warnings:
                print(f"   {warning}")
            print()
        
        print("Scheduled Tasks:")
        print("-" * 60)
        
        for item in schedule:
            print(f"⏰ {item['scheduled_time']} | {item['task']:20s} | "
                  f"Pet: {item['pet']:10s} | "
                  f"Priority: {item['priority']:6s} | "
                  f"Duration: {item['duration']} min")
        
        print("-" * 60)
        print()
        print(scheduler.explain_plan())
    else:
        print("No tasks scheduled.")
    
    # Test recurring tasks
    print()
    print("=" * 60)
    print("🔄 Recurring Task Demo")
    print("=" * 60)
    print(f"Before marking complete: {len(pet1.tasks)} tasks for Mochi")
    
    # Mark the daily medication task as complete
    pet1.mark_task_complete("Daily medication")
    
    print(f"After marking 'Daily medication' complete: {len(pet1.tasks)} tasks for Mochi")
    print("(A new instance should have been created automatically)")
    
    # Show the new recurring task
    recurring_tasks = [t for t in pet1.tasks if t.title == "Daily medication"]
    print(f"Found {len(recurring_tasks)} 'Daily medication' task(s):")
    for task in recurring_tasks:
        status = "✅ Complete" if task.completed else "❌ Incomplete"
        print(f"  - {status}, Frequency: {task.frequency}")
    
    print("=" * 60)
    
    # Test conflict detection with overlapping tasks
    print()
    print("=" * 60)
    print("⚠️  Conflict Detection Demo")
    print("=" * 60)
    
    # Create two tasks that will overlap
    conflict_task1 = Task(
        title="Overlapping task 1",
        duration_minutes=60,
        priority="high",
        task_type="walk"
    )
    conflict_task2 = Task(
        title="Overlapping task 2",
        duration_minutes=30,
        priority="medium",
        task_type="feeding"
    )
    
    # Manually schedule them to overlap
    conflict_task1.scheduled_time = 10  # 10:00
    conflict_task2.scheduled_time = 10  # 10:00 (same start time)
    
    # Create a test schedule with conflicts
    test_schedule = [
        {
            "task": conflict_task1.title,
            "pet": "Mochi",
            "type": conflict_task1.task_type,
            "duration": conflict_task1.duration_minutes,
            "priority": conflict_task1.priority,
            "scheduled_time": "10:00",
            "scheduled_hour": 10
        },
        {
            "task": conflict_task2.title,
            "pet": "Whiskers",
            "type": conflict_task2.task_type,
            "duration": conflict_task2.duration_minutes,
            "priority": conflict_task2.priority,
            "scheduled_time": "10:00",
            "scheduled_hour": 10
        }
    ]
    
    conflicts = scheduler.detect_conflicts(test_schedule)
    if conflicts:
        print("Detected conflicts:")
        for conflict in conflicts:
            print(f"  {conflict}")
    else:
        print("No conflicts detected.")
    
    print("=" * 60)


if __name__ == "__main__":
    main()
