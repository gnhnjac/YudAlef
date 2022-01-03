
class Rect():

    def __init__(self,width,height):

        self.width = width
        self.height = height

    def __str__(self):

        return f"Width: {self.width}, Height: {self.height}"

    def __add__(self, r):

        return Rect(self.width + r.width, self.height + r.height)

    def __sub__(self, r):

        return Rect(abs(self.width - r.width), abs(self.height - r.height))

    def __mul__(self, r):

        return Rect(self.width * r.width, self.height * r.height)

    def __truediv__(self, r):
        return Rect(self.width / r.width, self.height / r.height)

    def __floordiv__(self, r):
        return Rect(self.width // r.width, self.height // r.height)

class Square(Rect):

    def __init(self,len):

        super(len,len)

rect = Rect(5,5)
rect2 = Rect(3,3)

print(rect // rect2)