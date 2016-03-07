__author__ = 'admin'

class Node:
    def __init__(self,v):
        self.value=v
        self.next=None
    def getVal(self):
        return self.value
    def getNext(self):
        return self.next
    def removeNext(self):
        self.next=self.next.next

class LKlist (object):
    def __init__(self,v):
        self.first=Node(v)
        self.last=self.first

    def getFirst(self):
        return self.first

    def add(self,v):
        temp=Node(v)
        temp.next=self.first
        self.first=temp
    def union(self,lk):
        self.last.next=lk.first
        self.last=lk.last

    def __str__(self):
        current=self.first
        print(current.value)
        while current.next != None:
            print(current.next.value)
            current=current.next
        return("")

