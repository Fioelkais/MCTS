__author__ = 'admin'

class NodeUF(object):
    def __init__(self):
        self.parent = self
        #self.value = value
        self.rank = 0
        self.color=0
        self.liberty=[]
        self.children = []
        self.x=0
        self.y=0
    def __str__(self):
        return self.rank

def Create(values):
    l = [NodeUF(value) for value in values]
    return l

def MakeSet(x):
     x.parent = x
     x.rank   = 0

def Union(x, y):
     xRoot = Find(x)
     yRoot = Find(y)
     if xRoot.rank > yRoot.rank:
         yRoot.parent = xRoot
         #process of transferring children
         xRoot.children.append(yRoot)
         xRoot.children.extend(yRoot.children)
         yRoot.children.clear()
         #process of transferring liberties
         xRoot.liberty.extend(yRoot.liberty)
         yRoot.liberty.clear()

     elif xRoot.rank < yRoot.rank:
         xRoot.parent = yRoot

         yRoot.children.append(xRoot)
         yRoot.children.extend(xRoot.children)
         xRoot.children.clear()

         yRoot.liberty.extend(xRoot.liberty)
         xRoot.liberty.clear()
     elif xRoot != yRoot: # Unless x and y are already in same set, merge them
         yRoot.parent = xRoot

         xRoot.children.append(yRoot)
         xRoot.children.extend(yRoot.children)
         yRoot.children.clear()

         xRoot.liberty.extend(yRoot.liberty)
         yRoot.liberty.clear()

         xRoot.rank = xRoot.rank + 1

def Find(x):
     if x.parent == x:
        return x
     else:
        x.parent = Find(x.parent)
        return x.parent

if __name__ == "__main__":
    """Unit test to verify the methods of UF"""
    b = [[NodeUF() for x in range(3)] for x in range(3)]
    print(b[0][0].color)

    print(Find(b[0][0])==Find(b[0][0]))

    b[0][1].color= 2
    b[0][0].color= 1
    b[0][2].color = 3
    print(b[0][0].color)
    print(b[0][1].color)

    Union(b[0][1],b[0][0])
    Union(b[0][1],b[0][2])

    print(Find(b[0][0]).color)


    print(b[2][2].color,"test")

    print(len(b[0][0].liberty),"length")

    for i in Find(b[0][0]).children:
        print(i.color)
        #i.color=25
    #    print(b[0][0].color)