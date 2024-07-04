#!/usr/bin/env python3
#!/usr/bin/python3.12.4
from abc import ABC, abstractmethod
from src.core.models.proccess_frame_model import ProcessFrameModel

class SubWorker(ABC):

    def __init__(self):
        super().__init__()

    @abstractmethod
    def on_message(self, message: ProcessFrameModel = None) -> None:
        raise NotImplementedError("Can't use 'set' on an ADC!")