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
class Owner:
    """Represents a pet owner with availability and preferences."""
    name: str
    available_start_hour: int = 8  # Default: 8 AM
    available_end_hour: int = 20   # Default: 8 PM
    preferences: Dict[str, any] = field(default_factory=dict)
    
    def get_available_time(self) -> Tuple[int, int]:
        """Returns tuple of (start_hour, end_hour) for owner's available time."""
        pass
    
    def update_preferences(self, prefs: Dict[str, any]) -> None:
        """Updates owner preferences dictionary."""
        pass


@dataclass
class Pet:
    """Represents a pet with basic information."""
    name: str
    species: str
    owner: Owner
    
    def get_info(self) -> Dict[str, str]:
        """Returns dictionary with pet information."""
        pass


@dataclass
class Task:
    """Represents a pet care task with duration and priority."""
    title: str
    duration_minutes: int
    priority: str  # "low", "medium", or "high"
    task_type: str  # "walk", "feeding", "meds", "enrichment", "grooming", etc.
    
    def get_duration(self) -> int:
        """Returns duration in minutes."""
        pass
    
    def get_priority_value(self) -> int:
        """Returns numeric priority value (1=low, 2=medium, 3=high)."""
        pass


class Scheduler:
    """Generates daily schedules for pet care tasks based on constraints."""
    
    def __init__(self, owner: Owner, pet: Pet):
        """Initialize scheduler with owner and pet."""
        self.owner = owner
        self.pet = pet
        self.tasks: List[Task] = []
        self.daily_plan: List[Dict] = []
    
    def add_task(self, task: Task) -> None:
        """Adds a task to the scheduler."""
        pass
    
    def remove_task(self, task_title: str) -> None:
        """Removes a task by title."""
        pass
    
    def generate_schedule(self) -> List[Dict]:
        """Creates daily schedule based on constraints and priorities."""
        pass
    
    def explain_plan(self) -> str:
        """Returns explanation of why tasks were scheduled as they were."""
        pass
