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
from datetime import datetime, timedelta


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
    
    def mark_complete(self) -> Optional['Task']:
        """Marks the task as completed. Returns a new task instance if frequency is set."""
        self.completed = True
        
        # Handle recurring tasks
        if self.frequency:
            new_task = Task(
                title=self.title,
                duration_minutes=self.duration_minutes,
                priority=self.priority,
                task_type=self.task_type,
                frequency=self.frequency,
                completed=False
            )
            return new_task
        return None
    
    def mark_incomplete(self) -> None:
        """Marks the task as not completed."""
        self.completed = False
    
    def get_scheduled_time_str(self) -> str:
        """Returns scheduled time as HH:MM string, or empty string if not scheduled."""
        if self.scheduled_time is not None:
            return f"{self.scheduled_time:02d}:00"
        return ""


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
    
    def mark_task_complete(self, task_title: str) -> bool:
        """Marks a task as complete and handles recurring tasks. Returns True if task was found."""
        for task in self.tasks:
            if task.title == task_title:
                new_task = task.mark_complete()
                if new_task:
                    # Add new recurring task instance
                    self.add_task(new_task)
                return True
        return False


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
        self.conflict_warnings: List[str] = []
    
    def add_task(self, task: Task, pet: Pet) -> None:
        """Adds a task to a pet's task list."""
        pet.add_task(task)
    
    def remove_task(self, task_title: str, pet: Pet) -> bool:
        """Removes a task by title from a pet. Returns True if task was found."""
        return pet.remove_task(task_title)
    
    def sort_by_time(self, tasks: List[Task]) -> List[Task]:
        """Sorts tasks by their scheduled time (HH:MM format). Unscheduled tasks go to the end."""
        def time_key(task: Task) -> Tuple[int, int]:
            """Returns (hour, minute) tuple for sorting, or (999, 999) for unscheduled tasks."""
            if task.scheduled_time is not None:
                return (task.scheduled_time, 0)
            return (999, 999)  # Put unscheduled tasks at the end
        
        return sorted(tasks, key=time_key)
    
    def filter_tasks(self, tasks: List[Task], completed: Optional[bool] = None, pet_name: Optional[str] = None) -> List[Task]:
        """Filters tasks by completion status and/or pet name."""
        filtered = tasks
        
        # Filter by completion status
        if completed is not None:
            filtered = [task for task in filtered if task.completed == completed]
        
        # Filter by pet name
        if pet_name is not None:
            pet_tasks = []
            for pet in self.owner.get_pets():
                if pet.name.lower() == pet_name.lower():
                    pet_tasks.extend([task for task in filtered if task in pet.get_tasks()])
            filtered = pet_tasks
        
        return filtered
    
    def detect_conflicts(self, schedule: List[Dict]) -> List[str]:
        """Detects scheduling conflicts where tasks overlap in time. Returns list of warning messages."""
        warnings = []
        
        # Group tasks by scheduled time
        time_slots = {}
        for item in schedule:
            time_key = item["scheduled_time"]
            if time_key not in time_slots:
                time_slots[time_key] = []
            time_slots[time_key].append(item)
        
        # Check for conflicts (same time or overlapping durations)
        for time_slot, items in time_slots.items():
            if len(items) > 1:
                # Multiple tasks at the same time
                pet_names = [item["pet"] for item in items]
                task_names = [item["task"] for item in items]
                warnings.append(
                    f"⚠️ Conflict at {time_slot}: Multiple tasks scheduled - "
                    f"{', '.join(task_names)} for pets {', '.join(set(pet_names))}"
                )
            
            # Check for overlapping durations
            for i, item1 in enumerate(items):
                for item2 in items[i+1:]:
                    # Calculate end times
                    start_time1 = self._parse_time(item1["scheduled_time"])
                    end_time1 = start_time1 + timedelta(minutes=item1["duration"])
                    start_time2 = self._parse_time(item2["scheduled_time"])
                    end_time2 = start_time2 + timedelta(minutes=item2["duration"])
                    
                    # Check if times overlap
                    if not (end_time1 <= start_time2 or end_time2 <= start_time1):
                        warnings.append(
                            f"⚠️ Overlap detected: '{item1['task']}' ({item1['pet']}) and "
                            f"'{item2['task']}' ({item2['pet']}) overlap in time"
                        )
        
        return warnings
    
    def _parse_time(self, time_str: str) -> datetime:
        """Helper method to parse HH:MM time string into datetime object."""
        hour, minute = map(int, time_str.split(":"))
        return datetime(2000, 1, 1, hour, minute)
    
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
        
        # Detect and report conflicts
        conflicts = self.detect_conflicts(scheduled)
        if conflicts:
            self.conflict_warnings = conflicts
        else:
            self.conflict_warnings = []
        
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
