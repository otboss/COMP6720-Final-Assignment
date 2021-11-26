from enum import Enum

class Privileges(Enum):
    SELECT = 1,
    UPDATE = 2,
    INSERT = 3,
    DELETE = 4,
    CREATE = 5,
    SHOW = 6,
    DROP = 7,
