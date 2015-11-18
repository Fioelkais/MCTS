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
        return self.value

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