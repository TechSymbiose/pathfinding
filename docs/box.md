# <a name="box" />Box

    class Box():

Objective : define a box in a table.

Attributs | Meaning
--- | ---
`g` | the distance G relative to the start box
`h` | the distance H relative to the end box
`f`| the distance F between the start Box and the end box passing throw this box (F = G + H)
`column` | the number of the column of the box
`line` | the number of the line of the box
`type` | the type of the box (START, END, EMPTY, WALL, EVALUATED, NON_EVALUATED, PATH)

## **Constructor**

    def __init__(self):

Initialize each value to 0 and the type of the box to `EMPTY`.