import methods as m


#node class for each square of board
class Node():
    """A node class for A* Pathfinding"""

    def __init__(self, parent=None, position=None):
        self.parent = parent
        self.position = position

        self.g = 0
        self.h = 0
        self.f = 0

    def __eq__(self, other):
        return self.position == other.position

#pathfind from start(head) to end
def astar(maze, start, end):
    #initializes start and end nodes
    start_node = Node(None, start)
    start_node.g = start_node.h = start_node.f = 0
    end_node = Node(None, end)
    end_node.g = end_node.h = end_node.f = 0

    #initializes openlist and closedlist
    open_list = []
    closed_list = []

    # Add the start node
    open_list.append(start_node)

    # Loop until you find the end of openlist
    while len(open_list) > 0:
        # Get the current node, begins at start node
        current_node = open_list[0]
        current_index = 0
        #for item in openlist, if better f, make current node = item
        for index, item in enumerate(open_list):
            if item.f < current_node.f:
                current_node = item
                current_index = index
        
        # Pop current off open list, add to closed list
        open_list.pop(current_index)
        closed_list.append(current_node)

        #If found the goal, return reversed path
        if current_node == end_node:
            path = []
            current = current_node
            while current is not None:
                path.append(current.position)
                current = current.parent
            return path[::-1] # Return reversed path

        # Generate children of current node (adjacent nodes)
        children = []
        for new_position in [(0, -1), (0, 1), (-1, 0), (1, 0)]:#adj squares 
            # Get node position
            node_position = (current_node.position[0] + new_position[0], current_node.position[1] + new_position[1])
            # Make sure within range
            if node_position[0] > (len(maze) - 1) or node_position[0] < 0 or node_position[1] > (len(maze[len(maze)-1]) -1) or node_position[1] < 0:
                continue
            # Make sure walkable terrain
            if maze[node_position[0]][node_position[1]] != 0:
                continue
            # Create new node
            new_node = Node(current_node, node_position)
            # Append
            children.append(new_node)

            # Loop through children (ignore or add to openlist)
        for child in children:
            """
            # Child is on the closed list
            for closed_child in closed_list:
                if child == closed_child:
                    continue
            """

            # Create the f, g, and h values for children not already in closed list
            if child not in closed_list:
              child.g = current_node.g + 1
              child.h = ((child.position[0] - end_node.position[0]) ** 2) + ((child.position[1] - end_node.position[1]) ** 2)
              child.f = child.g + child.h

            """
            # Child is already in the open list
            for open_node in open_list:
                if child == open_node and child.g > open_node.g:
                    continue
            """
            #add to openlist if in openlist and has smaller g value than twin (or not in list)
            good_nodes = []
            for open_node in open_list:
                if child == open_node and child.g <= open_node.g:
                  good_nodes.append(open_node)

            # Add the child to the open list
            if child not in open_list or child in good_nodes:
              open_list.append(child)


#makes a "maze" to use astar on using board data
def make_maze(data):
  maze = []
  obstruct = m.body_coords(data)
  #iterate through columns in first row
  for r in range(0,11):
    row = []
    for y in range(0,11):
      if obstruct[1] == y: #if this coord is obstructed
        row.append(0)
      else:
        row.append(1)
    maze.append(row)
  return maze





"""       
def main():

    #zeros are unwalkable terrain (body_coords), each "row" is a row of the board

    maze = [[0, 0, 0, 0, 1, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 1, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 1, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 1, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 1, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 1, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 1, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 1, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0, 0, 0]]

    start = (0, 0)
    end = (7, 6)

    path = astar(maze, start, end)
    print(path)


if __name__ == '__main__':
    main()
"""
