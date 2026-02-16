"""
Demo script for PawPal+ system.

This script demonstrates the core functionality by creating an owner,
multiple pets, tasks, and generating a daily schedule.
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
    
    # Create tasks for Mochi (dog)
    task1 = Task(
        title="Morning walk",
        duration_minutes=30,
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
        title="Evening walk",
        duration_minutes=45,
        priority="high",
        task_type="walk"
    )
    
    # Create tasks for Whiskers (cat)
    task4 = Task(
        title="Morning feeding",
        duration_minutes=10,
        priority="medium",
        task_type="feeding"
    )
    
    task5 = Task(
        title="Playtime",
        duration_minutes=20,
        priority="low",
        task_type="enrichment"
    )
    
    # Add tasks to pets
    pet1.add_task(task1)
    pet1.add_task(task2)
    pet1.add_task(task3)
    pet2.add_task(task4)
    pet2.add_task(task5)
    
    # Create scheduler
    scheduler = Scheduler(owner=owner)
    
    # Generate schedule
    schedule = scheduler.generate_schedule()
    
    # Print today's schedule
    print("=" * 60)
    print("🐾 PawPal+ - Today's Schedule")
    print("=" * 60)
    print()
    
    if schedule:
        print(f"Owner: {owner.name}")
        print(f"Available: {owner.available_start_hour:02d}:00 - {owner.available_end_hour:02d}:00")
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
    
    print("=" * 60)


if __name__ == "__main__":
    main()
