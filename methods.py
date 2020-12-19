
#Returns the opposite of a move
def opp(amove):
    if amove == "right":
        return "left"
    if amove == "left": 
        return "right"
    if amove == "up":
        return "down"
    if amove == "down":
        return "up"

#Given data, makes a list of coordinates of all snakes, not including tails
def body_coords(data):
    coords = []
    boarddict = data["board"]
    snakelist = boarddict["snakes"]
    for j in range(0, len(snakelist)):
        bodylist = snakelist[j]["body"]
        for i in range(0, len(bodylist)-1):
            x = bodylist[i]["x"]
            y = bodylist[i]["y"]
            coords.append([x, y])
    return coords

#given data, makes a list of other snake
def get_snakes(data):
    snakes = []
    boarddict = data["board"]
    snakelist = boarddict["snakes"]
    for j in range(0, len(snakelist)):#do not include my snake
        name = snakelist[j]["name"]
        length = len(snakelist[j]["body"])
        head = snakelist[j]["head"] #in form {'x': 3, 'y': 1}
        if(name!="Twister"):
          snakes.append({"name":name,"length":length,"head":head})
    return snakes

#Returns a list of all food coords
def food_coords(data):
    coords = []
    boarddict = data["board"]
    foodlist = boarddict["food"]
    for i in range(0, len(foodlist)):
        x = foodlist[i]["x"]
        y = foodlist[i]["y"]
        coords.append([x, y])
    return coords

#get board height
def height(data):
  boarddict = data['board'] #coords of board
  return boarddict['height'] - 1

#get board width
def width(data):
  boarddict = data['board'] #coords of board
  return boarddict['width'] - 1