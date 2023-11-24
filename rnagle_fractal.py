from cmu_graphics import *

def onAppStart(app):
    filename = 'setup.txt'
    with open(filename, encoding='utf-8') as f:
        fileString = f.read()
                
    lines = fileString.splitlines()
    app.title = lines[0]
    app.level = int(lines[1])

def drawFractal(level, cx, cy, r):
    if level == 0:
        drawMickey(cx, cy, r)
    else:
        drawMickey(cx, cy, r*3/4)
        drawFractal(level-1, cx-r*3/4, cy-3/4*r, r*0.45)
        drawFractal(level-1, cx+r*3/4, cy-3/4*r, r*0.45)

def drawMickey(cx, cy, r):
    skinColor = rgb(253, 227, 203)
    tongueColor = rgb(246, 157, 133)
    #draw face shape
    drawCircle(cx, cy, r)
    drawOval(cx - r/4, cy - r*0.36, r*0.68, r, fill = skinColor)
    drawOval(cx + r/4, cy - r*0.36, r*0.68, r, fill = skinColor)
    drawOval(cx, cy + r*0.35, r*1.7, r, fill = skinColor)

    #draw mouth
    drawOval(cx, cy + r*0.5, r*0.7, r*0.6)
    drawArc(cx, cy + r*0.1, r*1.5, r, 210, 120, fill = skinColor, border = 'black', borderWidth = r/50)
    drawOval(cx, cy + r*0.2, r*1.25, r/2, fill = skinColor)
    drawArc(cx, cy + r*0.64, r*0.4, r*0.25, 180, 180, fill = tongueColor)
    
    #draw eyes
    drawOval(cx - r/8, cy - r*0.22, r/5, r/2, fill = 'white', border = 'black', borderWidth = r/50)
    drawOval(cx + r/8, cy - r*0.22, r/5, r/2, fill = 'white', border = 'black', borderWidth = r/50)
    
    drawOval(cx - r/12, cy - r/10, r/10, r/5)
    drawOval(cx + r/12, cy - r/10, r/10, r/5)

    #draw nose
    drawOval(cx, cy + r*0.1, r/2, r/3, border = skinColor, borderWidth = r/15)

    

def onKeyPress(app, key):
    if (key in ['up', 'right']) and (app.level < 5):
        app.level += 1
    elif (key in ['down', 'left']) and (app.level > 0):
        app.level -= 1

def redrawAll(app):
    drawFractal(app.level, 200, 250, 125)
    drawLabel(app.title, app.width/2, 30, size=16, bold=True)
    drawLabel('Use arrows to change level',
              app.width/2, 50, size=12, bold=True)

def main():
    runApp()

main()