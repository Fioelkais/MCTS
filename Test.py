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
            m=UCTdivided( a, iter)
        else:
            m=UCT(rootstate = a, itermax = iter, verbose = False)
        if m==((1,0)):
            cor+=1
    print(cor/100)


if __name__ == "__main__":
    testall(100,9,1000)
    #joseki34(1000,True  )