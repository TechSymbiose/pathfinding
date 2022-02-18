from pathfinding import *

"""
Here is an example of how to use the pathfinding module
"""

def main():
    pathfinding.set_window(1920,1080,100,50) # Set the window to 1920x1080 px with a map size of 100x50
    pathfinding.init_map() # Initialize the map
    pathfinding.init_display() # Initialiaze the display 
    pathfinding.run() # Run the pathfinding program

if __name__ == "__main__":
    main()