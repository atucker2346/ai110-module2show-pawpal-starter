"""
PawPal+ System Logic Layer

This module contains the core classes for the pet care planning system:
- Owner: Represents the pet owner with availability and preferences
- Pet: Represents a pet with basic information
- Task: Represents a pet care task with duration and priority
- Scheduler: Generates daily schedules based on constraints
"""

from dataclasses import dataclass, field
from typing import List, Dict, Tuple, Optional


@dataclass
class Task:
    """Represents a pet care task with duration, priority, and completion status."""
    title: str
    duration_minutes: int
    priority: str  # "low", "medium", or "high"
    task_type: str  # "walk", "feeding", "meds", "enrichment", "grooming", etc.
    scheduled_time: Optional[int] = None  # Hour of day (0-23) when task is scheduled
    completed: bool = False
    frequency: Optional[str] = None  # e.g., "daily", "twice_daily", "weekly"
    
    def get_duration(self) -> int:
        """Returns duration in minutes."""
        return self.duration_minutes
    
    def get_priority_value(self) -> int:
        """Returns numeric priority value (1=low, 2=medium, 3=high)."""
        priority_map = {"low": 1, "medium": 2, "high": 3}
        return priority_map.get(self.priority.lower(), 1)
    
    def mark_complete(self) -> None:
        """Marks the task as completed."""
        self.completed = True
    
    def mark_incomplete(self) -> None:
        """Marks the task as not completed."""
        self.completed = False


@dataclass
class Pet:
    """Represents a pet with basic information and a list of tasks."""
    name: str
    species: str
    owner: 'Owner'
    tasks: List[Task] = field(default_factory=list)
    
    def get_info(self) -> Dict[str, str]:
        """Returns dictionary with pet information."""
        return {
            "name": self.name,
            "species": self.species,
            "owner": self.owner.name,
            "task_count": len(self.tasks)
        }
    
    def add_task(self, task: Task) -> None:
        """Adds a task to this pet's task list."""
        self.tasks.append(task)
    
    def remove_task(self, task_title: str) -> bool:
        """Removes a task by title. Returns True if task was found and removed."""
        for i, task in enumerate(self.tasks):
            if task.title == task_title:
                self.tasks.pop(i)
                return True
        return False
    
    def get_tasks(self) -> List[Task]:
        """Returns list of all tasks for this pet."""
        return self.tasks


@dataclass
class Owner:
    """Represents a pet owner with availability, preferences, and multiple pets."""
    name: str
    available_start_hour: int = 8  # Default: 8 AM
    available_end_hour: int = 20   # Default: 8 PM
    preferences: Dict[str, any] = field(default_factory=dict)
    pets: List[Pet] = field(default_factory=list)
    
    def get_available_time(self) -> Tuple[int, int]:
        """Returns tuple of (start_hour, end_hour) for owner's available time."""
        return (self.available_start_hour, self.available_end_hour)
    
    def update_preferences(self, prefs: Dict[str, any]) -> None:
        """Updates owner preferences dictionary."""
        self.preferences.update(prefs)
    
    def add_pet(self, pet: Pet) -> None:
        """Adds a pet to the owner's pet list."""
        self.pets.append(pet)
    
    def get_all_tasks(self) -> List[Task]:
        """Returns a list of all tasks from all pets."""
        all_tasks = []
        for pet in self.pets:
            all_tasks.extend(pet.get_tasks())
        return all_tasks
    
    def get_pets(self) -> List[Pet]:
        """Returns list of all pets."""
        return self.pets


class Scheduler:
    """Generates daily schedules for pet care tasks based on constraints."""
    
    def __init__(self, owner: Owner):
        """Initialize scheduler with owner."""
        self.owner = owner
        self.daily_plan: List[Dict] = []
    
    def add_task(self, task: Task, pet: Pet) -> None:
        """Adds a task to a pet's task list."""
        pet.add_task(task)
    
    def remove_task(self, task_title: str, pet: Pet) -> bool:
        """Removes a task by title from a pet. Returns True if task was found."""
        return pet.remove_task(task_title)
    
    def generate_schedule(self) -> List[Dict]:
        """Creates daily schedule based on constraints and priorities."""
        # Get all tasks from all pets
        all_tasks = self.owner.get_all_tasks()
        
        # Filter out completed tasks
        incomplete_tasks = [task for task in all_tasks if not task.completed]
        
        # Sort by priority (high to low), then by duration (shorter first)
        sorted_tasks = sorted(
            incomplete_tasks,
            key=lambda t: (-t.get_priority_value(), t.duration_minutes)
        )
        
        # Schedule tasks within available time window
        start_hour, end_hour = self.owner.get_available_time()
        available_minutes = (end_hour - start_hour) * 60
        current_time_minutes = 0
        scheduled = []
        
        for task in sorted_tasks:
            if current_time_minutes + task.duration_minutes <= available_minutes:
                scheduled_hour = start_hour + (current_time_minutes // 60)
                scheduled_minute = current_time_minutes % 60
                
                task.scheduled_time = scheduled_hour
                
                # Find which pet this task belongs to
                pet_name = "Unknown"
                for pet in self.owner.get_pets():
                    if task in pet.get_tasks():
                        pet_name = pet.name
                        break
                
                scheduled.append({
                    "task": task.title,
                    "pet": pet_name,
                    "type": task.task_type,
                    "duration": task.duration_minutes,
                    "priority": task.priority,
                    "scheduled_time": f"{scheduled_hour:02d}:{scheduled_minute:02d}",
                    "scheduled_hour": scheduled_hour
                })
                
                current_time_minutes += task.duration_minutes
        
        self.daily_plan = scheduled
        return scheduled
    
    def explain_plan(self) -> str:
        """Returns explanation of why tasks were scheduled as they were."""
        if not self.daily_plan:
            return "No tasks scheduled. Add tasks to pets to generate a schedule."
        
        explanation = "Today's Schedule Explanation:\n\n"
        explanation += f"Available time: {self.owner.available_start_hour:02d}:00 - {self.owner.available_end_hour:02d}:00\n\n"
        explanation += "Tasks were scheduled based on:\n"
        explanation += "1. Priority (high priority tasks scheduled first)\n"
        explanation += "2. Duration (shorter tasks scheduled first within same priority)\n"
        explanation += "3. Available time window\n\n"
        explanation += "Scheduled tasks:\n"
        
        for item in self.daily_plan:
            explanation += f"- {item['scheduled_time']}: {item['task']} ({item['pet']}) - {item['priority']} priority, {item['duration']} min\n"
        
        return explanation
