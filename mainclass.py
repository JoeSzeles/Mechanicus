class Cuboid:
    name = "Cuboid"

    def __init__(self, length, breadth, height, weight):
        self.length = length
        self.breadth = breadth
        self.height = height
        self.weight = weight

    def volume(self):
        x = self.length
        y = self.breadth
        z = self.height
        v = x * y * z
        print("The volume is:", v)

    def density(self):
        x = self.length
        y = self.breadth
        z = self.height
        v = x * y * z
        d = self.weight / v
        print("Density is:", d)

    def surface_area(self):
        x = self.length
        y = self.breadth
        z = self.height
        s = 2 * (x * y + y * z + x * z)
        print("The surface area is:", s)


