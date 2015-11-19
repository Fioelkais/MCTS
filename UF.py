__author__ = 'admin'

class NodeUF(object):
    def __init__(self):
        self.parent = self
        #self.value = value
        self.rank = 0
        self.color=0
        self.liberty=0
        self.children = []
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
         xRoot.children.append(yRoot)
         xRoot.children.extend(yRoot.children)
         yRoot.children.clear()
     elif xRoot.rank < yRoot.rank:
         xRoot.parent = yRoot
         yRoot.children.append(xRoot)
         yRoot.children.extend(xRoot.children)
         xRoot.children.clear()
     elif xRoot != yRoot: # Unless x and y are already in same set, merge them
         yRoot.parent = xRoot
         xRoot.children.append(yRoot)
         xRoot.children.extend(yRoot.children)
         yRoot.children.clear()
         xRoot.rank = xRoot.rank + 1

def Find(x):
     if x.parent == x:
        return x
     else:
        x.parent = Find(x.parent)
        return x.parent


"""Unit test to verify the methods of UF"""
b = [[NodeUF() for x in range(3)] for x in range(3)]
print(b[0][0].color)


b[0][1].color= 2
b[0][0].color= 1
b[0][2].color = 3
print(b[0][0].color)
print(b[0][1].color)

Union(b[0][1],b[0][0])
Union(b[0][1],b[0][2])

print(Find(b[0][0]).color)


for i in Find(b[0][0]).children:
    print(i.color)
    #i.color=25
#    print(b[0][0].color)