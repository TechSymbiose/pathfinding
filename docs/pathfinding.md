# <a name="pathfinding" />Pathfinding

    class Pathfinding():

**Objective** : generate a 2D map randomly filled with a starting box, an ending box and walls, run a pathfinding algorithm to find the best path between the start and the arrival and display all the process.

Attributes | Meaning
--- | ---
`columns` | number of columns of the map
`lines` | number of lines of the map
`width` | width of the window
`height` | height of the window
`delay` | the delay between 2 iterations of the algorithm
`FPS`| Frame Per Second for displaying
`screen` | pygame window to display the map
`table` | 2D map
`tableRect` | matrix to display images on screen
`image` | image displayed on screen
`start` | starting box
`end` | ending box
`path` | list of boxes used to store the final path

# **Constructor**

    def __init__(self, maxWidth, maxHeight, columns, lines):

Parameter | Use
--- | ---
`maxWidth` | the maximum pixels width of the window
`maxHeight` | the maximum pixels height of the window
`columns` | the number of columns of the map
`lines` | the number of lines of the map

# **Methods**

- [set_window()](#set_window)
- [init_map()](#init_map)
- [init_display](#init_display)
- [get_event()](#get_event)
- [lowest_f_cost_box()](#lowest_f_cost_box)
- [lowest_f_cost_box_index()](#lowest_f_cost_box_index)
- [calculating_g_cost()](#calculating_g_cost)
- [calculating_h_cost](#calculating_h_cost)
- [calculating_f_cost](#calculating_f_cost)
- [evaluate()](#evaluate)
- [display()](#display)
- [lowest_f_cost_box_path](#lowest_f_cost_box_path)
- [get_path](#get_path)
- [display_path()](#display_path)
- [run()](#run)

# <a name="set_window" />set_window()   

**Objective** : set the map and the window caracteristics.

    def set_window(self, maxWidth, maxHeight, columns, lines):

Parameters | Use
--- | ---
`maxWidth` | maximum width of the window
`maxHeight` | maximum height of the window
`columns` | number of columns of the map
`lines` | numer of lines of the map

# <a name="init_map" />init_map()

**Objective** : initialize the map.

    def init_map(self):

*return* : none

# <a name="init_display" />init_display()

**Objective** : initialize the display to display the map.

    def init_display(self):

*return* : none

# <a name="get_event" />get_event()

**Objective** : get the keyboard key pressing and do the correspondant actions.

    def get_event(self, play):

Parameters | Use
--- | ---
`play` | boolean used to pause and unpause the game

*return* : the boolean used to pause and unpause the game.

# <a name="lowest_f_cost_box" />lowest_f_cost_box()

**Objective** : get the box with the lowest f cost.

    def lowest_f_cost_box(self, boxesToEvaluate):

Parameters | Use
--- | ---
`boxesToEvaluate` | the list of boxes to evaluate to determine the box with the lowest f cost

*return* : the box with the lowest f cost.

# <a name="lowest_f_cost_box_index" />lowest_f_cost_box_index()

**Objective** : get the index of the box with the lowest f cost in the list.

    def lowest_f_cost_box_index(self, boxesToEvaluate):

Parameters | Use
--- | ---
`boxesToEvaluate` | the list of boxes to evaluate to determine the box with the lowest f cost

*return* : the index of the box with the lowest f cost.

# <a name="calculating_g_cost" />calculating_g_cost()

**Objective** : calculate the g cost of the box which need to be evaluated.

    def calculating_g_cost(self, evaluatedbox, motherbox):

Parameters | Use
--- | ---
`evaluatedbox` | the box which need to be evaluated
`motherbox` | the mother box of the box which need to be evaluated

*return* : the g cost of the box which need to be evaluated.

# <a name="calculating_h_cost" />calculating_h_cost()

**Objective** : calculate the h cost of the box which need to be evaluated.

    def calculating_h_cost(self, evaluatedbox):

Parameters | Use
`evaluatedbox` | the box which need to be evaluated 

*return* : the h cost of the box which need to be evaluated.

# <a name="get_path" />et_path()

**Objective** : get the best path.

    def run(self):

*return* : none

# <a name="display_path" />display_path()

**Objective** : display the path on the window.

    def run(self):

Parameter | Use
--- | ---
play | boolean used to pause and unpause the game.

*return* : none

# <a name="run" />run()

**Objective** : run the pathfinding algorithm and display the process on screen.

    def run(self):

*return* : none