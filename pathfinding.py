import pygame
import enum
from math import *
from random import *

class Box_type(enum.Enum):
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
        self.type = Box_type.EMPTY

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
        self.start.type = Box_type.START
        self.end.type = Box_type.END
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
        # Set lins and columns attributes
        self.lines = lines
        self.columns = columns

        # Case 1 : the ratio (max width / columns) is smaller than the ratio (max height / lines)
        if ((maxWidth/self.columns < maxHeight/self.lines)):
            self._width = int((maxWidth/self.columns))*self.columns
            self._height = int((((min((maxWidth/self.columns), (maxHeight/self.lines)) / max((maxWidth/self.columns), (maxHeight/self.lines))) * maxHeight)/self.lines))*self.lines

        # Case 2 : the ratio (max width / columns) is bigger than the ratio (max height / lines)
        else:
            self._width = int((((min((maxWidth/self.columns), (maxHeight/self.lines)) / max((maxWidth/self.columns), (maxHeight/self.lines))) * maxWidth)/self.columns))*self.columns
            self._height = int((maxHeight/self.lines))*self.lines

        # Initialyse pygame display
        self.screen = pygame.display.set_mode((self._width, self._height))
        self.screen.fill((0, 0, 0))

        # Initialyse the map and the image to blit on screen
        self.table = [[box() for column in range(self.columns)] for line in range(self.lines)]
        self.image = Image(self._width/self.columns, self._height/self.lines)

    """ init_map function : 
    brief : initialize and generate the map with the variables used for the map.
    The map is generated randomly with empty boxes, walls and a start and end box
    param : none
    """
    def init_map(self):

        # Go through the map to initialize each box
        for line in range(self.lines):
            for column in range(self.columns):
                # Set the type of the box randomly
                self.table[line][column].type = Box_type.WALL if (randint(0,1) == 1) else Box_type.EMPTY
                # Set the position of each box
                (self.table[line][column].line, self.table[line][column].column) = (line,column)

        # Randomly set the position of both the start and the end boxes
        self.start.line = randint(0,self.lines-1)
        self.start.column = randint(0,self.columns-1)
        
        self.end.line = randint(0,self.lines-1)
        self.end.column = randint(0,self.columns-1)

        # Ensure that the position of the end box is different from the position of the start box
        while ((self.end.line ==  self.start.line) and (self.end.column ==  self.start.column)):
            self.end.line = randint(0,self.lines-1)
            self.end.column = randint(0,self.columns-1)
        
        # Set both the start and the end boxes type
        self.table[self.start.line][self.start.column].type = Box_type.START
        self.table[self.end.line][self.end.column].type = Box_type.END

    """ init_display function : 
    brief : init the table of rectangles used to blit the images on
    param : none 
    """
    def init_display(self):

        # Initialize the size of the matrix of rectangles
        self.tableRect = [[pygame.Rect((column*self._width/self.columns, line*self._height/self.lines), (self._width/self.columns, self._height/self.lines)) for column in range(self.columns)] for line in range(self.lines)]
        
        # Go through the table of rectangles
        for line in range(self.lines):
            for column in range(self.columns):
                # Initialize the position and the size of each rectangle
                self.tableRect[line][column] = pygame.Rect(((column*self._width/self.columns), (line*self._height/self.lines)), ((self._width/self.columns),(self._height/self.lines)))

    """ get_event function : 
    brief : get the event using pygame library to close the window and update the variable used to pause the program
    param :
    - play : the boolean used to pause the program
    """
    def get_event(self, play):

        # Look for user actions
        for event in pygame.event.get():

            # Quit the program if the user close the window
            if (event.type == pygame.QUIT):
                quit()

            # Look for keydown actions
            if (event.type == pygame.KEYDOWN):

                # Close the program if the escape key is pressed
                if (event.key == pygame.K_ESCAPE):
                    quit()

                # Pause or unpause the program if the space bar key is pressed
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
        
        # Ensure that the list of boxes to evaluate is not empty
        if (len(boxesToEvaluate) >= 1):
            # Get the box with the lowest f cost
            for index in range(len(boxesToEvaluate)):
                if (boxesToEvaluate[index].f < fCostMin):
                    fCostMin = boxesToEvaluate[index].f

            # Add the boxes with the lowest f cost to the list of the box with the lowest f cost
            for index in range(len(boxesToEvaluate)):
                if (boxesToEvaluate[index].f == fCostMin):
                    fCostMinNodes.append(boxesToEvaluate[index])

            hCostMin = fCostMinNodes[0].h
            fCostMinNode = fCostMinNodes[0]

            # Get the box with the lowest h cost among the boxes with the lowest f cost
            for index in range(len(fCostMinNodes)):
                if (fCostMinNodes[index].h < hCostMin):
                    hCostMin = fCostMinNodes[index].h
                    fCostMinNode = fCostMinNodes[index]

        return fCostMinNode # return the box with the lowest f cost (+ lowest h cost)

    """ lowest_f_cost_box_index function : 
    brief : Determine the index of the box with the lowest F cost
    param : 
    - boxesToEvaluate : the list of boxes which need to be evaluated
    return lowest_f_cost_box_index : the index of the box with the lowest F cost
    """
    def lowest_f_cost_box_index(self, boxesToEvaluate):

        # Get the box with the lowest f cost
        box = self.lowest_f_cost_box(boxesToEvaluate)
        lowest_f_cost_box_index = 0

        # Go through the list of boxes to evaluate to get the index of the box with the lowest f cost
        for index in range(len(boxesToEvaluate)):
            if ((boxesToEvaluate[index].line == box.line) and (boxesToEvaluate[index].column == box.column)):
                lowest_f_cost_box_index = index
    
        return lowest_f_cost_box_index # return the index of the box with the lowest f cost

    """ calculating_g_cost function : 
    brief : Calculate the G cost of the box which need to be evaluated thanks to its mother box
    param : 
    - evaluatedbox : the box which need to be evaluated
    - motherbox : the mother box of the box which need to be evaluated
    return gCost : the G cost of the evaluated box
    """
    def calculating_g_cost(self, evaluatedBox, motherbox):

        # Case 1 : the mother box is the start box
        if motherbox.type == Box_type.START:
            # If the evaluated box (empty or end box) is in the same line or column that the mother box
            if ((evaluatedBox.line == motherbox.line) or (evaluatedBox.column == motherbox.column) and ((evaluatedBox.type == Box_type.EMPTY) or (evaluatedBox.type == Box_type.END))):
                gCost = 10
            # If the evaluated box (empty or end box) is situated in a diagonal of the mother box
            else:
                gCost = 14

        # Case 2 : the mother box isn't the mother box
        # If the evaluated box (empty or end box) is in the same line or column that the mother box and (mother box g cost + move cost < evaluated box g cost)
        elif (((evaluatedBox.line == motherbox.line) or (evaluatedBox.column == motherbox.column)) and ((motherbox.g + 10 < evaluatedBox.g) or (evaluatedBox.type == Box_type.EMPTY) or (evaluatedBox.type == Box_type.END))):
            gCost = motherbox.g + 10

        # If the evaluated box (empty or end box) is situated in a diagonal of the mother box and (mother box g cost + move cost < evaluated box g cost)
        elif ((not(evaluatedBox.line == motherbox.line or evaluatedBox.column == motherbox.column)) and ((motherbox.g + 14 < evaluatedBox.g) or (evaluatedBox.type == Box_type.EMPTY or evaluatedBox.type == Box_type.END))):
            gCost = motherbox.g + 14
        
        # (mother box g cost + move cost >= evaluated box g cost)
        else:
            gCost = evaluatedBox.g

        return gCost # return the g cost of the evaluated box

    """ calculating_h_cost function : 
    brief : Calculate the H cost of the box which need to be evaluated
    param : 
    - evaluatedbox : the box which need to be evaluated
    return hCost : the H cost of the evaluated box
    """
    def calculating_h_cost(self, evaluatedbox):

        # Case 1 : the evaluated box is situated on the same line that the end box
        if (evaluatedbox.line == self.end.line):
            hCost = fabs(evaluatedbox.column-self.end.column)*10

        # Case 2 : the evaluated box is situated on the same column that the end box
        if (evaluatedbox.column == self.end.column):
            hCost = fabs(evaluatedbox.line-self.end.line)*10

        # Case 3 : the evaluated box is situated on both different line and column that the end box
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
        # f cost = g cost + h cost
        return current.g + current.h

    """ evaluate function : 
    brief : evaluate current box costs and add the best neighbour in the list of boxes to evaluate next
    param :
    - boxesToEvaluate : the list of boxes which need to be evaluated next
    - current : the current box to evaluate
    """
    def evaluate(self, boxesToEvaluate, current):

        # Look for  the neighbour of the current box
        for line in (-1, 0, 1):
            for column in (-1, 0, 1):

                # Ensure that the neighbour isn't the current box and is situated on the map
                if ((not((line == 0) and (column == 0)) and (current.column + column < self.columns) and (current.line + line < self.lines) and (current.column + column >= 0) and (current.line + line >= 0))):

                    # Calculate the current box costs
                    self.table[current.line+line][current.column+column].g = self.calculating_g_cost(self.table[current.line+line][current.column+column], current)
                    self.table[current.line+line][current.column+column].h = self.calculating_h_cost(self.table[current.line+line][current.column+column])
                    self.table[current.line+line][current.column+column].f = self.calculating_f_cost(self.table[current.line+line][current.column+column])

                    # Add the neighbour to the list of boxes to evaluate and set its type to NON_EVALUATED if the neighbour is an EMPTY box
                    if (self.table[current.line+line][current.column+column].type == Box_type.EMPTY):
                        boxesToEvaluate.append(self.table[current.line+line][current.column+column])
                        self.table[current.line+line][current.column+column].type = Box_type.NON_EVALUATED

                    # Only add the neighbour to the list of boxes to evaluate if it's the end box
                    elif (self.table[current.line+line][current.column+column].type == Box_type.END):
                        boxesToEvaluate.append(self.table[current.line+line][current.column+column])

    """ display function : 
    brief : display the map on the window
    param : none 
    """
    def display(self):

        # Go through the map
        for line in range(self.lines):
            for column in range(self.columns):
                
                # Blit the image corresponding to the type of the box
                if (self.table[line][column].type == Box_type.EMPTY):
                    self.screen.blit(self.image.empty, self.tableRect[line][column])
                elif (self.table[line][column].type == Box_type.WALL):
                    self.screen.blit(self.image.wall, self.tableRect[line][column])
                elif (self.table[line][column].type == Box_type.START):
                    self.screen.blit(self.image.start, self.tableRect[line][column])
                elif (self.table[line][column].type == Box_type.END):
                    self.screen.blit(self.image.end, self.tableRect[line][column])
                elif (self.table[line][column].type == Box_type.EVALUATED):
                    self.screen.blit(self.image.evaluated, self.tableRect[line][column])
                elif (self.table[line][column].type == Box_type.NON_EVALUATED):
                    self.screen.blit(self.image.nonEvaluated, self.tableRect[line][column])
                elif (self.table[line][column].type == Box_type.CURRENT):
                    self.screen.blit(self.image.current, self.tableRect[line][column])
                elif (self.table[line][column].type == Box_type.PATH):
                    self.screen.blit(self.image.path, self.tableRect[line][column])
        
        pygame.display.update()
        pygame.time.wait(self.delay) # Add a delay

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
        
        # Ensure that the list of boxes to evaluate is not empty
        if (len(boxesToEvaluate) >= 1):
            # Get the box with the lowest f cost
            for index in range(len(boxesToEvaluate)):
                if (boxesToEvaluate[index].f < fCostMin):
                    fCostMin = boxesToEvaluate[index].f

            # Add the boxes with the lowest f cost to the list of the box with the lowest f cost
            for index in range(len(boxesToEvaluate)):
                if (boxesToEvaluate[index].f == fCostMin):
                    fCostMinNodes.append(boxesToEvaluate[index])

            gCostMin = fCostMinNodes[0].g
            fCostMinNode = fCostMinNodes[0]

            # Get the box with the lowest g cost among the boxes with the lowest f cost
            for index in range(len(fCostMinNodes)):
                if (fCostMinNodes[index].g < gCostMin):
                    gCostMin = fCostMinNodes[index].g
                    fCostMinNode = fCostMinNodes[index]

        return fCostMinNode # return the box with the lowest f cost (+ lowest g cost)

    """ get_path function : 
    brief : get the optimized path adding the boxes in the path list
    """
    def get_path(self):
        # Start from the end box
        current = self.table[self.end.line][self.end.column]
        neighbours = []

        # Run the loop until we are in the tart box
        while (not(current.type == Box_type.START)):

            # Look for the neighbour of the current box
            for line in(-1,0,1):
                for column in (-1,0,1):

                    # Ensure that the neighbour isn't both the current or the start box and is situated on the map
                    if ((not(line == 0 and column == 0)) and (current.line + line >= 0) and (current.column + column >= 0) and (current.line + line < self.lines) and (current.column + column < self.columns) and (current.type != Box_type.START)):

                        # Add the neighbour to the list of neighbours if it is an evaluated box
                        if (self.table[current.line+line][current.column+column].type == Box_type.EVALUATED):
                            neighbours.append(self.table[current.line+line][current.column+column])

                        # The start box becomes the current box if the neighbour is the start box and empty the list of neighbours
                        elif (self.table[current.line+line][current.column+column].type == Box_type.START):
                            current = self.table[current.line+line][current.column+column]
                            neighbours = []

            # Ensure that the list of neighbours isn't empty (the current box isn't the start box)
            if (len(neighbours) > 0):
                # The neighbour with the lowest f cost becomes the current box
                current = self.lowest_f_cost_box_path(neighbours)
                # Add the current box to the path
                self.path.append(current)

            # Empty the list of neighbours before the next iteration
            neighbours = []

    """ display_path function : 
    brief : display the path on the window
    param : 
    - play : boolean used to pause the game
    """
    def display_path(self, play):
        update = False
        
        # Go through the boxes of the path
        for index in range(len(self.path)):
            
            update = False

            # Stay in the loop while the program is paused
            while(not(update)):

                # Get the user actions
                play = self.get_event(play)

                # If the program isn't paused
                if (play):
                    # Set the type of the current box to PATH
                    self.path[len(self.path)-index-1].type = Box_type.PATH

                    # Display the map with the new part of the path added
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
            
            # Look for the user actions
            for event in pygame.event.get():

                # Quit the program if the user close the window
                if (event.type == pygame.QUIT):
                    quit()

                # Look for the keyboard keys pressed
                if (event.type == pygame.KEYDOWN):

                    # Quit the program if the escape key is pressed
                    if (event.key == pygame.K_ESCAPE):
                        quit()

                    # Start the program if the space bar key is pressed
                    if (event.key == pygame.K_SPACE):

                        while (not(pathFound or impossiblePathfinding)):
                            play = self.get_event(play)

                            if (play):

                                # The list of boxes to evaluate is empty means that there isn't any possible path
                                if (len(boxesToEvaluate) == 0):
                                    print("Pathfinding impossible to solve")
                                    impossiblePathfinding = True
                                    current.type = Box_type.EVALUATED

                                else :
                                    
                                    # Get the box with the lowest f cost among the boxes to evaluate
                                    current = self.lowest_f_cost_box(boxesToEvaluate)

                                    # Delete the current box from the list of boxes with the lowest f cost
                                    del boxesToEvaluate[self.lowest_f_cost_box_index(boxesToEvaluate)]

                                    # Add the current box to the list of evaluated boxes
                                    boxesEvaluated.append(current)

                                    # Set the type of the current box to CURRENT if the current box isn't the start box neither the end box
                                    if ((current.type != Box_type.START) and (current.type != Box_type.END)):
                                        current.type = Box_type.CURRENT

                                    # If there is still no path found
                                    if (not(pathFound)):
                                        # Evaluate the current box and update the list of boxes to evaluate
                                        self.evaluate(boxesToEvaluate, current)

                                    # Set the type of the current box to EVALUATED if the current box isn't th start box neither the end box
                                    if ((current.type != Box_type.START) and (current.type != Box_type.END)):
                                        current.type = Box_type.EVALUATED

                                    # If the pathfinding algorithm reached the end box, get the path and display it
                                    if (current.type == Box_type.END):
                                        pathFound = True
                                        self.get_path()
                                        print("A path has been found !")
                                        self.display_path(play)                                    
                                                            
                                self.display()

pathfinding = Pathfinding(1920, 1080, 100, 50)