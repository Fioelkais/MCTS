__author__ = 'admin'
import random

class Mpos(object):
    def __init__(self):
        self.h={}
        self.ar=[]
        self.l=0

    def insert(self, value):
        self.l+=1
        self.ar.append(value)
        self.h[value]=self.l-1

    def remove(self,value):
        last=self.ar[self.l-1]
        torem=self.h[value]
        self.ar[torem]=last
        self.h[last]=torem
        self.l-=1
        del self.h[value]

    def contain(self,value):
        return value in self.h

    def getRandom(self):
        x = random.randint(0,self.l-1)
        return self.ar[x]

    def isempty(self):
        if self.ar:
            return False
        else:
            return True

if __name__ == "__main__":
    a=Mpos()
    a.insert((0,0))
    print(a.contain((0,1)))
    print(a.getRandom())