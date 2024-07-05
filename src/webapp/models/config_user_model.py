#!/usr/bin/env python3
#!/usr/bin/python3.12.4
from dataclasses import dataclass


@dataclass
class ConfigUserModel:
    username: str
    source: int
    dimension: str
    sid: list[str]
