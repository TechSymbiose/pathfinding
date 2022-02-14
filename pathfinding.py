from importlib.resources import path
from re import S
import pygame
import enum
from math import *
from random import *

class Type(enum.Enum):
    """ Class which defines an enumeration type for cases of a table
    - EMPTY : empty case where we can go
    - WALL : A wall where we can't go
    - START : the start of the pathfinding
    - END : the end of the pathfinding
    - EVALUATED : the different values are calculated
    - NON_EVALUATED : the case is located next to an evaluated case
    - PATH : the case is a part of the path
    - CURRENT : the current case which is evaluated
    """

    EMPTY = 0
    WALL = 1
    START = 2
    END = 3
    EVALUATED = 4
    NON_EVALUATED = 5
    PATH = 6
    CURRENT = 7

class Image():
    """ Class which defines images to print with pygame
    """
    def __init__(self, width, height):

        self.width = width
        self.height = height

        self.start = pygame.transform.scale((pygame.image.load("blue_box.png")).convert(), (width, height))
        self.evaluated = pygame.transform.scale((pygame.image.load("red_box.png")).convert(), (width, height))
        self.nonEvaluated = pygame.transform.scale((pygame.image.load("green_box.png")).convert(), (width, height))
        self.end = pygame.transform.scale((pygame.image.load("orange_box.png")).convert(), (width, height))
        self.wall = pygame.transform.scale((pygame.image.load("black_box.png")).convert(), (width, height))
        self.empty = pygame.transform.scale((pygame.image.load("grey_box.png")).convert(), (width, height))
        self.path = pygame.transform.scale((pygame.image.load("cyan_box.png")).convert(), (width, height))
        self.current = pygame.transform.scale((pygame.image.load("pink_box.png")).convert(), (width, height))

class Case():
    """ Class which defines a case in a table. Each case is characterized by :
    - the distance G relative to the start case
    - the distance H relative to the end case
    - the distance F between the start case and the end case passing throw this case.
    F = G + H
    - The position (x,y) in the table
    - The type of the case (START, END, EMPTY, WALL, EVALUATED, NON_EVALUATED, PATH).
    """

    def __init__(self):

        self.g = 0
        self.h = 0
        self.f = 0
        self.x = 0
        self.y = 0
        self.type = Type.EMPTY

class Pathfinding:
    """ Class which defines the pathfinding algorithm
    """

    def __init__(self, maxWidth = 1760, maxHeight = 990, columns = 68, lines = 32):

        successes, failures = pygame.init()
        print("{0} successes and {1} failures".format(successes, failures))
        pygame.font.init()

        self.columns = 0
        self.lines = 0   
        self._width = 0
        self._height = 0

        self.speed = 1
        self.FPS = 60

        pygame.display.set_caption("Pathfinding program")
        self.screen = pygame.display.init()
        self.screen = pygame.display.set_mode((self._width, self._height))
        self.screen.fill((0, 0, 0))

        self.table = [[Case()]]
        self.image = Image(0,0)
        self.tableRect = []
        (self.start, self.end) = (Case(), Case())
        self.start.type = Type.START
        self.end.type = Type.END

        self.setWindow(maxWidth, maxHeight, columns, lines)

    def setWindow(self, maxWidth, maxHeight, columns, lines):
        self.lines = lines
        self.columns = columns

        if ((maxWidth/self.columns < maxHeight/self.lines)):
            self._width = int((maxWidth/self.columns))*self.columns
            self._height = int((((min((maxWidth/self.columns), (maxHeight/self.lines)) / max((maxWidth/self.columns), (maxHeight/self.lines))) * maxHeight)/self.lines))*self.lines

        else:
            self._width = int((((min((maxWidth/self.columns), (maxHeight/self.lines)) / max((maxWidth/self.columns), (maxHeight/self.lines))) * maxWidth)/self.columns))*self.columns
            self._height = int((maxHeight/self.lines))*self.lines

        self.screen = pygame.display.set_mode((self._width, self._height))
        self.screen.fill((0, 0, 0))

        self.table = [[Case() for j in range(self.columns)] for i in range(self.lines)]
        self.image = Image(self._width/self.columns, self._height/self.lines)

    def initTable(self):

        for i in range(self.lines):
            for j in range(self.columns):
                self.table[i][j].type = Type.WALL if (randint(0,1) == 1) else Type.EMPTY
                (self.table[i][j].x, self.table[i][j].y) = (j,i)
        
        self.start.x = randint(0,self.columns-1)
        self.start.y = randint(0,self.lines-1)

        self.end.x = randint(0,self.columns-1)
        self.end.y = randint(0,self.lines-1)

        while (self.end.x ==  self.start.x and  self.end.y ==  self.start.y):
            self.end.x = randint(0,self.columns-1)
            self.end.y = randint(0,self.lines-1)
        
        self.table[self.start.y][self.start.x].type = Type.START
        self.table[self.end.y][self.end.x].type = Type.END

    def run(self):

        boxesToEvaluate = []
        boxesEvaluated = []
        current = self.table[self.start.y][self.start.x]
        pathFound = False
        impossiblePathfinding = False
        clock = pygame.time.Clock()

        boxesToEvaluate.append(self.table[self.start.y][self.start.x]) # Adding the start box in the tab of boxes to evaluate

        while True:
            clock.tick(self.FPS)

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    quit()

                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_SPACE:

                        while (not(pathFound or impossiblePathfinding)):

                            if (len(boxesToEvaluate) == 0):
                                print("Pathfinding impossible to solve")
                                impossiblePathfinding = True

                            else :

                                if ((current.type != Type.START) and (current.type != Type.END)):
                                    current.type = Type.EVALUATED

                                current = self.lowestFcostCase(boxesToEvaluate)
                                del boxesToEvaluate[self.lowestFcostCaseIndex(boxesToEvaluate)]
                                boxesEvaluated.append(current)

                                if ((current.type != Type.START) and (current.type != Type.END)):
                                    current.type = Type.CURRENT

                                if (current.type == Type.END):
                                    pathFound = True
                                    self.getPath()
                                    print("A path has been found !")

                                if (not(pathFound)):

                                    for i in (-1, 0, 1):
                                        for j in (-1, 0, 1):

                                            if ((not((i == 0) and (j == 0)) and (current.x + j < self.columns) and (current.y + i < self.lines) and (current.x + j >= 0) and (current.y + i >= 0))):

                                                self.table[current.y+i][current.x+j].g = self.calculatingGcost(self.table[current.y+i][current.x+j], current)
                                                self.table[current.y+i][current.x+j].h = self.calculatingHcost(self.table[current.y+i][current.x+j])
                                                self.table[current.y+i][current.x+j].f = self.calculatingFcost(self.table[current.y+i][current.x+j])

                                                if (self.table[current.y+i][current.x+j].type == Type.EMPTY):
                                                    boxesToEvaluate.append(self.table[current.y+i][current.x+j])
                                                    self.table[current.y+i][current.x+j].type = Type.NON_EVALUATED
                                                elif (self.table[current.y+i][current.x+j].type == Type.END):
                                                    boxesToEvaluate.append(self.table[current.y+i][current.x+j])
                                                        
                            self.display()
                            pygame.time.wait(self.speed)
                            pygame.display.update()

    def display(self):

        for i in range(self.lines):
            for j in range(self.columns):
                if (self.table[i][j].type == Type.EMPTY):
                    self.screen.blit(self.image.empty, self.tableRect[i][j])
                elif (self.table[i][j].type == Type.WALL):
                    self.screen.blit(self.image.wall, self.tableRect[i][j])
                elif (self.table[i][j].type == Type.START):
                    self.screen.blit(self.image.start, self.tableRect[i][j])
                elif (self.table[i][j].type == Type.END):
                    self.screen.blit(self.image.end, self.tableRect[i][j])
                elif (self.table[i][j].type == Type.EVALUATED):
                    self.screen.blit(self.image.evaluated, self.tableRect[i][j])
                elif (self.table[i][j].type == Type.NON_EVALUATED):
                    self.screen.blit(self.image.nonEvaluated, self.tableRect[i][j])
                elif (self.table[i][j].type == Type.CURRENT):
                    self.screen.blit(self.image.current, self.tableRect[i][j])
                elif (self.table[i][j].type == Type.PATH):
                    self.screen.blit(self.image.path, self.tableRect[i][j])
        
        pygame.display.update()

    def initDisplay(self):

        self.tableRect = [[pygame.Rect((j*self._width/self.columns, i*self._height/self.lines), (self._width/self.columns, self._height/self.lines)) for j in range(self.columns)] for i in range(self.lines)]
        for i in range(self.lines):
            for j in range(self.columns):
                self.tableRect[i][j] = pygame.Rect(((j*self._width/self.columns), (i*self._height/self.lines)), ((self._width/self.columns),(self._height/self.lines)))

        self.display()
    
    def lowestFcostCase(self, boxesToEvaluate):
        fCostMinNodes = []
        fCostMinNode = boxesToEvaluate[0]
        fCostMin = boxesToEvaluate[0].f
        
        if len(boxesToEvaluate) > 1:
            for i in range(len(boxesToEvaluate)):
                if (boxesToEvaluate[i].f < fCostMin):
                    fCostMin = boxesToEvaluate[i].f

            for i in range(len(boxesToEvaluate)):
                if (boxesToEvaluate[i].f == fCostMin):
                    fCostMinNodes.append(boxesToEvaluate[i])

            hCostMin = fCostMinNodes[0].h
            fCostMinNode = fCostMinNodes[0]

            for i in range(len(fCostMinNodes)):
                if (fCostMinNodes[i].h < hCostMin):
                    hCostMin = fCostMinNodes[i].h
                    fCostMinNode = fCostMinNodes[i]

        return fCostMinNode
    
    def lowestFcostCaseIndex(self, boxesToEvaluate):
        case = self.lowestFcostCase(boxesToEvaluate)
        index = 0

        for i in range(len(boxesToEvaluate)):
            if (boxesToEvaluate[i].x == case.x and boxesToEvaluate[i].y == case.y):
                index = i
    
        return index

    def calculatingGcost(self, boxeEvaluated, boxeMother):
        if boxeMother.type == Type.START:
            if boxeEvaluated.x == boxeMother.x or boxeMother.y == boxeMother.y:
                gCost = 10
            else:
                gCost = 14
        elif (boxeEvaluated.x == boxeMother.x or boxeEvaluated.y == boxeMother.y) and (boxeMother.g + 10 < boxeEvaluated.g or boxeEvaluated.type == Type.EMPTY or boxeEvaluated.type == Type.END):
            gCost = boxeMother.g + 10
        elif not(boxeEvaluated.x == boxeMother.x or boxeEvaluated.y == boxeMother.y) and (boxeMother.g + 14 < boxeEvaluated.g or boxeEvaluated.type == Type.EMPTY or boxeEvaluated.type == Type.END):
            gCost = boxeMother.g + 14
        else:
            gCost = boxeEvaluated.g
        return gCost
    
    def calculatingHcost(self, boxeEvaluated):
        if boxeEvaluated.x == self.end.x:
            hCost = fabs(boxeEvaluated.y-self.end.y)*10

        if (boxeEvaluated.y == self.end.y):
            hCost = fabs(boxeEvaluated.x-self.end.x)*10

        else:
            hCost = min(fabs(boxeEvaluated.x - self.end.x),fabs(boxeEvaluated.y-self.end.y))*14 + (fabs(boxeEvaluated.x - self.end.x)-min(fabs(boxeEvaluated.x - self.end.x),fabs(boxeEvaluated.y-self.end.y)))*10 + (fabs(boxeEvaluated.y - self.end.y)-min(fabs(boxeEvaluated.x - self.end.x),fabs(boxeEvaluated.y-self.end.y)))*10
        return int(hCost)
        
    def calculatingFcost(self, current):    
        return current.g + current.h

    def lowestFcostCasePath(self, boxesToEvaluate):
        fCostMinNodes = []
        fCostMinNode = boxesToEvaluate[0]
        fCostMin = boxesToEvaluate[0].f
        if len(boxesToEvaluate) > 1:
            for i in range(len(boxesToEvaluate)):
                if boxesToEvaluate[i].f < fCostMin:
                    fCostMin = boxesToEvaluate[i].f

            for i in range(len(boxesToEvaluate)):
                if boxesToEvaluate[i].f == fCostMin:
                    fCostMinNodes.append(boxesToEvaluate[i])

            gCostMin = fCostMinNodes[0].g
            fCostMinNode = fCostMinNodes[0]

            for i in range(len(fCostMinNodes)):
                if fCostMinNodes[i].g < gCostMin:
                    gCostMin = fCostMinNodes[i].g
                    fCostMinNode = fCostMinNodes[i]

        return fCostMinNode

    def getPath(self):
        current = self.table[self.end.y][self.end.x]
        neighbours = []

        while (not(current.type == Type.START)):
            for i in(-1,0,1):
                for j in (-1,0,1):
                    if ((not(i == 0 and j == 0)) and (current.y + i >= 0) and (current.x + j >= 0) and (current.y + i < self.lines) and (current.x + j < self.columns)):
                        if ((self.table[current.y+i][current.x+j].type == Type.EVALUATED) or (self.table[current.y+i][current.x+j].type == Type.START)):
                            if (self.table[current.y+i][current.x+j].type == Type.START):
                                neighbours = []
                                neighbours.append(self.table[current.y+i][current.x+j])
                                break
                            else:
                                neighbours.append(self.table[current.y+i][current.x+j])
            if (len(neighbours) > 0):
                current = self.lowestFcostCasePath(neighbours)
            if current.type != Type.START:
                current.type = Type.PATH

            neighbours = []
            self.display()
        
def main():
    pathfinding = Pathfinding(1920,1080,200,100)
    pathfinding.initTable()
    pathfinding.initDisplay()
    pathfinding.run()

if __name__ == "__main__":
    main()