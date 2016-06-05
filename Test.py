from GSUFinal import *

def testall(iter, size,all):
    a=GoState(size)
    #print(a.CheckP(0,0,1)


    s=time.time()


    cor = [[0 for x in range(size)] for x in range(size)]

    for i in range (all):
        m=UCT(rootstate = a, itermax =iter , verbose = False)
        cor[m[0]][m[1]]+=1
    for i in range(size):
        for j in range(size) :
            print(cor[i][j],end=" ")
        print()

    print(time.time()-s)

def joseki34(iter, divided):
    cor=0
    for i in range (100):
        a=GoState(5)
        a.points2=0
        a.DoMove((0,2))
        a.DoMove((0,3))
        a.DoMove((1,2))
        a.DoMove((1,3))
        a.DoMove((2,2))
        a.DoMove((2,3))

        a.DoMove((3,0))
        a.DoMove((3,2))
        a.DoMove((3,1))
        a.DoMove((3,3))

        a.playerJustMoved=1
        a.DoMove((4,0))
        a.playerJustMoved=1
        a.DoMove((4,1))
        a.playerJustMoved=1
        a.DoMove((4,2))
        a.playerJustMoved=1
        a.DoMove((4,3))
        a.playerJustMoved=1
        a.DoMove((3,4))
        a.playerJustMoved=1
        a.DoMove((1,4))

        #a.DoMove((2,1))
        if divided:
            m=UCTdivided( a, iter,20)
        else:
            m=UCT(rootstate = a, itermax = iter, verbose = False)
        if m==((1,0)):
            cor+=1
    print(cor/500)


def joseki46b(iter, divided):
    cor=0
    #Strange behaviour
    for i in range (10):
        a=GoState(5)
        a.points2=0
        a.points1=0.5

        a.DoMove((0,2))
        a.DoMove((0,1))
        a.DoMove((1,1))
        a.DoMove((1,0))
        a.DoMove((2,1))
        a.DoMove((2,0))

        a.DoMove((1,3))
        a.DoMove((0,0))
        a.DoMove((2,3))
        a.DoMove((1,4))

        a.DoMove((3,3))
        a.DoMove((3,0))
        a.DoMove((3,4))
        a.DoMove((3,1))

        a.playerJustMoved=1
        a.DoMove((4,2))
        a.playerJustMoved=1
        a.DoMove((4,3))
        a.playerJustMoved=1
        a.DoMove((4,4))

        a.moves1.remove((4,0))
        a.moves1.remove((4,1))
        a.moves2.remove((4,0))
        a.moves2.remove((4,1))

        #a.DoMove((2,1))
        if divided:
            m=UCTdivided( a, iter,10)
        else:
            m=UCT(rootstate = a, itermax = iter, verbose = False)
        if m==((2,4)) or  m==((2,2)) or m==((3,2)):
            cor+=1
    print(cor/100)


def joseki32h(iter, divided):
    cor=0
    #Strange behaviour
    for i in range (100):
        a=GoState(6)

        a.DoMove((0,3))
        a.DoMove((0,2))
        a.DoMove((1,4))
        a.DoMove((1,1))
        a.DoMove((2,1))
        a.DoMove((2,0))
        a.DoMove((2,4))
        a.DoMove((2,2))
        a.DoMove((3,3))
        a.DoMove((2,3))

        a.DoMove((4,0))
        a.DoMove((4,1))
        a.DoMove((4,3))
        a.DoMove((4,2))

        a.DoMove((5,1))
        a.playerJustMoved=2
        a.DoMove((5,2))
        a.playerJustMoved=2
        a.DoMove((5,3))
        a.playerJustMoved=2

        a.DoMove((3,2))


        #a.DoMove((2,1))
        if divided:
            m=UCTdivided( a, iter)
        else:
            m=UCT(rootstate = a, itermax = iter, verbose = False)
        if m==((3,1)) :
            cor+=1
    print(cor/100)

def testmatch(iter1, iter2, divided,div1,div2):
    won1=0
    won2=0
    for a in range (50):
        state = GoState(9)
        m=((-3,-3))
        passe=0
        while not state.GetMoves().isempty() and passe<2:
            if state.playerJustMoved == 1:
                if divided:
                    m=UCTdivided(state,iter2,div2)
                else:
                    m = UCT(rootstate = state, itermax = iter2, verbose = False)
            else:
                if divided:
                    m=UCTdivided(state,iter1,div1)
                else:
                    m = UCT(rootstate = state, itermax = iter1, verbose = False)
            if m !=((-2,-2)):
                passe=0
                state.DoMove(m)
            else:
                passe+=1
                state.playerJustMoved=3-state.playerJustMoved
        for i in range(state.size):
            for j in range(state.size) :
                print(state.board[i][j].color,end="")
            print()

        if state.GetWinner(1) == 1.0:
            won1+=1
        else:
            won2+=1
        print(a,won1,won2)



if __name__ == "__main__":
    #testall(5000,9,1000)
    #joseki34(1000,False )
    #joseki46b(1000,True)
    joseki32h(1000,False)
    s=time.time()
    #print("5*1000vs5000")
    #testmatch(5000,5000,True,5,10)
    #a=GoState(7)
    #m=UCT(a,1000,False)
    print(time.time()-s)