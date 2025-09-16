from abc import ABC, abstractmethod
import math

class Shape(ABC):
    def __init__(self, length: float, width: float):
        self.length = length
        self.width = width
    
    def all_info(self) -> tuple[float, float]:
        return self.length, self.width
    
    @abstractmethod
    def get_perimiter(self) -> float:
        pass

    @abstractmethod
    def get_area(self) -> float:
        pass
    
class Rectangle(Shape):
    def get_perimiter(self):
        return (self.length * 2) + (self.width * 2)
    
    def get_area(self):
        return (self.length * self.width)
    
class Square(Rectangle):
    def __init__(self, length, width = None):
        super().__init__(length, length)

class Triangle(Shape):
    def get_perimiter(self):
        return self.length + self.width + math.sqrt(self.length ** 2 + self.width ** 2)
    
    def get_area(self):
        return (self.length * self.width) / 2