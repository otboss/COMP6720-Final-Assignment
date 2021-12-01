from enum import Enum

# Privileges : The privileges that are grantable to users
class Privileges(Enum):
    SELECT = 1,
    UPDATE = 2,
    INSERT = 3,
    DELETE = 4,
    CREATE = 5,
    SHOW = 6,
    DROP = 7,
    ALTER = 8,
    DESCRIBE=9,
