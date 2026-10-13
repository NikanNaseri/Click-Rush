import random

class GameObject:
    def __init__(self, name, score, color, duration, is_illusion=False):
        self.name = name
        self.score = score
        self.color = color
        self.duration = duration 
        self.x = random.randint(50, 350)
        self.y = random.randint(50, 350)
        self.spawn_time = 0 
        self.is_illusion = is_illusion

class ShapeFactory:
    @staticmethod
    def create_shape():
        r = random.random()
        if r < 0.1:
            return GameObject("Shield", 0, "blue", 5)
        elif r < 0.2:
            return GameObject("Ice", 0, "cyan", 3)
        elif r < 0.5:
            return GameObject("Bad", random.randint(-3, -1), "red", 2)
        else:
            return GameObject("Good", random.randint(1, 6), "green", 2)

# an example for illusional objects -->    GameObject("Illusion", 0, "pink", 3, is_illusion=True)

class PlayerState:
    def __init__(self):
        self.stamina = 100
        self.stress = 0
        self.frozen_until = 0
        self.shield_until = 0 
        self.score = 0
