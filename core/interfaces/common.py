from abc import ABC, ABCMeta, abstractmethod

class ISave(ABC, metaclass=ABCMeta):
    
    @abstractmethod
    def save(self)->None:
        pass