__author__ = 'admin'
from math import *
import random
import queue
import copy

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
        self.board = [[0] * size for _ in range(size)]
        self.lastboard = [[0] * size for _ in range(size)]
        self.points1 = 0
        self.points2 = 6.5
        self.size = size
        #KOMI TODO

    def Clone(self):
        """ Create a deep clone of this game state.
        """
        st = GoState(self.size)
        st.board=copy.deepcopy(self.board [:])
        st.lastboard=copy.deepcopy(self.lastboard [:])
        st.playerJustMoved = self.playerJustMoved
        st.points1=self.points1
        st.points2=self.points2
        st.size=self.size
        return st

    def DoMove(self,move):
        self.lastboard=self.board
        (x,y)=(move[0],move[1])
        self.board[x][y]= 3 - self.playerJustMoved
        #print(self.CheckNB(move[0],move[1]))

        self.board=self.CheckNB(move[0],move[1])
        self.playerJustMoved = 3 - self.playerJustMoved


    def CheckKo(self, x,y):
        st=self.Clone()
        return  self.lastboard!=st.CheckNB(x,y)


    """
    When we play a stone of a color we have to check if there is another stone of the other color in neighbour.
    If yes, checked if it's alive
    """
    def CheckNB(self,x,y):
        st=copy.deepcopy(self.board)
        color= 3-self.playerJustMoved
        st[x][y]=color
        if x>0:
            if(st[x-1][y]==3-color):
                st= self.CheckAlive(st,x-1,y,3-color)
                #print("test")
        if y>0:
            if(st[x][y-1]==3-color):
                st= self.CheckAlive(st,x,y-1,3-color)
                #print("test")


        if x<self.size-1:
            if(st[x+1][y]==3-color):
                st= self.CheckAlive(st,x+1,y,3-color)
                #print("test")

        if y <self.size-1:
            if(st[x][y+1]==3-color):
                st= self.CheckAlive(st,x,y+1,3-color)
                #print("test")
        return st


    """
    Check from a stone of a color all the neighbouring stones and liberties to see if the group of >=1 stone is alive or not
    Do it with a queue to add in the queue all the neighbouring stone of the same color. Stop when the queue is empty( no liberty)
    or when a liberty is found
    return a board updated
    """
    def CheckAlive(self,brd,x,y,color):
        st=brd
        q = queue.Queue()
        checked = [[False] * self.size for _ in range(self.size)]
        q.put((x,y))
        NoLib=True
        while (q.empty()==False and NoLib==True):
            pos=q.get()
            print(pos)
            checked[pos[0]][pos[1]]=True
            if pos[0]>0:
                if (st[pos[0]-1][pos[1]]==0):
                    NoLib=False
                if (st[pos[0]-1][pos[1]]==color and checked[pos[0]-1][pos[1]]==False):
                    q.put((pos[0]-1,pos[1]))

            if pos[0]<self.size-1:
                if (st[pos[0]+1][pos[1]]==0):
                    NoLib=False
                if (st[pos[0]+1][pos[1]]==color and checked[pos[0]+1][pos[1]]==False):
                    q.put((pos[0]+1,pos[1]))
            if pos[1]>0:
                if (st[pos[0]][pos[1]-1]==0):
                    NoLib=False
                if (st[pos[0]][pos[1]-1]==color and checked[pos[0]][pos[1]-1]==False):
                    q.put((pos[0],pos[1]-1))

            if pos[1]<self.size-1:
                if (st[pos[0]][pos[1]+1]==0):
                    NoLib=False
                if (st[pos[0]][pos[1]+1]==color & checked[pos[0]][pos[1]+1]==False):
                    q.put((pos[0],pos[1]+1))
        #If no liberties for the group, we have to remove it from the board
        if(NoLib==True):
            q.put((x,y))
            while (q.empty()==False):
                pos=q.get()
                st[pos[0]][pos[1]]=0
                #Computations of prisonners IF THERE IS NO COMPUTATION OF PRISONNERS IN SCORE LOOK HERE
                if(color==2):
                    self.points1+=1
                else:
                    self.points2+=1
                if pos[0]>0:
                    if (st[pos[0]-1][pos[1]]==color):
                        q.put((pos[0]-1,pos[1]))
                if pos[0]<self.size-1:
                    if (st[pos[0]+1][pos[1]]==color ):
                        q.put((pos[0]+1,pos[1]))
                if pos[1]>0:
                    if (st[pos[0]][pos[1]-1]==color):
                        q.put((pos[0],pos[1]-1))
                if pos[1]<self.size-1:
                    if (st[pos[0]][pos[1]+1]==color ):
                        q.put((pos[0],pos[1]+1))

        return st


    def CheckAliveB(self,brd,x,y,color):
        st=brd
        q = queue.Queue()
        checked = [[False] * self.size for _ in range(self.size)]
        q.put((x,y))
        NoLib=True
        while (q.empty()==False and NoLib==True):
            pos=q.get()
            checked[pos[0]][pos[1]]=True
            if pos[0]>0:
                if (st[pos[0]-1][pos[1]]==0):
                    NoLib=False
                if (st[pos[0]-1][pos[1]]==color and checked[pos[0]-1][pos[1]]==False):
                    q.put((pos[0]-1,pos[1]))

            if pos[0]<self.size-1:
                if (st[pos[0]+1][pos[1]]==0):
                    NoLib=False
                if (st[pos[0]+1][pos[1]]==color and checked[pos[0]+1][pos[1]]==False):
                    q.put((pos[0]+1,pos[1]))
            if pos[1]>0:
                if (st[pos[0]][pos[1]-1]==0):
                    NoLib=False
                if (st[pos[0]][pos[1]-1]==color and checked[pos[0]][pos[1]-1]==False):
                    q.put((pos[0],pos[1]-1))

            if pos[1]<self.size-1:
                if (st[pos[0]][pos[1]+1]==0):
                    NoLib=False
                if (st[pos[0]][pos[1]+1]==color & checked[pos[0]][pos[1]+1]==False):
                    q.put((pos[0],pos[1]+1))
        return NoLib
    def CheckNBB(self,brd,x,y):
        st=brd
        color= 3-self.playerJustMoved
        hasnb=False
        st[x][y]=color
        if x>0:
            if(st[x-1][y]==0):
                hasnb=True
            elif st[x-1][y]==3-color:
                if self.CheckAliveB(st,x-1,y,3-color):
                    hasnb=True



        if y>0:
            if(st[x][y-1]==0):
                hasnb=True
            elif st[x][y-1]==3-color:
                if self.CheckAliveB(st,x,y-1,3-color):
                    hasnb=True


        if x<self.size-1:
            if(st[x+1][y]==0):
                hasnb=True
            elif st[x+1][y]==3-color:
                if self.CheckAliveB(st,x+1,y,3-color):
                    hasnb=True


        if y<self.size-1 :
            if(st[x][y+1]==0):
                hasnb=True
            elif st[x][y+1]==3-color:
                if self.CheckAliveB(st,x,y+1,3-color):
                    hasnb=True
        st[x][y]=0
        return hasnb

    def GetMoves(self):
        #print(self.board)
        #return [(i,i) for i in range(self.size)  if self.board[i][i] == 0]
        st=self.Clone()
        return [(i,j) for i in range(self.size) for j in range(self.size)  if self.board[i][j] == 0 and st.CheckNBB(st.board,i,j) and st.CheckKo(i,j)]# and  not self.CheckNBB(i,j)]
        #ATTENTION AU KO ! TODO

    def GetResult(self,player):
        checked = [[False] * self.size for _ in range(self.size)]
        q = queue.Queue()
        for i in range(self.size):
            for j in range (self.size):
                if(self.board[i][j]==0 & checked[i][j]==False):
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
                            if (self.board[pos[0]-1][pos[1]]==0 and checked[pos[0]-1][pos[1]]==False):
                                #print((pos[0]-1,pos[1]))
                                print(checked[pos[0]-1][pos[1]])
                                q.put((pos[0]-1,pos[1]))
                            if (self.board[pos[0]-1][pos[1]]==1):
                                b=True
                            if (self.board[pos[0]-1][pos[1]]==2):
                                w=True

                        if(pos[0]<self.size-1):
                            if (self.board[pos[0]+1][pos[1]]==0 and checked[pos[0]+1][pos[1]]==False ):
                                q.put((pos[0]+1,pos[1]))
                            if (self.board[pos[0]+1][pos[1]]==1):
                                b=True
                            if (self.board[pos[0]+1][pos[1]]==2):
                                w=True

                        if(pos[1]>0):
                            if (self.board[pos[0]][pos[1]-1]==0 and checked[pos[0]][pos[1]-1]==False):
                                q.put((pos[0],pos[1]-1))
                            if (self.board[pos[0]][pos[1]-1]==1):
                                b=True
                            if (self.board[pos[0]][pos[1]-1]==2):
                                w=True

                        if(pos[1]<self.size-1):
                            if (self.board[pos[0]][pos[1]+1]==0 and checked[pos[0]][pos[1]+1]==False):
                                q.put((pos[0],pos[1]+1))
                            if (self.board[pos[0]][pos[1]+1]==1):
                                b=True
                            if (self.board[pos[0]][pos[1]+1]==2):
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
        if player==1 and win1 | player==2 and not win1:
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
        state.board=[[0, 0, 0, 0], [0, 0, 0, 0], [0, 0, 0, 0], [0, 0, 0, 0]]


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

        # Backpropagate

        while node != None: # backpropagate from the expanded node and work back to the root node
            node.Update(state.GetResult(node.playerJustMoved)) # state is terminal. Update node with result from POV of node.playerJustMoved
            #print("backpropagate")
            node = node.parentNode


    # Output some information about the tree - can be omitted
    if (verbose): print (rootnode.TreeToString(0))
    else: print (rootnode.ChildrenToString())

    return sorted(rootnode.childNodes, key = lambda c: c.visits)[-1].move # return the move that was most visited

def UCTPlayGame():
    """ Play a sample game between two UCT players where each player gets a different number
        of UCT iterations (= simulations = tree nodes).
    """
    #state = OthelloState(4) # uncomment to play Othello on a square board of the given size
    #state = OXOState() # uncomment to play OXO
    #state = NimState(15) # uncomment to play Nim with the given number of starting chips
    state = GoState(4)
    while (state.GetMoves() != []):
        print(str(state))
        if state.playerJustMoved == 1:
            m = UCT(rootstate = state, itermax = 5, verbose = False) # play with values for itermax and verbose = True
        else:
            m = UCT(rootstate = state, itermax = 5, verbose = False)
        print("Best Move: " + str(m) + "\n")
        print(state.board)
        state.DoMove(m)
        #print(state.board)
    if state.GetResult(state.playerJustMoved) == 1.0:
        print("Player " + str(state.playerJustMoved) + " wins!")
    elif state.GetResult(state.playerJustMoved) == 0.0:
        print ("Player " + str(3 - state.playerJustMoved) + " wins!")
    else: print ("Nobody wins!")

if __name__ == "__main__":
    """ Play a single game to the end using UCT for both players.
"""
    a=GoState(2)
    a.board=[[2,2],[2,0]]
    a.lastboard=[[1,0],[0,0]]
    print(a.CheckNB(1,1))
    print(a.board)
    print(a.CheckKo(0,0))
    print(a.board)
    a.DoMove((1,1))
    print(a.board)
    #print(a.CheckNB(1,0))
    print(a.GetMoves())
    #print(a.CheckNBB( a.board,1,1))
    #print(a.board)



    #UCTPlayGame()


    #TODO : COmmunication with GTP /The equal and the changing rootstate/ Ko problem
    #Solved ?  Problems of posing a stone and remove the deads one/ Not posing a stone where she will die immediately/


