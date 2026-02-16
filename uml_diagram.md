# PawPal+ UML Class Diagram

```mermaid
classDiagram
    class Owner {
        +str name
        +int available_start_hour
        +int available_end_hour
        +dict preferences
        +get_available_time() tuple
        +update_preferences(dict) None
    }
    
    class Pet {
        +str name
        +str species
        +Owner owner
        +get_info() dict
    }
    
    class Task {
        +str title
        +int duration_minutes
        +str priority
        +str task_type
        +get_duration() int
        +get_priority_value() int
    }
    
    class Scheduler {
        +list tasks
        +Owner owner
        +Pet pet
        +list daily_plan
        +add_task(Task) None
        +remove_task(str) None
        +generate_schedule() list
        +explain_plan() str
    }
    
    Owner "1" --> "*" Pet : owns
    Pet "1" --> "1" Owner : belongs_to
    Scheduler "1" --> "1" Owner : uses
    Scheduler "1" --> "1" Pet : schedules_for
    Scheduler "1" --> "*" Task : manages
```

## Class Descriptions

### Owner
- **Attributes**: 
  - `name`: Owner's name
  - `available_start_hour`: When owner's day starts (0-23)
  - `available_end_hour`: When owner's day ends (0-23)
  - `preferences`: Dictionary of owner preferences (e.g., preferred walk times)
- **Methods**:
  - `get_available_time()`: Returns tuple of (start_hour, end_hour)
  - `update_preferences(prefs)`: Updates owner preferences

### Pet
- **Attributes**:
  - `name`: Pet's name
  - `species`: Type of pet (dog, cat, etc.)
  - `owner`: Reference to Owner instance
- **Methods**:
  - `get_info()`: Returns dictionary with pet information

### Task
- **Attributes**:
  - `title`: Task name/description
  - `duration_minutes`: How long the task takes
  - `priority`: Priority level ("low", "medium", "high")
  - `task_type`: Type of task (walk, feeding, meds, enrichment, grooming)
- **Methods**:
  - `get_duration()`: Returns duration in minutes
  - `get_priority_value()`: Returns numeric priority (1=low, 2=medium, 3=high)

### Scheduler
- **Attributes**:
  - `tasks`: List of Task objects
  - `owner`: Owner instance
  - `pet`: Pet instance
  - `daily_plan`: Generated schedule for the day
- **Methods**:
  - `add_task(task)`: Adds a task to the scheduler
  - `remove_task(task_title)`: Removes a task by title
  - `generate_schedule()`: Creates daily schedule based on constraints
  - `explain_plan()`: Returns explanation of why tasks were scheduled
