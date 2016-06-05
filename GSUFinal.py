__author__ = 'Thibault Vandermosten'

from math import *
import copy
from MoveStruct import *
from UFinal import *
import time


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
        self.moves1=Mpos()
        self.moves2=Mpos()
        for i in range(size):
            for j in range(size) :
                self.board[i][j].x=i
                self.board[i][j].y=j
                self.moves1.insert((i,j))
                self.moves2.insert((i,j))
        self.points1 = 0
        self.points2 = 4.5
        self.size = size
        self.lastpass= False
        self.komove=[]
        self.tocheck=set()
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
        st.moves1=copy.deepcopy(self.moves1)
        st.moves2=copy.deepcopy(self.moves2)
        st.tocheck=self.tocheck
        return st

    def DoMove(self,move):
        if move[0]==-1 and move[1]==-1:
            self.playerJustMoved= 3 - self.playerJustMoved
            self.lastboard=self.board
            self.lastpass=True
            self.komove.clear()
        else:
            self.lastpass=False
            self.komove.clear()


            (x,y)=(move[0],move[1])
            self.board[x][y].color = 3 - self.playerJustMoved
            self.board[x][y].comp.add(self.board[x][y])
            self.board[x][y].size=0

            #Remove move of stone put
            if self.moves1.contain(move):
                self.moves1.remove(move)
            if self.moves2.contain(move):
                self.moves2.remove(move)

            #set liberties of the stone alone
            if x>0:
                if self.board[x-1][y].color ==0:
                    self.board[x][y].size+=1


            if y>0:
                if self.board[x][y-1].color==0:
                    self.board[x][y].size+=1



            if x<self.size-1:
                if self.board[x+1][y].color==0:
                    self.board[x][y].size+=1


            if y <self.size-1:
                if self.board[x][y+1].color==0:
                    self.board[x][y].size+=1

            #if another stone of the same color, union
            #if another stone of the opposite color check if that groupa live

            if x>0:
                if(self.board[x-1][y].color==3-self.playerJustMoved):
                    Find(self.board[x-1][y]).size-=1
                    Union(self.board[x][y],self.board[x-1][y])


                if(self.board[x-1][y].color==self.playerJustMoved):
                    Find(self.board[x-1][y]).size-=1
                    if Find(self.board[x-1][y]).size==0:
                        self.DeleteGroup(Find(self.board[x-1][y]))

            if y>0:
                if(self.board[x][y-1].color==3-self.playerJustMoved):
                    Find(self.board[x][y-1]).size-=1
                    Union(self.board[x][y],self.board[x][y-1])


                if(self.board[x][y-1].color==self.playerJustMoved):
                    Find(self.board[x][y-1]).size-=1
                    if Find(self.board[x][y-1]).size==0:
                        self.DeleteGroup(Find(self.board[x][y-1]))


            if x<self.size-1:
                if(self.board[x+1][y].color==3-self.playerJustMoved):
                    Find(self.board[x+1][y]).size-=1
                    Union(self.board[x][y],self.board[x+1][y])

                if(self.board[x+1][y].color==self.playerJustMoved):
                    Find(self.board[x+1][y]).size-=1
                    if Find(self.board[x+1][y]).size==0:
                        self.DeleteGroup(Find(self.board[x+1][y]))


            if y <self.size-1:
                if(self.board[x][y+1].color==3-self.playerJustMoved):
                    Find(self.board[x][y+1]).size-=1
                    Union(self.board[x][y],self.board[x][y+1])

                if(self.board[x][y+1].color==self.playerJustMoved):
                    Find(self.board[x][y+1]).size-=1
                    if Find(self.board[x][y+1]).size==0:
                        self.DeleteGroup(Find(self.board[x][y+1]))


            self.playerJustMoved = 3 - self.playerJustMoved


    def DeleteGroup(self,x):
        temp=Find(x).comp.first
        col=temp.value.color
        if temp.next==None:
            self.komove.append((Find(x).x,Find(x).y))
        while temp != None :
            temp.value.color=0
            temp.value.rank=0
            temp.value.size=0
            if not self.moves1.contain((temp.value.x,temp.value.y)):
                if(col==1):
                    self.points2+=1
                else:
                    self.points1+=1
                self.moves1.insert((temp.value.x,temp.value.y))
                self.moves2.insert((temp.value.x,temp.value.y))
                if temp.value.x>0:
                    Find(self.board[temp.value.x-1][temp.value.y]).size+=1
                if temp.value.y>0:
                    Find(self.board[temp.value.x][temp.value.y-1]).size+=1
                if temp.value.x<self.size-1:
                    Find(self.board[temp.value.x+1][temp.value.y]).size+=1
                if temp.value.y <self.size-1:
                    Find(self.board[temp.value.x][temp.value.y+1]).size+=1
            temp.value.parent=temp.value
            temp.value.comp.clear()
            temp2=temp.next
            temp.next=None
            temp=temp2

    """
    Check return true if the intersection x,y is valid for player p
    """
    def Check(self,x,y,p):
        if x==-1 and y==-1:
            return True
        check=False

        if self.board[x][y].color!=0:
            return False

        nb=set()
        if len(self.komove)==1:
            if x==self.komove[0][0] and y==self.komove[0][1]:
                return False

        if x>0:
            nb.add(Find(self.board[x-1][y]))
        if y>0:
            nb.add(Find(self.board[x][y-1]))
        if x<self.size-1:
            nb.add(Find(self.board[x+1][y]))
        if y <self.size-1:
            nb.add(Find(self.board[x][y+1]))

        if len(nb)==1:
            if nb.pop().color==p:
                nb.clear()
                return False

        if x>0:
            if self.board[x-1][y].color != 0:
                Find(self.board[x-1][y]).size-=1
        if y>0:
            if self.board[x][y-1].color!=0:
                Find(self.board[x][y-1]).size-=1
        if x<self.size-1:
            if self.board[x+1][y].color!=0:
                Find(self.board[x+1][y]).size-=1
        if y <self.size-1:
            if self.board[x][y+1].color!=0:
                Find(self.board[x][y+1]).size-=1


        if x>0:
            if self.board[x-1][y].color==0:
                check=True
            elif  self.CheckL(x-1,y) and self.board[x-1][y].color==p:
                check= True
            elif  not self.CheckL(x-1,y) and self.board[x-1][y].color==3-p:
                check=True
        if y>0 and not check:
            if self.board[x][y-1].color==0:
                check=True
            elif self.CheckL(x,y-1) and self.board[x][y-1].color==p:
                check= True
            elif not self.CheckL(x,y-1) and self.board[x][y-1].color==3-p:
                check=True



        if x<self.size-1 and not check:
            if self.board[x+1][y].color==0:
                check=True
            elif self.CheckL(x+1,y) and self.board[x+1][y].color==p:
                check= True
            elif not self.CheckL(x+1,y) and self.board[x+1][y].color==3-p:
                check=True


        if y <self.size-1 and not check:
            if self.board[x][y+1].color==0:
                check=True
            elif self.CheckL(x,y+1) and self.board[x][y+1].color==p:
                check= True
            elif not self.CheckL(x,y+1) and self.board[x][y+1].color==3-p:
                check=True

        if x>0:
            if self.board[x-1][y].color != 0:
                Find(self.board[x-1][y]).size+=1
        if y>0:
            if self.board[x][y-1].color!=0:
                Find(self.board[x][y-1]).size+=1
        if x<self.size-1:
            if self.board[x+1][y].color!=0:
                Find(self.board[x+1][y]).size+=1
        if y <self.size-1:
            if self.board[x][y+1].color!=0:
                Find(self.board[x][y+1]).size+=1

        return check

    def CheckEye(self,x,y,p):
        check=False
        nb=set()
        if x>0:
            nb.add(Find(self.board[x-1][y]))
        if y>0:
            nb.add(Find(self.board[x][y-1]))
        if x<self.size-1:
            nb.add(Find(self.board[x+1][y]))
        if y <self.size-1:
            nb.add(Find(self.board[x][y+1]))

        if len(nb)==1:
            if nb.pop().color==p:
                nb.clear()
                self.tocheck.add((x,y))
                return True
        return check

    def CheckL(self,x,y):
        return Find(self.board[x][y]).size>0

    def GetMoves(self):

        if self.playerJustMoved==2:
            a=self.moves1
        else:
            a=self.moves2

        return a

    def GetWinner(self,player):
        for a in self.tocheck:
            i=a[0]
            j=a[1]
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

    def GetResJoseki32(self):
        white=False
        for i in range(self.size):
            for j in range (self.size):
                if self.board[i][j].color==2:
                    white=True
        if white:
            return 0
        else:
            return 1
    def GetResJoseki46(self):
        black=False
        for i in range(self.size):
            for j in range (self.size):
                if self.board[i][j].color==1:
                    black=True
        if black:
            return 1
        else:
            return 0

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
        """ Use the UCB1 formula to select a child node
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
        return "[M:" + str(self.move) + " W/V:" + str(self.wins) + "/" + str(self.visits) #+ " U:" + str(self.untriedMoves) + "]"

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
    m1=copy.deepcopy(rootstate.moves1)
    m2=copy.deepcopy(rootstate.moves2)
    for i in range(itermax):
        node = rootnode
        rootstate.moves1=m1
        rootstate.moves2=m2
        state = rootstate.Clone()

        # Select
        while node.untriedMoves.isempty() and node.childNodes != []: # node is fully expanded and non-terminal
            node = node.UCTSelectChild()
            state.DoMove(node.move)

        # Expand
        if not node.untriedMoves.isempty(): # if we can expand (i.e. state/node is non-terminal)
            m = node.untriedMoves.getRandom()
            still=True
            while (not state.Check(m[0],m[1],3-state.playerJustMoved)) and still:
                node.untriedMoves.remove(m)
                if node.untriedMoves.isempty:
                    still=False
                else:
                    m=node.untriedMoves.getRandom()

            if still:
                state.DoMove(m)
                node = node.AddChild(m,state) # add child and descend tree


        ck=True

        # Rollout -
        while ck : # while state is non-terminal

            templist=state.GetMoves()
            movetodo=True
            deleted =set()
            #if no more moves, including pass, we stop
            if templist.isempty():
                if state.lastpass==False:
                    state.DoMove((-1,-1))
                    movetodo=False
                else:
                    ck=False
            #if still moves possible, we look for one until either we got one and apply it, either we realize that the list was fill
            #with impossible moves and so we pass or stop the game
            else:
                while movetodo :
                    m=templist.getRandom()
                    if  state.Check(m[0],m[1],3-state.playerJustMoved) and not m in deleted:
                        state.DoMove(m)
                        movetodo=False

                    else:
                        templist.remove(m)
                        if not state.CheckEye(m[0],m[1],3-state.playerJustMoved):
                            deleted.add(m)
                        if templist.isempty():
                            movetodo=False
                            if state.lastpass==False:
                                state.DoMove((-1,-1))
                            else:
                                ck=False
                if state.playerJustMoved==2:
                    for i in deleted:
                        if not state.moves2.contain(i):
                            state.moves2.insert(i)
                else:
                    for i in deleted:
                        if not state.moves1.contain(i):
                            state.moves1.insert(i)

        # Backpropagate


        p1=state.GetWinner(1)
        #p1=state.GetResJoseki46()
        p2=1-p1


        while node != None: # backpropagate from the expanded node and work back to the root node
            # Update node with result from POV of node.playerJustMoved

            if node.playerJustMoved==2:
                node.Update(p2)
            if node.playerJustMoved==1:
                node.Update(p1)
            node = node.parentNode

    print (rootnode.ChildrenToString())

    try :
        return sorted(rootnode.childNodes, key = lambda c: c.visits)[-1].move # return the move that was most visited
    except IndexError:
        return ((-2,-2))

def UCTtime(rootstate, timelimit, verbose = False):
    """ Same than UCT, but with a limit of time instead of iterations"""

    rootnode = Node(state = rootstate)
    m1=copy.deepcopy(rootstate.moves1)
    m2=copy.deepcopy(rootstate.moves2)
    s=time.time()
    while time.time()-s < timelimit:
        node = rootnode
        rootstate.moves1=m1
        rootstate.moves2=m2
        state = rootstate.Clone()

        # Select
        while node.untriedMoves.isempty() and node.childNodes != []: # node is fully expanded and non-terminal
            node = node.UCTSelectChild()
            state.DoMove(node.move)

        # Expand
        if not node.untriedMoves.isempty(): # if we can expand (i.e. state/node is non-terminal)
            m = node.untriedMoves.getRandom()
            still=True
            while (not state.Check(m[0],m[1],3-state.playerJustMoved)) and still:
                node.untriedMoves.remove(m)
                if node.untriedMoves.isempty:
                    still=False
                else:
                    m=node.untriedMoves.getRandom()

            if still:
                state.DoMove(m)
                node = node.AddChild(m,state) # add child and descend tree


        ck=True

        # Rollout
        while ck : # while state is non-terminal

            templist=state.GetMoves()
            movetodo=True
            deleted =set()

            if templist.isempty():
                if state.lastpass==False:
                    state.DoMove((-1,-1))
                    movetodo=False
                else:
                    ck=False
            else:
                while movetodo :
                    m=templist.getRandom()
                    if  state.Check(m[0],m[1],3-state.playerJustMoved) and not m in deleted:
                        try:
                            state.DoMove(m)
                        except:
                            print(m,"MOVE FAILED")
                            ck=False
                            for i in range(state.size):
                                for j in range(state.size) :
                                    if state.board[i][j].color == 0:
                                        print(".",end="")
                                    else:
                                        print(state.board[i][j].color,end="")
                                print()
                            print()

                        movetodo=False

                    else:
                        templist.remove(m)
                        if not state.CheckEye(m[0],m[1],3-state.playerJustMoved):
                            deleted.add(m)
                        if templist.isempty():
                            movetodo=False
                            if state.lastpass==False:
                                state.DoMove((-1,-1))
                            else:
                                ck=False
                if state.playerJustMoved==2:
                    for i in deleted:
                        if not state.moves2.contain(i):
                            state.moves2.insert(i)
                else:
                    for i in deleted:
                        if not state.moves1.contain(i):
                            state.moves1.insert(i)
        # Backpropagate


        p1=state.GetWinner(1)
        #p1=state.GetResJoseki()
        p2=1-p1


        while node != None: # backpropagate from the expanded node and work back to the root node
            # Update node with result from POV of node.playerJustMoved

            if node.playerJustMoved==2:
                node.Update(p2)
            if node.playerJustMoved==1:
                node.Update(p1)
            node = node.parentNode
    try :
        return sorted(rootnode.childNodes, key = lambda c: c.visits)[-1].move # return the move that was most visited
    except IndexError:
        return ((-2,-2))

def UCTPlayGame():
    """ Play a sample game between two UCT players where each player gets a different number
        of UCT iterations (= simulations = tree nodes).
    """
    state = GoState(5)
    m=((-3,-3))
    while not state.GetMoves().isempty() and m !=((-2,-2)):
        print(str(state))
        if state.playerJustMoved == 1:
            m = UCT(rootstate = state, itermax = 1000, verbose = False) # play with values for itermax and verbose = True
        else:
            m = UCT(rootstate = state, itermax = 1000, verbose = False)
        print("Best Move: " + str(m) + "\n")
        if m !=((-2,-2)):
            state.DoMove(m)
        for i in range(state.size):
            for j in range(state.size) :
                print(state.board[i][j].color,end="")
            print()

    print("score",state.points1,state.points2)
    if state.GetWinner(state.playerJustMoved) == 1.0:
        print("Player " + str(state.playerJustMoved) + " wins!")
    elif state.GetWinner(state.playerJustMoved) == 0.0:
        print ("Player " + str(3 - state.playerJustMoved) + " wins!")
    else: print ("Nobody wins!")

def UCTdivided(rootstate,x,div):
    """
    A uct method with div time x/div operation, majority voting technique
    """
    test=[]
    testset=set()
    for i in range (div):
        m=UCT(rootstate,int(x/div), verbose = False)
        test.append(m)
        testset.add(m)
    best=0
    for i in testset:
        if test.count(i)>best:
            best=test.count(i)
            bestm=i
    return bestm
if __name__ == "__main__":
    """ Play a single game to the end using UCT for both players
"""
    a=GoState(9)

    s=time.time()

    m=UCT(a,1000,verbose=False)




    """for i in range(a.size):
            for j in range(a.size) :
                print(a.board[i][j].color,end="")
            print()"""

    print(time.time()-s)


    #UCTPlayGame()




