import methods as m

def no_back(nomove,prevmove):
    nomove.add(m.opp(prevmove))
    return nomove

#avoid bodies, add bodies to nomove, not including tails
def no_bodies(nomove,data,move_coords):
  for i in m.body_coords(data):
    for key in move_coords:
        if move_coords[key] == i:
            nomove.add(key)
  return nomove

#avoid walls, add walls to nomove
def no_walls(nomove,data,x,y):
    if x + 1 == m.width(data) + 1:
        nomove.add("right")
    elif x - 1 == -1:
        nomove.add('left')

    if y + 1 == m.height(data) + 1:
        nomove.add("up")
    elif y - 1 == -1:
        nomove.add('down')
    return nomove