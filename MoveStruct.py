__author__ = 'admin'
import random

"""
Data structure that support insert, remove and getRandomElement in O(1)
"""

class Mpos(object):
    def __init__(self):
        self.h={}
        self.ar=[]

    def insert(self, value):
        self.ar.append(value)
        self.h[value]=len(self.ar)-1

    def remove(self,value):
        last=self.ar[len(self.ar)-1]
        torem=self.h[value]
        self.ar[torem]=last
        self.h[last]=torem
        self.ar.pop()
        del self.h[value]

    def contain(self,value):
        return value in self.h

    def getRandom(self):
        x = random.randint(0,len(self.ar)-1)
        return self.ar[x]

    def isempty(self):
        if self.ar  :
            return False
        else:
            return True

    def show(self):
        print("moves START")
        for i in self.ar:
            print(i)
        print("moves END")

if __name__ == "__main__":
    a=Mpos()

