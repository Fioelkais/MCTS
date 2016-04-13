__author__ = 'admin'

class NodeL:
    def __init__(self,v):
        self.value=v
        self.next=None

class LKlist (object):
    def __init__(self,v):
        self.first=NodeL(v)
        self.last=self.first

    def getFirst(self):
        return self.first

    def add(self,v):
        temp=NodeL(v)
        if(self.first==None):
            self.last=temp
        temp.next=self.first
        self.first=temp
    def union(self,lk):
        self.last.next=lk.first
        self.last=lk.last

    def clear(self):
        self.first=None


    def __str__(self):
        current=self.first
        print(current.value)
        while current.next != None:
            print(current.next.value)
            current=current.next
        return("")

