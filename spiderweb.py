from cmu_graphics import *
from random import randint

# Experimental variables

numberDots = 2
speedScaleFactor = 1
speed = 1
lineColor = "white"
app.background = "black"
app.steps = 0


# Static

dots = [Circle(200,200,5,fill=None) for i in range(numberDots)]

for d in dots:
    d.slope_direction = ( randint(-10, 10), randint(-10, 10) )
    # d.slope_direction = ( 1, -1 )

x = Polygon(fill=None, border=lineColor, opacity=100, borderWidth=0.3)


def moveDot(dot):
    rise, run = dot.slope_direction
    dot.centerX += run
    dot.centerY += rise
    if dot.centerY - 5 > 400 or dot.centerY - 5 < 0:
        dot.slope_direction = (-rise * speed * speedScaleFactor, run * speed * speedScaleFactor)
    if dot.centerX + 5 > 400 or dot.centerX - 5 < 0:
        dot.slope_direction = (rise * speed * speedScaleFactor, -run * speed * speedScaleFactor)
    x.addPoint(dot.centerX, dot.centerY)

def onStep():
    app.steps += 1
    if app.steps < 750:
        for dot in dots:
            moveDot(dot)

cmu_graphics.run()