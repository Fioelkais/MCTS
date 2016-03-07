from LKlist import *
from rf import *
class NodeUF(object):
    def __init__(self):
        self.parent = self
        #self.value = value
        self.rank = 0
        self.color=rf(0)
        self.comp = LKlist((self))
        self.lib=LKlist((self))
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
         xRoot.comp.union(yRoot.comp)
         xRoot.lib.union(yRoot.lib)

     elif xRoot.rank < yRoot.rank:
         xRoot.parent = yRoot

         yRoot.comp.union(xRoot.comp)
         yRoot.lib.union(xRoot.lib)


     elif xRoot != yRoot: # Unless x and y are already in same set, merge them
         yRoot.parent = xRoot

         xRoot.comp.union(yRoot.comp)
         xRoot.lib.union(yRoot.lib)

         xRoot.rank = xRoot.rank + 1

def Destroy(x):
    temp=Find(x).comp.first
    temp.value.color.set(0)
    temp.value.rank=0
    temp.value.parent=temp.value
    temp.value.comp=LKlist(temp.value)
    while(temp.next !=None):
        temp.next.value.color.set(0)
        temp.next.value.rank=0
        temp.next.value.parent=temp.value
        temp.next.value.comp=LKlist(temp.value)
        temp2=temp.next
        temp.next=None
        temp=temp2

def Find(x):
     if x.parent == x:
        return x
     else:
        x.parent = Find(x.parent)
        return x.parent

def Extend1(x,y):
    for i in y:
        if i not in x:
            x.append(i)

if __name__ == "__main__":
    """Unit test to verify the methods of UF"""

    x=5
    y=x
    x=3
    print(y,'toast')

    b = [[NodeUF() for x in range(3)] for x in range(3)]
    print(b[0][0].color.get())
    c=b[0][0].color
    print(c.get(),"t1")
    b[0][0].color.set(8)
    print(c.get(),"t2")

    print(Find(b[0][0])==Find(b[0][0]))

    b[0][1].color= 2
    b[0][0].color= 1
    b[0][2].color = 3
    print(b[0][0].color)
    print(b[0][1].color)

    Union(b[0][1],b[0][0])
    Union(b[0][1],b[0][2])

    print("test")

    Destroy(Find(b[0][0]))
    print(b[0][0].color)
    print(b[0][1].color)



