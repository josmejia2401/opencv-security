#!/usr/bin/env python3
#!/usr/bin/python3.12.4
from dataclasses import dataclass
from src.core.sub.sub_worker import SubWorker

@dataclass
class SubscriberModel:
    clazz: SubWorker
    name: str
    topic: str
