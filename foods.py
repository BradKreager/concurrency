class food:
    def __init__(self):
        self.consumed = False

    def consumed(self):
        return self.consumed





class hamburger(food):
    def __init__(self):
        self.name = "HAMBURGER"

    def __repr__(self):
        return "HAMBURGER"

    def __eq__(self, obj):
        return isinstance(obj, hamburger) and obj.name == self.name

    def __ne__(self, obj):
        return not self.__eq__(obj)





class soda(food):
    def __init__(self):
        self.name = "SODA"

    def __repr__(self):
        return "SODA"

    def __eq__(self, obj):
        return isinstance(obj, soda) and obj.name == self.name

    def __ne__(self, obj):
        return not self.__eq__(obj)





class fries(food):
    def __init__(self):
        self.name = "FRIES"

    def __repr__(self):
        return "FRIES"

    def __eq__(self, obj):
        return isinstance(obj, fries) and obj.name == self.name

    def __ne__(self, obj):
        return not self.__eq__(obj)





class garbage(food):
    def __init__(self):
        self.name = "GARBAGE"

    def __repr__(self):
        return "GARBAGE"

    def __eq__(self, obj):
        return isinstance(obj, garbage) and obj.name == self.name

    def __ne__(self, obj):
        return not self.__eq__(obj)

