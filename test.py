
import enum
import pygame

class Type(enum.Enum):
    """
    """
    EMPTY = 0
    WALL = 1
    START = 2
    END = 3

class Case():
    """
    """

    def __init__(self):
        self.g = 0
        self.h = 0
        self.f = 0
        self.x = 0
        self.y = 0
        self.type = Type.WALL    


"""
#successes, failures = pygame.init()
#print("{0} successes and {1} failures".format(successes, failures))

pygame.display.set_caption("Pathfinding program")
#screen = pygame.display.set_mode((720, 720))
screen = pygame.display.init()
"""

class Classe():
    def __init__(self, value1 = 25, value2 = 32):
        self.a = 1
        self.value1 = value1
        self.value2 = value2
        self.value3 = self.fonction(self.value1)
    def fonction(self, nombre):
        return nombre+8
    def fonction2(self, nombre):
        return nombre + self.fonction(nombre)

a = Classe()
a.a = 2
b = 4
c = a.fonction(b)

print(c)
print(a.value1)
print(a.value2)
print(a.value3)