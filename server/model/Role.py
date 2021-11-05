from typing import List, Any

from server.model.Privileges import Privileges

class Role:
    role: str
    privileges: List[Privileges]

    def __init__(self, role: str, privilages: List[Privileges]) -> None:
        self.role = role
        self.privilages = privilages
