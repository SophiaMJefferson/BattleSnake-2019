import os
import random

import cherrypy

prevmove = "left" #initialize to something random

#for adding dictionaries
def add_dicts(d1,d2):
  d = {"up":0,"down":0,"left":0,"right":0}
  for k in d:
    d[k] = d1[k]+d2[k]
  return d

#for subtracting dictionaries
def subtract_dicts(d1,d2):
  d = {"up":0,"down":0,"left":0,"right":0}
  print(d1,d2,d)
  for k in d:
    d[k] = d1[k]-d2[k]
  return d

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

#Given data, makes a list of coordinates of all snakes
def body_coords(data):
    coords = []
    boarddict = data["board"]
    snakelist = boarddict["snakes"]
    for j in range(0, len(snakelist)):
        bodylist = snakelist[j]["body"]
        for i in range(0, len(bodylist)):
            x = bodylist[i]["x"]
            y = bodylist[i]["y"]
            coords.append([x, y])
    return coords

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

        
class Battlesnake(object):
    @cherrypy.expose
    @cherrypy.tools.json_out()
    def index(self):
        # This function is called when you register your Battlesnake on play.battlesnake.com
        # It controls your Battlesnake appearance and author permissions.
        # TIP: If you open your Battlesnake URL in browser you should see this data
        return {
            "apiversion": "1",
            "author": "",  # TODO: Your Battlesnake Username
            "color": "#64CCCD",  # TODO: Personalize
            "head": "bwc-scarf",  # TODO: Personalize
            "tail": "sharp",  # TODO: Personalize
        }

    @cherrypy.expose
    @cherrypy.tools.json_in()
    def start(self):
        # This function is called everytime your snake is entered into a game.

        print("START")
        return "ok"

    @cherrypy.expose
    @cherrypy.tools.json_in()
    @cherrypy.tools.json_out()
    def move(self):
        # This function is called on every turn of a game. It's how your snake decides where to move.
        data = cherrypy.request.json

        boarddict = data['board'] #coords of board
        height = boarddict['height'] - 1
        width = boarddict['width'] - 1

        youdict = data["you"] #coords of my snake
        headdict = youdict["head"] #coords of my head
        health = youdict["health"] #my health value
        #x, y coords of head
        global x
        global y
        x = headdict["x"] 
        y = headdict['y']

        all_moves = set(["up", "down", "left", "right"])
        #dict of where moves will place head
        move_coords = {
            "up": [x, y + 1],
            "down": [x, y - 1],
            "left": [x - 1, y],
            "right": [x + 1, y]
        }

        nomove = set([])
        #add backwards to nomove dict
        global prevmove
        nomove.add(opp(prevmove))

        #avoid bodies
        for i in body_coords(data):
            for key in move_coords:
                if move_coords[key] == i:
                    nomove.add(key)
        #avoid walls
        if x + 1 == width + 1:
            nomove.add("right")
        elif x - 1 == -1:
            nomove.add('left')

        if y + 1 == height + 1:
            nomove.add("up")
        elif y - 1 == -1:
            nomove.add('down')

        #avoid food when full
        if health>20:
          for i in food_coords(data):
            if move_coords[key]==i:
              if len(nomove)<3:
                nomove.add(key)

        #don't go into a mouth if smaller
        #heads of all snakes
        #sizes of all snakes
        #dont move into square adjacent to snake head if small
        #do if bigger
        
        #randomly pick from possible moves
        move = random.choice(list(all_moves - nomove))

        #go straight forward if possible
        if prevmove not in list(nomove):
            move = prevmove


        print("nomove:", nomove)
        prevmove = move #resets previous move variable
        print(f"MOVE: {move}")
        return {"move": move}

    @cherrypy.expose
    @cherrypy.tools.json_in()
    def end(self):
        # This function is called when a game your snake was in ends.
        data = cherrypy.request.json

        print("END")
        return "ok"


if __name__ == "__main__":
    server = Battlesnake()
    cherrypy.config.update({"server.socket_host": "0.0.0.0"})
    cherrypy.config.update({
        "server.socket_port":
        int(os.environ.get("PORT", "8080")),
    })
    print("Starting Battlesnake Server...")
    cherrypy.quickstart(server)
