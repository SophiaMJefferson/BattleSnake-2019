import os
import random
import methods as m
import findmoves as f
import cherrypy

prevmove = "left" #initialize to something random

class Battlesnake(object):
    @cherrypy.expose
    @cherrypy.tools.json_out()
    def index(self):
        return {
            "apiversion": "1",
            "author": "sophiajay",  
            "color": "#64CCCD", 
            "head": "bwc-scarf", 
            "tail": "sharp",  
        }

    @cherrypy.expose
    @cherrypy.tools.json_in()
    def start(self):
        # This function is called everytime your snake is entered into a game.

        print("START")
        return "ok"

    #this function is called every move
    @cherrypy.expose
    @cherrypy.tools.json_in()
    @cherrypy.tools.json_out()
    def move(self):
        #get from data
        data = cherrypy.request.json

        height = m.height(data)
        width = m.width(data)
        health = data["you"]["health"] #my health value
        length = len(data["you"]["body"])#my length
        #x, y coords of head
        x = data["you"]["head"]["x"] 
        y = data["you"]["head"]['y']
        
        #initialize variables
        move = ""
        ATmove = ""
        subparmove = set([]) 
        all_moves = set(["up", "down", "left", "right"])
        nomove = set([])
        move_coords = { #dict of where moves will place head
            "up": [x, y + 1],
            "down": [x, y - 1],
            "left": [x - 1, y],
            "right": [x + 1, y]
        }

        #updates nomove to inlcude backwards, bodies, walls
        global prevmove
        nomove = f.no_back(nomove,prevmove)
        nomove = f.no_bodies(nomove,data,move_coords)
        nomove = f.no_walls(nomove,data,x,y)

        #avoid food when full, add food to nomove
        if health>100:
          for i in m.food_coords(data):
            for key in move_coords:
              if move_coords[key]==i:
                if len(nomove)<3:
                  subparmove.add(key)


  
        #Add eat zones(adj to head) to nomove
        snakes = m.get_snakes(data)
        for s in range (0,len(snakes)):
          i = snakes[s]["head"]
          eat_coords = [[i["x"]+1,i["y"]],[i["x"]-1,i["y"]],[i["x"],i["y"]+1],[i["x"],i["y"]-1]]
          for j in eat_coords:
            for key in move_coords:
                if move_coords[key] == j:
                    if snakes[s]["length"]>=length:
                      subparmove.add(key)
                    else: #if I am bigger, try to eat
                      ATmove = key


        #move priority processing
        #ATMOVE, PREVMOVE,NOTSUBPAR,possible
        if (ATmove not in subparmove) and (ATmove not in nomove) and (ATmove != ""):
          move = ATmove #eating move if not subpar
        elif (prevmove not in subparmove) and (prevmove not in nomove): 
          move = prevmove #continue straight if not subpar
        elif len((all_moves-nomove)-subparmove)>0:
          #choose from good moves if not empty
          move = random.choice(list((all_moves-nomove)-subparmove))
        else:
          #choose from possible moves
          move = random.choice(list(all_moves - nomove))


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
