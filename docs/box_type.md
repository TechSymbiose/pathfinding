# **<a name="box_type" />Box_type**

    class Box_type(enum.Enum):

Type class defines an enumerated type for boxes of a map :

Type | Meaning 
--- | ---
EMPTY | empty box where we pass through 
WALL | A wall where we can't pass through 
START | the start of the pathfinding map
END | the end of the pathfinding map
EVALUATED | the different values are calculated
NON_EVALUATED | the Box is located next to an evaluated Box
PATH | the Box is a part of the path
CURRENT | the current Box which is evaluated