#!/usr/bin/env python3
#!/usr/bin/python3.12.4
from dataclasses import dataclass


@dataclass
class UserModel:
    username: str
    full_name: str
    sid: list[str]
