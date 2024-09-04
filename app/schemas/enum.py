from enum import Enum

class Priority(Enum):
    CRITICAL = 1
    HIGH = 2
    MEDIUM = 3
    LOW = 4
    
class Status(Enum):
    NEW = "New"
    ACTIVE = "Active"
    RESOLVED = "Resolved"
    CLOSED = "Closed"
    ABANDONED = "Abandoned"
    
class Mode(Enum):
    ON_SITE = "On site"
    REMOTE = "Remote"
    HYBRID = "Hybrid"
    SYSTEM = "System"
    
     