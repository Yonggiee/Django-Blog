class Circle():

    pi = 3.14
    radius

    def __init__(self, radius):
        self.radius = radius

    def get_area(self):
        return self.radius * self.radius * self.pi


circle1 = Circle(3)
circle2 = Circle(4)
print(circle1.get_area())
