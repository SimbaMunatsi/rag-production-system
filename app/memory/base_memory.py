from abc import ABC, abstractmethod


class BaseMemory(ABC):

    @abstractmethod
    def add(self, query, answer):
        pass

    @abstractmethod
    def get_history(self):
        pass