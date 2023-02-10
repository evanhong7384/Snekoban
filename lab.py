# Snekoban Game

import json
import typing

# NO ADDITIONAL IMPORTS!


direction_vector = {
    "up": (-1, 0),
    "down": (+1, 0),
    "left": (0, -1),
    "right": (0, +1),
}


def new_game(level_description):
    """
    Given a description of a game state, create and return a game
    representation of your choice.

    The given description is a list of lists of lists of strs, representing the
    locations of the objects on the board (as described in the lab writeup).

    For example, a valid level_description is:

    [
        [[], ['wall'], ['computer']],
        [['target', 'player'], ['computer'], ['target']],
    ]

    The exact choice of representation is up to you; but note that what you
    return will be used as input to the other functions.
    """
    
    ObjDict={}
    ObjDict['numRow']=len(level_description)
    ObjDict['numCol']=len(level_description[0])
    ObjDict['wall']=set()
    ObjDict['player']=set()
    ObjDict['computer']=set()
    ObjDict['target']=set()
    for row in range(len(level_description)):
        for col in range(len(level_description[row])):
            if level_description[row][col]:
                for i in range(len(level_description[row][col])):
                    ObjDict[level_description[row][col][i]].add((col,row))
    playerPos=ObjDict['player']
    playerPos=list(playerPos)
    ObjDict['player']=playerPos[0]
    return ObjDict


def victory_check(game):
    """
    Given a game representation (of the form returned from new_game), return
    a Boolean: True if the given game satisfies the victory condition, and
    False otherwise.
    """
    if len(game['target'])!=len(game['computer']):
        return False
    if len(game['target'])==0 or len(game['computer'])==0:
        return False
    for position in game['target']:
        if position not in game['computer']:
            return False
    return True
    


def step_game(game, direction):
    """
    Given a game representation (of the form returned from new_game), return a
    new game representation (of that same form), representing the updated game
    after running one step of the game.  The user's input is given by
    direction, which is one of the following: {'up', 'down', 'left', 'right'}.

    This function should not mutate its input.
    """
    DirectionDict={
        'left':[0,-1],
        'right':[0,1],
        'up':[1,-1],
        'down':[1,1]
    }
    nextGame={
        'numRow':game['numRow'],
        'numCol':game['numCol'],
        'player': game['player'],
        'computer':set(computer for computer in game['computer']),
        'target':set(target for target in game['target']),
        'wall': set(walls for walls in game['wall'])
    }
    
    newPlayerPosition=list(nextGame['player'])
    newPlayerPosition[DirectionDict[direction][0]]+=DirectionDict[direction][1]
    oneMoreMove=newPlayerPosition.copy()
    oneMoreMove[DirectionDict[direction][0]]+=DirectionDict[direction][1]
    oneMoreMove=tuple(oneMoreMove)
    newPlayerPosition=tuple(newPlayerPosition)
    if newPlayerPosition in game['wall']:
        return nextGame
    if newPlayerPosition in game['computer']:
        if oneMoreMove in game['computer'] or oneMoreMove in game['wall']:
            return nextGame
        else:
            nextGame['player']=newPlayerPosition
            nextGame['computer'].remove(newPlayerPosition)
            nextGame['computer'].add(oneMoreMove)
    else:
        nextGame['player']=newPlayerPosition
    return nextGame

def dump_game(game):
    """
    Given a game representation (of the form returned from new_game), convert
    it back into a level description that would be a suitable input to new_game
    (a list of lists of lists of strings).

    This function is used by the GUI and the tests to see what your game
    implementation has done, and it can also serve as a rudimentary way to
    print out the current state of your game for testing and debugging on your
    own.
    """
    level_description=[]
    for row in range(game['numRow']):
        level_description.append([])
        for col in range(game['numCol']):
            level_description[row].append([])
    for walls in game['wall']:
        level_description[walls[1]][walls[0]].append('wall')
    for computer in game['computer']:
        level_description[computer[1]][computer[0]].append('computer')
    for target in game['target']:
        level_description[target[1]][target[0]].append('target')
    player=game['player']
    level_description[player[1]][player[0]].append('player')
    return level_description

def solve_puzzle(game):
    """
    Given a game representation (of the form returned from new game), find a
    solution.

    Return a list of strings representing the shortest sequence of moves ("up",
    "down", "left", and "right") needed to reach the victory condition.

    If the given level cannot be solved, return None.
    """
    
    if len(game['computer'])!=len(game['target']):
        return None
    queue=[game]
    visited={game['player'],tuple(game['computer'])}
    backtrack={}
    found=False
    movementList=['right','left','up','down']
    while queue:
        if victory_check(queue[0]):
            found=True
            break
        for movement in movementList:
            nextMove=step_game(queue[0],movement)
            playerAndCompPos=(nextMove['player'],tuple(nextMove['computer']))
            if playerAndCompPos not in visited:
                queue.append(nextMove)
                visited.add(playerAndCompPos)
                backtrack[playerAndCompPos]=(queue[0]['player'],tuple(queue[0]['computer']))
        queue.pop(0)
        #print(len(queue))
    #print(backtrack)
    if not queue:
        return None
    currentsearch=(queue[0]['player'],tuple(queue[0]['computer']))
    path=[]
    while currentsearch!=(game['player'],tuple(game['computer'])):
        path.insert(0,currentsearch[0])
        #print(currentsearch)
        currentsearch=backtrack[currentsearch]
    path.insert(0,game['player'])
    direction=[]
    for i in range(1,len(path)):
        if path[i][0]!=path[i-1][0]:
            if path[i][0]>path[i-1][0]:
                direction.append('right')
            else:
                direction.append('left')
        else:
            if path[i][1]>path[i-1][1]:
                direction.append('down')
            else:
                direction.append('up')

    return direction
          



if __name__ == "__main__":
    level=[
  [["wall"], ["wall"], ["wall"], ["wall"], [], []],
  [["wall"], [], [], ["wall"], [], []],
  [["wall"], [], [], ["wall"], [], []],
  [["wall"], [], [], ["wall"], ["wall"], ["wall"]],
  [["wall"], ["target"], ["computer"], ["computer"], ["player"], ["wall"]],
  [["wall"], [], [], ["target"], [], ["wall"]],
  [["wall"], [], [], ["wall"], ["wall"], ["wall"]],
  [["wall"], ["wall"], ["wall"], ["wall"], [], []]
]


    game=new_game(level)

    print(solve_puzzle(game))

