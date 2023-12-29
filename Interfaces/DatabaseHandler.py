from abc import ABC, abstractmethod


class DatabaseHandler(ABC):
    def __init__(self):
        pass

    @abstractmethod
    def connect(self, **kwargs):
        pass

    @abstractmethod
    def disconnect(self):
        pass

    @abstractmethod
    def write_data(self, **kwargs):
        pass


    @abstractmethod
    def read_data(self, **kwargs):
        pass