__author__ = 'admin'
__author__ = 'admin'
from math import *
import random
import queue
import copy
from MoveStruct import *
from UFSET import *
import time
class GameState:
    """ A state of the game, i.e. the game board. These are the only functions which are
        absolutely necessary to implement UCT in any 2-player complete information deterministic
        zero-sum game, although they can be enhanced and made quicker, for example by using a
        GetRandomMove() function to generate a random move during rollout.
        By convention the players are numbered 1 and 2.
    """
    def __init__(self):
            self.playerJustMoved = 2 # At the root pretend the player just moved is player 2 - player 1 has the first move

    def Clone(self):
        """ Create a deep clone of this game state.
        """
        st = GameState()
        st.playerJustMoved = self.playerJustMoved
        return st

    def DoMove(self, move):
        """ Update a state by carrying out the given move.
            Must update playerJustMoved.
        """
        self.playerJustMoved = 3 - self.playerJustMoved

    def GetMoves(self):
        """ Get all possible moves from this state.
        """

    def GetResult(self, playerjm):
        """ Get the game result from the viewpoint of playerjm.
        """

    def __repr__(self):
        """ Don't need this - but good style.
        """
        pass

"""
Definition of the GoState

A board of 19*19 intersections

0 represent empty
1 represent a black stone-black player
2 represent a white stone-white player


"""


class GoState:
    def __init__(self, size):
        self.playerJustMoved = 2 # At the root pretend the player just moved is p2 - p1 has the first move
        self.board = [[NodeUF() for x in range(size)] for x in range(size)]
        self.moves=Mpos()
        for i in range(size):
            for j in range(size) :
                self.board[i][j].x=i
                self.board[i][j].y=j
                self.moves.insert((i,j))
        self.points1 = 0
        self.points2 = 0
        self.size = size
        self.lastpass= False
        self.komove=[]
        #KOMI TODO

    def Clone(self):
        """ Create a deep clone of this game state.
        """
        st = GoState(self.size)
        st.board=copy.deepcopy(self.board [:])
        st.playerJustMoved = self.playerJustMoved
        st.points1=self.points1
        st.points2=self.points2
        st.size=self.size
        st.lastpass=self.lastpass
        st.komove=self.komove
        return st

    def DoMove(self,move):
        if move[0]==-1 and move[1]==-1:
            self.playerJustMoved= 3 - self.playerJustMoved
            self.lastboard=self.board
            self.lastpass=True
        else:
            self.lastpass=False
            first=True
            (x,y)=(move[0],move[1])
            self.board[x][y].color = 3 - self.playerJustMoved

            #set liberties of the stone alone
            if x>0:
                if(self.board[x-1][y].color==0):
                    self.board[x][y].liberty.add(self.board[x-1][y])

            if y>0:
                if(self.board[x][y-1].color==0):
                    self.board[x][y].liberty.add(self.board[x][y-1])

            if x<self.size-1:
                if(self.board[x+1][y].color==0):
                    self.board[x][y].liberty.add(self.board[x+1][y])

            if y <self.size-1:
                if(self.board[x][y+1].color==0):
                    self.board[x][y].liberty.add(self.board[x][y+1])


            #if another stone of the same color, union
            #if another stone of the opposite color , remove lib
            #if 0 lib, remove group
            #if 1 lib, check if playable
            if x>0:
                if(self.board[x-1][y].color==3-self.playerJustMoved):
                    Union(self.board[x][y],self.board[x-1][y])

                    Find(self.board[x][y]).liberty=Find(self.board[x][y]).liberty.difference({self.board[x][y]})


                if(self.board[x-1][y].color==self.playerJustMoved):
                    Find(self.board[x-1][y]).liberty=Find(self.board[x-1][y]).liberty.difference({self.board[x][y]})

                    if len(Find(self.board[x-1][y]).liberty)==0:
                        self.Destroy(x-1,y)




            if y>0:
                if(self.board[x][y-1].color==3-self.playerJustMoved):
                    Union(self.board[x][y],self.board[x][y-1])

                    Find(self.board[x][y]).liberty=Find(self.board[x][y]).liberty.difference({self.board[x][y]})

                if(self.board[x][y-1].color==self.playerJustMoved):

                    Find(self.board[x][y-1]).liberty=Find(self.board[x][y-1]).liberty.difference({self.board[x][y]})

                    if len(Find(self.board[x][y-1]).liberty)==0:
                        self.Destroy(x,y-1)

            if x<self.size-1:
                if(self.board[x+1][y].color==3-self.playerJustMoved):
                    Union(self.board[x][y],self.board[x+1][y])


                    Find(self.board[x][y]).liberty=Find(self.board[x][y]).liberty.difference({self.board[x][y]})

                if(self.board[x+1][y].color==self.playerJustMoved):
                    Find(self.board[x+1][y]).liberty=Find(self.board[x+1][y]).liberty.difference({self.board[x][y]})

                    if len(Find(self.board[x+1][y]).liberty)==0:
                       self.Destroy(x+1,y)


            if y <self.size-1:
                if(self.board[x][y+1].color==3-self.playerJustMoved):
                    Union(self.board[x][y],self.board[x][y+1])

                    Find(self.board[x][y]).liberty=Find(self.board[x][y]).liberty.difference({self.board[x][y]})

                if(self.board[x][y+1].color==self.playerJustMoved):

                   Find(self.board[x][y+1]).liberty=Find(self.board[x][y+1]).liberty.difference({self.board[x][y]})

                   if len(Find(self.board[x][y+1]).liberty)==0:
                        self.Destroy(x,y+1)

            self.playerJustMoved = 3 - self.playerJustMoved

    def Destroy(self,x,y):
        a=Find(self.board[x][y])
        a.children.add(a)
        if len(a.children)==1:
            self.komove.append((x,y))
        if self.playerJustMoved==2:
            self.points1+=len(a.children)
        else:
            self.points2+=len(a.children)
        for i in a.children:

            #attention est ce que ca ne detruit pas la recherche du noeud
            #give the liberties freed to the corresponding groups
            if i.x>0:
                #extend lib
                if  self.board[i.x-1][i.y].color!=0:
                    Find(self.board[i.x-1][i.y]).liberty.add(i)

            if i.y>0:
                if self.board[i.x][i.y-1].color!=0:
                    Find(self.board[i.x][i.y-1]).liberty.add(i)

            if i.x<self.size-1:
                if  self.board[i.x+1][i.y].color!=0:
                    Find(self.board[i.x+1][i.y]).liberty.add(i)


            if i.y <self.size-1:
                if self.board[i.x][i.y+1].color!=0:
                    Find(self.board[i.x][i.y+1]).liberty.add(i)

            i.parent=i
            i.color=0
            i.rank=0
            i.liberty=set()
            i.children=set()


    def Check(self,x,y):
        check=False
        if x>0:
            if self.board[x-1][y].color==0 or (self.board[x-1][y].color==self.playerJustMoved and len(Find(self.board[x-1][y]).liberty)==1) or (self.board[x-1][y].color== 3- self.playerJustMoved and len(Find(self.board[x-1][y]).liberty)>1 ) :
                check= True
        if y>0:
            if self.board[x][y-1].color==0 or (self.board[x][y-1].color==self.playerJustMoved and len(Find(self.board[x][y-1]).liberty)==1) or (self.board[x][y-1].color== 3- self.playerJustMoved and len(Find(self.board[x][y-1]).liberty)>1 ):
                check= True

        if x<self.size-1:
            if self.board[x+1][y].color==0 or (self.board[x+1][y].color==self.playerJustMoved and len(Find(self.board[x+1][y]).liberty)==1) or (self.board[x+1][y].color== 3- self.playerJustMoved and len(Find(self.board[x+1][y]).liberty)>1 ):
                check= True

        if y <self.size-1:
            if self.board[x][y+1].color==0 or(self.board[x][y+1].color==self.playerJustMoved and len(Find(self.board[x][y+1]).liberty)==1) or (self.board[x][y+1].color== 3- self.playerJustMoved and len(Find(self.board[x][y+1]).liberty)>1 ) :
                check= True
        return check


    def GetMoves(self):
        if self.lastpass==True:
            return [(i,j) for i in range(self.size) for j in range(self.size)  if self.board[i][j].color == 0 and self.Check(i,j)]#

        else :
            a =list([(i,j) for i in range(self.size) for j in range(self.size)  if self.board[i][j].color == 0 and self.Check(i,j)])
            a.append((-1,-1))
            if len(self.komove)==1 and self.komove[0] in a:
                a.remove(self.komove[0])
            return a
        #ATTENTION AU KO ! TODO

    def GetWinner(self,player):
        for i in range(self.size):
            for j in range(self.size):
                if self.board[i][j].color==0:
                    if i <1:
                        if self.board[i+1][j].color==1:
                            self.points1+=1
                        else :
                            self.points2+=1
                    else:
                        if self.board[i-1][j].color==1:
                            self.points1+=1
                        else :
                            self.points2+=1
        if (player==1 and self.points1>self.points2) or (player==2 and self.points2>self.points1):
            return 1.0
        else:
            return 0.0

    def GetResult(self,player):
        checked = [[False] * self.size for _ in range(self.size)]
        q = queue.Queue()
        for i in range(self.size):
            for j in range (self.size):
                if(self.board[i][j].color==0 and checked[i][j]==False):
                    q.put((i,j))
                    b=False
                    w=False
                    count=0
                    while (q.empty()==False):
                        #print(q.qsize())
                        #print(self.board)
                        pos=q.get()
                        checked[pos[0]][pos[1]]=True
                        count+=1
                        if(pos[0]>0):
                            if (self.board[pos[0]-1][pos[1]].color==0 and checked[pos[0]-1][pos[1]]==False):
                                #print((pos[0]-1,pos[1]))
                                q.put((pos[0]-1,pos[1]))
                            if (self.board[pos[0]-1][pos[1]].color==1):
                                b=True
                            if (self.board[pos[0]-1][pos[1]].color==2):
                                w=True

                        if(pos[0]<self.size-1):
                            if (self.board[pos[0]+1][pos[1]].color==0 and checked[pos[0]+1][pos[1]]==False ):
                                q.put((pos[0]+1,pos[1]))
                            if (self.board[pos[0]+1][pos[1]].color==1):
                                b=True
                            if (self.board[pos[0]+1][pos[1]].color==2):
                                w=True

                        if(pos[1]>0):
                            if (self.board[pos[0]][pos[1]-1].color==0 and checked[pos[0]][pos[1]-1]==False):
                                q.put((pos[0],pos[1]-1))
                            if (self.board[pos[0]][pos[1]-1].color==1):
                                b=True
                            if (self.board[pos[0]][pos[1]-1].color==2):
                                w=True

                        if(pos[1]<self.size-1):
                            if (self.board[pos[0]][pos[1]+1].color==0 and checked[pos[0]][pos[1]+1]==False):
                                q.put((pos[0],pos[1]+1))
                            if (self.board[pos[0]][pos[1]+1].color==1):
                                b=True
                            if (self.board[pos[0]][pos[1]+1].color==2):
                                w=True

                    if b and not w :
                        self.points1+=count
                    if w and not b:
                        self.points2+=count
                    """if(NOIR ET PAS BLANC):
                        update points noir
                    if(BLANC ET PAS NOIR):
                        update points blanc
                    if(BLANC ET NOIR):
                        Partie pas finie -> DETECTER FIN DE PARTIE ?"""

                    """2eme methode a faire pour une autre representation, voire feuille pq dans celle ci
                    probleme du fait qu'on ne peut jouer un coup perdu, sauf si ca tue"""
        win1= self.points1>self.points2
        if (player==1 and win1) or (player==2 and not win1):
            return 1.0
        else:
            return 0.0

class Node:
    """ A node in the game tree. Note wins is always from the viewpoint of playerJustMoved.
        Crashes if state not specified.
    """
    def __init__(self, move = None, parent = None, state = None):
        self.move = move # the move that got us to this node - "None" for the root node
        self.parentNode = parent # "None" for the root node
        self.childNodes = []
        self.wins = 0
        self.visits = 0
        self.untriedMoves = state.GetMoves() # future child nodes
        self.playerJustMoved = state.playerJustMoved # the only part of the state that the Node needs later

    def UCTSelectChild(self):
        """ Use the UCB1 formula to select a child node. Often a constant UCTK is applied so we have
            lambda c: c.wins/c.visits + UCTK * sqrt(2*log(self.visits)/c.visits to vary the amount of
            exploration versus exploitation.
        """
        s = sorted(self.childNodes, key = lambda c: c.wins/c.visits + sqrt(2*log(self.visits)/c.visits))[-1]
        return s

    def AddChild(self, m, s):
        """ Remove m from untriedMoves and add a new child node for this move.
            Return the added child node
        """
        n = Node(move = m, parent = self, state = s)
        self.untriedMoves.remove(m)
        self.childNodes.append(n)
        return n

    def Update(self, result):
        """ Update this node - one additional visit and result additional wins. result must be from the viewpoint of playerJustmoved.
        """
        self.visits += 1
        self.wins += result

    def __repr__(self):
        return "[M:" + str(self.move) + " W/V:" + str(self.wins) + "/" + str(self.visits) + " U:" + str(self.untriedMoves) + "]"

    def TreeToString(self, indent):
        s = self.IndentString(indent) + str(self)
        for c in self.childNodes:
             s += c.TreeToString(indent+1)
        return s

    def IndentString(self,indent):
        s = "\n"
        for i in range (1,indent+1):
            s += "| "
        return s

    def ChildrenToString(self):
        s = ""
        for c in self.childNodes:
             s += str(c) + "\n"
        return s


def UCT(rootstate, itermax, verbose = False):
    """ Conduct a UCT search for itermax iterations starting from rootstate.
        Return the best move from the rootstate.
        Assumes 2 alternating players (player 1 starts), with game results in the range [0.0, 1.0]."""

    rootnode = Node(state = rootstate)

    for i in range(itermax):
        node = rootnode
        state = rootstate.Clone()


        # Select
        while node.untriedMoves == [] and node.childNodes != []: # node is fully expanded and non-terminal
            node = node.UCTSelectChild()
            state.DoMove(node.move)
            #print("select")
        #print(i,rootstate.board)

        # Expand
        if node.untriedMoves != []: # if we can expand (i.e. state/node is non-terminal)
            m = random.choice(node.untriedMoves)
            state.DoMove(m)
            #print("expand")
            node = node.AddChild(m,state) # add child and descend tree
        #print(i,rootstate.board)

        # Rollout - this can often be made orders of magnitude quicker using a state.GetRandomMove() function
        while state.GetMoves() != []: # while state is non-terminal
            #print("printrollout")
            state.DoMove(random.choice(state.GetMoves()))

        for i in range(state.size):
            for j in range(state.size):
                print(i,j,state.board[i][j].color)
        print(state.playerJustMoved,"playerjustmoved")

        # Backpropagate

        p1=state.GetWinner(1)
        p2=1-p1

        while node != None: # backpropagate from the expanded node and work back to the root node
            #node.Update(state.GetWinner(node.playerJustMoved)) # state is terminal. Update node with result from POV of node.playerJustMoved
            if node.playerJustMoved==2:
                node.Update(p2)
            if node.playerJustMoved==1:
                node.Update(p1)
            #print("backpropagate")
            node = node.parentNode


    # Output some information about the tree - can be omitted
    if (verbose): print (rootnode.TreeToString(0))
    #else: print (rootnode.ChildrenToString())

    return sorted(rootnode.childNodes, key = lambda c: c.visits)[-1].move # return the move that was most visited

def UCTPlayGame():
    """ Play a sample game between two UCT players where each player gets a different number
        of UCT iterations (= simulations = tree nodes).
    """
    state = GoState(3)
    while (state.GetMoves() != []):
        print(str(state))
        if state.playerJustMoved == 1:
            m = UCT(rootstate = state, itermax = 300, verbose = False) # play with values for itermax and verbose = True
        else:
            m = UCT(rootstate = state, itermax = 100, verbose = False)
        print("Best Move: " + str(m) + "\n")
        state.DoMove(m)
        print(state.board)
        for i in range(state.size):
            for j in range(state.size):
                print(i,j,state.board[i][j].color)
    if state.GetResult(state.playerJustMoved) == 1.0:
        print("Player " + str(state.playerJustMoved) + " wins!")
    elif state.GetResult(state.playerJustMoved) == 0.0:
        print ("Player " + str(3 - state.playerJustMoved) + " wins!")
    else: print ("Nobody wins!")

if __name__ == "__main__":
    """ Play a single game to the end using UCT for both players.
"""
    a=GoState(9)
    start = time.time()
    m = UCT(rootstate = a, itermax = 1, verbose = False)
    print(m)
    print(time.time()-start)
    #a.DoMove((1,1))
    #print(len(Find(a.board[0][1]).liberty))



    #a.DoMove((1,0))
    #a.DoMove((0,2))
    #a.DoMove((2,2))


    #a.DoMove((1,1))
    #print(a.board[0][1].color)
    #print(a.board[1][1].liberty)
    #a.playerJustMoved=3-a.playerJustMoved

    #a.komove.append((1,1))
    #print(a.GetMoves())

    #a.points2=0
    #a.board=[[2, 2, 2, 2, 1, 0], [2, 2, 2, 2, 1, 1], [2, 0, 2, 2, 2, 2], [2, 2, 2, 2, 2, 2], [2, 2, 2, 0, 2, 2], [2, 2, 2, 2, 1, 0]]

    #a.lastboard=[[1,0],[0,0]]
    #print(a.CheckNB(1,1))
    #print(a.board)
    #print(a.CheckAliveB(a.board,1,1,2))
    #print(a.GetMoves())
    #print(a.board)
    #a.DoMove((2,1))
    #print(a.board)
    #UCTPlayGame()



    #TODO : COmmunication with GTP /The pass problem : Solution  add a move pass (-1,-1), can be play only when the last mvoe wasn't pass.
    #Solved ?  Problems of posing a stone and remove the deads one/ Not posing a stone where she will die immediately/


