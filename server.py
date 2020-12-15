import os
import random
import methods as m

import cherrypy

prevmove = "left" #initialize to something random

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

#given data, makes a list of other snake (heads,names,health)
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
        move = ""
        ATmove = "" 

        data = cherrypy.request.json
        boarddict = data['board'] #coords of board
        height = boarddict['height'] - 1
        width = boarddict['width'] - 1

        youdict = data["you"] #coords of my snake
        headdict = youdict["head"] #coords of my head
        health = youdict["health"] #my health value
        length = len(youdict["body"])#my length
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
        if health>60:
          for i in food_coords(data):
            if move_coords[key]==i:
              if len(nomove)<3:
                nomove.add(key)

  
        #Do not move into an eat zone(adj to head)
        snakes = get_snakes(data)
        for s in range (0,len(snakes)):
          i = snakes[s]["head"]
          eat_coords = [[i["x"]+1,i["y"]],[i["x"]-1,i["y"]],[i["x"],i["y"]+1],[i["x"],i["y"]-1]]
          for j in eat_coords:
            for key in move_coords:
                if move_coords[key] == j:
                    if snakes[s]["length"]>=length:
                      nomove.add(key)
                    else: #if I am bigger, try to eat
                      ATmove = key

      

        #randomly pick from possible moves
        try:
          move = random.choice(list(all_moves - nomove))
        except IndexError:
          move = prevmove

        #go straight forward if possible
        if prevmove not in list(nomove):
            move = prevmove

        #Eat someone if possible
        if ATmove not in list(nomove):
          if ATmove != "":
            move = ATmove

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
