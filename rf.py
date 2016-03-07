__author__ = 'admin'
class rf:
    def __init__(self, obj): self.obj = obj
    def get(self):    return self.obj
    def set(self, obj):      self.obj = obj

if __name__ == "__main__":
    a = rf('test')
    b = a
    print (a.get())  # => [1, 2]
    print (b.get())  # => [1, 2]

    a.set((5,5))
    print (a.get()) # => 2
    print (b.get()) # => 2