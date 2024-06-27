#!/usr/bin/env python3
#!/usr/bin/python3.12.4
from dataclasses import dataclass

@dataclass
class DefaultModel:
    name: str
    salary: int

    def total(self) -> float:
        return self.salary * 0.1