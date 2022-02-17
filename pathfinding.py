import pygame
import enum
from math import *
from random import *

class Type(enum.Enum):
    """ Class which defines an enumerated type for boxes of a map :
    - EMPTY : empty box where we pass through 
    - WALL : A wall where we can't pas through 
    - START : the start of the pathfinding map
    - END : the end of the pathfinding map
    - EVALUATED : the different values are calculated
    - NON_EVALUATED : the box is located next to an evaluated box
    - PATH : the box is a part of the path
    - CURRENT : the current box which is evaluated
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
    """ Class which defines the image to print with pygame. The size of one image representing a box is width x height. There are 8 types of images with 8 different color :
    - start : blue 
    - evaluated : red
    - nonEvaluated :green
    - end : orange
    - wall : black
    - empty : grey
    - path : cyan
    - current : pink
    """
    def __init__(self, width, height):

        self.width = width
        self.height = height

        # For each image, the image is loaded, then converted into a displayable image and finally transform into the good scale (to get a width x height image)
        self.start = pygame.transform.scale((pygame.image.load("images/blue_box.png")).convert(), (width, height))
        self.evaluated = pygame.transform.scale((pygame.image.load("images/red_box.png")).convert(), (width, height))
        self.nonEvaluated = pygame.transform.scale((pygame.image.load("images/green_box.png")).convert(), (width, height))
        self.end = pygame.transform.scale((pygame.image.load("images/orange_box.png")).convert(), (width, height))
        self.wall = pygame.transform.scale((pygame.image.load("images/black_box.png")).convert(), (width, height))
        self.empty = pygame.transform.scale((pygame.image.load("images/grey_box.png")).convert(), (width, height))
        self.path = pygame.transform.scale((pygame.image.load("images/cyan_box.png")).convert(), (width, height))
        self.current = pygame.transform.scale((pygame.image.load("images/pink_box.png")).convert(), (width, height))

class box():
    """ Class which defines a box in a table. Each box is characterized by :
    - the distance G relative to the start box
    - the distance H relative to the end box
    - the distance F between the start box and the end box passing throw this box.
    (F = G + H)
    - The position (x,y) in the table
    - The type of the box (START, END, EMPTY, WALL, EVALUATED, NON_EVALUATED, PATH).
    """

    def __init__(self):

        self.g = 0
        self.h = 0
        self.f = 0
        self.column = 0
        self.line = 0
        self.type = Type.EMPTY

class Pathfinding():
    """ Class which defines the pathfinding algorithm. 
    It can generate a window with a max width and a max height determined by the number of lines and columns of the map.
    The map is generated randomly and the path between the start box and the end box is determined using a pathfinding algorithm.
    The solving process is launched pressing the space bar key and displayed to see what the algorithm do and the final path is displayed if the map can be solved.
    """

    """ __init__ function : 
    brief : initialize the variables used for the pathfinding and the windows 
    param : 
    - maxWidth : the maximum width of the window created
    - maxHeight : the maximum height of the window created
    - columns : the number of columns of the map
    - lines : the number of lines of the map
    """
    def __init__(self, maxWidth, maxHeight, columns, lines):

        successes, failures = pygame.init()
        print("{0} successes and {1} failures".format(successes, failures))
        pygame.font.init()

        # Initialize the variables used to initialize display
        self.columns = 0
        self.lines = 0   
        self._width = 0
        self._height = 0

        self.delay = 15 # the delay between 2 iterations of the algorithm
        self.FPS = 60 # Frames Per Seconds to display

        pygame.display.set_caption("Pathfinding program")

        # Initialization of the window
        self.screen = pygame.display.init()
        self.screen = pygame.display.set_mode((self._width, self._height))
        self.screen.fill((0, 0, 0))

        # Initialize variables for the algorithm process
        self.table = [[]]
        self.tableRect = []
        self.image = Image(0,0)
        (self.start, self.end) = (box(), box())
        self.start.type = Type.START
        self.end.type = Type.END
        self.path = []

        self.set_window(maxWidth, maxHeight, columns, lines)

    
    """ set_window function : 
    brief : set the variables for display
    param :
    - maxWidth : the maximum width of the window created
    - maxHeight : the maximum height of the window created
    - columns : the number of columns of the map
    - lines : the number of lines of the map
    """
    def set_window(self, maxWidth, maxHeight, columns, lines):
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

        self.table = [[box() for column in range(self.columns)] for line in range(self.lines)]
        self.image = Image(self._width/self.columns, self._height/self.lines)

    """ init_map function : 
    brief : initialize and generate the map with the variables used for the map.
    The map is generated randomly with empty boxes, walls and a start and end box
    param : none
    """
    def init_map(self):

        for line in range(self.lines):
            for column in range(self.columns):
                self.table[line][column].type = Type.WALL if (randint(0,1) == 1) else Type.EMPTY
                (self.table[line][column].line, self.table[line][column].column) = (line,column)

        self.start.line = randint(0,self.lines-1)
        self.start.column = randint(0,self.columns-1)
        
        self.end.line = randint(0,self.lines-1)
        self.end.column = randint(0,self.columns-1)

        while ((self.end.line ==  self.start.line) and (self.end.column ==  self.start.column)):
            self.end.line = randint(0,self.lines-1)
            self.end.column = randint(0,self.columns-1)
        
        self.table[self.start.line][self.start.column].type = Type.START
        self.table[self.end.line][self.end.column].type = Type.END

    """ init_display function : 
    brief : init the table of rectangles used to blit the images on
    param : none 
    """
    def init_display(self):

        self.tableRect = [[pygame.Rect((column*self._width/self.columns, line*self._height/self.lines), (self._width/self.columns, self._height/self.lines)) for column in range(self.columns)] for line in range(self.lines)]
        for line in range(self.lines):
            for column in range(self.columns):
                self.tableRect[line][column] = pygame.Rect(((column*self._width/self.columns), (line*self._height/self.lines)), ((self._width/self.columns),(self._height/self.lines)))

    """ get_event function : 
    brief : get the event using pygame library to close the window and update the variable used to pause the program
    param :
    - play : the boolean used to pause the program
    """
    def get_event(self, play):
        for event in pygame.event.get():
            if (event.type == pygame.QUIT):
                quit()
            if (event.type == pygame.KEYDOWN):
                if (event.key == pygame.K_ESCAPE):
                    quit()
                if (event.key == pygame.K_SPACE):
                    play = not play

        return play

    """ lowest_f_cost_box function : 
    brief : Determine the box with the lowest F cost
    param : 
    - boxesToEvaluate : the list of boxes which need to be evaluated
    return fCostMinNode : the node/box with the lowest F cost
    """
    def lowest_f_cost_box(self, boxesToEvaluate):
        fCostMinNodes = []
        fCostMinNode = boxesToEvaluate[0]
        fCostMin = boxesToEvaluate[0].f
        
        if (len(boxesToEvaluate) > 1):
            for index in range(len(boxesToEvaluate)):
                if (boxesToEvaluate[index].f < fCostMin):
                    fCostMin = boxesToEvaluate[index].f

            for index in range(len(boxesToEvaluate)):
                if (boxesToEvaluate[index].f == fCostMin):
                    fCostMinNodes.append(boxesToEvaluate[index])

            hCostMin = fCostMinNodes[0].h
            fCostMinNode = fCostMinNodes[0]

            for index in range(len(fCostMinNodes)):
                if (fCostMinNodes[index].h < hCostMin):
                    hCostMin = fCostMinNodes[index].h
                    fCostMinNode = fCostMinNodes[index]

        return fCostMinNode

    """ lowest_f_cost_box_index function : 
    brief : Determine the index of the box with the lowest F cost
    param : 
    - boxesToEvaluate : the list of boxes which need to be evaluated
    return lowest_f_cost_box_index : the index of the box with the lowest F cost
    """
    def lowest_f_cost_box_index(self, boxesToEvaluate):
        box = self.lowest_f_cost_box(boxesToEvaluate)
        lowest_f_cost_box_index = 0

        for index in range(len(boxesToEvaluate)):
            if ((boxesToEvaluate[index].line == box.line) and (boxesToEvaluate[index].column == box.column)):
                lowest_f_cost_box_index = index
    
        return lowest_f_cost_box_index

    """ calculating_g_cost function : 
    brief : Calculate the G cost of the box which need to be evaluated thanks to its mother box
    param : 
    - evaluatedbox : the box which need to be evaluated
    - motherbox : the mother box of the box which need to be evaluated
    return gCost : the G cost of the evaluated box
    """
    def calculating_g_cost(self, evaluatedbox, motherbox):
        if motherbox.type == Type.START:
            if ((motherbox.line == motherbox.line) or (evaluatedbox.column == motherbox.column)):
                gCost = 10
            else:
                gCost = 14
        elif (((evaluatedbox.line == motherbox.line) or (evaluatedbox.column == motherbox.column)) and ((motherbox.g + 10 < evaluatedbox.g) or (evaluatedbox.type == Type.EMPTY) or (evaluatedbox.type == Type.END))):
            gCost = motherbox.g + 10
        elif ((not(evaluatedbox.line == motherbox.line or evaluatedbox.column == motherbox.column)) and ((motherbox.g + 14 < evaluatedbox.g) or (evaluatedbox.type == Type.EMPTY or evaluatedbox.type == Type.END))):
            gCost = motherbox.g + 14
        else:
            gCost = evaluatedbox.g
        return gCost

    """ calculating_h_cost function : 
    brief : Calculate the H cost of the box which need to be evaluated
    param : 
    - evaluatedbox : the box which need to be evaluated
    return hCost : the H cost of the evaluated box
    """
    def calculating_h_cost(self, evaluatedbox):

        if (evaluatedbox.line == self.end.line):
            hCost = fabs(evaluatedbox.column-self.end.column)*10

        if (evaluatedbox.column == self.end.column):
            hCost = fabs(evaluatedbox.line-self.end.line)*10

        else:
            hCost = min(fabs(evaluatedbox.line-self.end.line), fabs(evaluatedbox.column - self.end.column))*14 + (fabs(evaluatedbox.column - self.end.column)-min(fabs(evaluatedbox.column - self.end.column),fabs(evaluatedbox.line-self.end.line)))*10 + (fabs(evaluatedbox.line - self.end.line)-min(fabs(evaluatedbox.column - self.end.column),fabs(evaluatedbox.line-self.end.line)))*10
        return hCost

    """ calculating_f_cost function : 
    brief : Calculate the F cost of the current box
    param : 
    - current : the current box which need to be evaluated
    return the F cost (G cost + H cost)
    """
    def calculating_f_cost(self, current):    
        return current.g + current.h

    """ evaluate function : 
    brief : evaluate current box costs and add the best neighbour in the list of boxes to evaluate next
    param :
    - boxesToEvaluate : the list of boxes which need to be evaluated next
    - current : the current box to evaluate
    """
    def evaluate(self, boxesToEvaluate, current):
        for line in (-1, 0, 1):
            for column in (-1, 0, 1):

                if ((not((line == 0) and (column == 0)) and (current.column + column < self.columns) and (current.line + line < self.lines) and (current.column + column >= 0) and (current.line + line >= 0))):

                    self.table[current.line+line][current.column+column].g = self.calculating_g_cost(self.table[current.line+line][current.column+column], current)
                    self.table[current.line+line][current.column+column].h = self.calculating_h_cost(self.table[current.line+line][current.column+column])
                    self.table[current.line+line][current.column+column].f = self.calculating_f_cost(self.table[current.line+line][current.column+column])

                    if (self.table[current.line+line][current.column+column].type == Type.EMPTY):
                        boxesToEvaluate.append(self.table[current.line+line][current.column+column])
                        self.table[current.line+line][current.column+column].type = Type.NON_EVALUATED
                    elif (self.table[current.line+line][current.column+column].type == Type.END):
                        boxesToEvaluate.append(self.table[current.line+line][current.column+column])

    """ display function : 
    brief : display the map on the window
    param : none 
    """
    def display(self):

        for line in range(self.lines):
            for column in range(self.columns):
                if (self.table[line][column].type == Type.EMPTY):
                    self.screen.blit(self.image.empty, self.tableRect[line][column])
                elif (self.table[line][column].type == Type.WALL):
                    self.screen.blit(self.image.wall, self.tableRect[line][column])
                elif (self.table[line][column].type == Type.START):
                    self.screen.blit(self.image.start, self.tableRect[line][column])
                elif (self.table[line][column].type == Type.END):
                    self.screen.blit(self.image.end, self.tableRect[line][column])
                elif (self.table[line][column].type == Type.EVALUATED):
                    self.screen.blit(self.image.evaluated, self.tableRect[line][column])
                elif (self.table[line][column].type == Type.NON_EVALUATED):
                    self.screen.blit(self.image.nonEvaluated, self.tableRect[line][column])
                elif (self.table[line][column].type == Type.CURRENT):
                    self.screen.blit(self.image.current, self.tableRect[line][column])
                elif (self.table[line][column].type == Type.PATH):
                    self.screen.blit(self.image.path, self.tableRect[line][column])
        
        pygame.display.update()
        pygame.time.wait(self.delay)

    """ lowest_f_cost_box_path function : 
    brief : Determine the box with the lowest F cost for the past
    param : 
    - boxesToEvaluate : the boxes which must be evaluate
    return fCostMinNode : the node/box with the lowest F cost
    """
    def lowest_f_cost_box_path(self, boxesToEvaluate):
        fCostMinNodes = []
        fCostMinNode = boxesToEvaluate[0]
        fCostMin = boxesToEvaluate[0].f
        
        if (len(boxesToEvaluate) > 1):
            for index in range(len(boxesToEvaluate)):
                if (boxesToEvaluate[index].f < fCostMin):
                    fCostMin = boxesToEvaluate[index].f

            for index in range(len(boxesToEvaluate)):
                if (boxesToEvaluate[index].f == fCostMin):
                    fCostMinNodes.append(boxesToEvaluate[index])

            gCostMin = fCostMinNodes[0].g
            fCostMinNode = fCostMinNodes[0]

            for index in range(len(fCostMinNodes)):
                if (fCostMinNodes[index].g < gCostMin):
                    gCostMin = fCostMinNodes[index].g
                    fCostMinNode = fCostMinNodes[index]

        return fCostMinNode

    """ get_path function : 
    brief : get the optimized path adding the boxes in the path list
    """
    def get_path(self):
        current = self.table[self.end.line][self.end.column]
        neighbours = []

        while (not(current.type == Type.START)):
            for line in(-1,0,1):
                for column in (-1,0,1):
                    if ((not(line == 0 and column == 0)) and (current.line + line >= 0) and (current.column + column >= 0) and (current.line + line < self.lines) and (current.column + column < self.columns) and (current.type != Type.START)):
                        if (self.table[current.line+line][current.column+column].type == Type.EVALUATED):
                            neighbours.append(self.table[current.line+line][current.column+column])
                        elif (self.table[current.line+line][current.column+column].type == Type.START):
                            current = self.table[current.line+line][current.column+column]
                            neighbours = []

            if (len(neighbours) > 0):
                current = self.lowest_f_cost_box_path(neighbours)
                self.path.append(current)
            neighbours = []

    """ display_path function : 
    brief : display the path on the window
    param : 
    - play : boolean used to pause the game
    """
    def display_path(self, play):
        update = False
        
        for index in range(len(self.path)):
            update = False
            while(not(update)):
                play = self.get_event(play)

                if (play):
                    self.path[len(self.path)-index-1].type = Type.PATH
                    self.display()
                    update = True

    """ run function : 
    brief : run the algorithm program and display the solving process and the final path if the map can be solved
    param : none
    """
    def run(self):

        boxesToEvaluate = []
        boxesEvaluated = []
        current = self.table[self.start.line][self.start.column]
        pathFound = False
        impossiblePathfinding = False
        clock = pygame.time.Clock()
        play = True

        boxesToEvaluate.append(self.table[self.start.line][self.start.column]) # Adding the start box in the tab of boxes to evaluate

        self.display()

        while True:
            clock.tick(self.FPS)

            for event in pygame.event.get():
                if (event.type == pygame.QUIT):
                    quit()

                if (event.type == pygame.KEYDOWN):
                    if (event.key == pygame.K_ESCAPE):
                        quit()

                    if (event.key == pygame.K_SPACE):

                        while (not(pathFound or impossiblePathfinding)):
                            play = self.get_event(play)

                            if (play):

                                if (len(boxesToEvaluate) == 0):
                                    print("Pathfinding impossible to solve")
                                    impossiblePathfinding = True
                                    current.type = Type.EVALUATED

                                else :

                                    current = self.lowest_f_cost_box(boxesToEvaluate)
                                    del boxesToEvaluate[self.lowest_f_cost_box_index(boxesToEvaluate)]
                                    boxesEvaluated.append(current)

                                    if ((current.type != Type.START) and (current.type != Type.END)):
                                        current.type = Type.CURRENT

                                    if (not(pathFound)):
                                        self.evaluate(boxesToEvaluate, current)

                                    if ((current.type != Type.START) and (current.type != Type.END)):
                                        current.type = Type.EVALUATED

                                    if (current.type == Type.END):
                                        pathFound = True
                                        self.get_path()
                                        print("A path has been found !")
                                        self.display_path(play)                                    
                                                            
                                self.display()
        
def main():
    pathfinding = Pathfinding(1920,1080,100,50)
    pathfinding.init_map()
    pathfinding.init_display()
    pathfinding.run()

if __name__ == "__main__":
    main()