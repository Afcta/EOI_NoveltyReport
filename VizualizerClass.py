import turtle
import math

def anglePosition2(angle, rad):
    """Returns the absolute position of an angle in a circumference with an offset in y (x, y+offset)

    Args:
        angle (float): radians
        rad (float): radius

    Returns:
        float, float: posX, posY + rad
    """
    x, y = rad*math.cos(angle),rad*math.sin(angle)
    return x, y + rad

class agentEnvironment:
    def __init__(self, pos = 0, radius=50):
        self.rad = radius
        self.pos = pos
        self.turt = turtle.Turtle()
        self.turt.shape("circle")
        self.turt.color("orange")
        self.turt.pencolor("black")
        self.turt.shapesize(0.5, 0.5)
        self._make_fturt()
        self._make_pturt()
        self.turt.speed(0)
        print(self.turt.position())
        print(self.turt.heading())
        self.has_food = False
        self.draw_circle()
        # for i in range(5):
        #     self.draw_food_spot(i)

    def _make_fturt(self):
        self.fturt = turtle.Turtle()
        self.fturt.speed(0)
        self.fturt.hideturtle()
        self.fturt.pencolor("yellow")
        self.fturt.pensize(3)
        self.fturt.hideturtle()
        
    def _make_pturt(self):
        self.pturt = turtle.Turtle()
        self.pturt.speed(0)
        self.pturt.hideturtle()
        self.pturt.pencolor("black")
        self.pturt.pensize(1)
        self.pturt.penup()

    def write(self, sentenceList):
        self.pturt.clear()
        maxHeight = 80
        x = 100
        for i in range(len(sentenceList)):
            self.pturt.setpos(x, maxHeight-i*10)
            self.pturt.write(sentenceList[i])

        
    def undo_fturt(self, n):
        for _ in range(n):
            self.fturt.undo()

    def draw_circle(self):
        self.turt.circle(self.rad)
        #Draw nest
        self.turt.penup()
        self.turt.pencolor("blue")
        self.turt.pensize(2)
        self.turt.setpos(anglePosition2(-math.pi/4, self.rad))
        self.turt.pendown()
        self.turt.setheading(-90/2+90)
        self.turt.circle(self.rad, 90)
        self.reset_turt_pos(self.turt)

    def reset_turt_pos(self, turtle):
        turtle.penup()
        turtle.setpos(0,0)
        turtle.setheading(0)
        if turtle != self.turt:
            turtle.pendown()

    def reset_environment(self):
        self.clear_food_spot()
        self.move_agent(0)
    
    def clear_food_spot(self):
        self.fturt.clear()

    def move_agent(self, angPos):
        self.turt.setpos(anglePosition2(angPos, self.rad))

    def draw_food_spot(self, foodID):
        if foodID >4 or foodID < 0: 
            raise IndexError("draw_food_spot only takes arguments from 0 to 4")
        if self.has_food: self.fturt.undo()
        # self.reset_turt_pos(self.fturt)
        foodSize = 45 #pi/4
        minAng = 90 - 45/2 
        newOrientation = minAng + foodID*45 + 90
        self.fturt.setheading(newOrientation)
        self.fturt.penup()
        self.fturt.setpos(anglePosition2((minAng+foodID*45)*(math.pi/180),self.rad))
        self.fturt.pendown()
        print(self.turt.heading())
        self.fturt.circle(self.rad, 45)
        self.has_food = True

if __name__ == "__main__":
    t = agentEnvironment()