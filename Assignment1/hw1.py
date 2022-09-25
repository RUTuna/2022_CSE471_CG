from OpenGL.GL import *
from OpenGL.GLUT import *
import numpy as np
import math 

class Polygon:
    def __init__(self, x, y):
        self.mat = np.eye(4)
        self.x = x
        self.y = y
        self.vertices = []

    def draw(self):
        raise NotImplementedError

    def scale(self, sx, sy):
        transfromeMat = np.array([[sx,  0,  0,  0], 
                                  [0,   sy, 0,  0], 
                                  [0,   0,  1,  0], 
                                  [0,   0,  0,  1]])

        self.mat = self.mat @ transfromeMat
    
    def translate(self, dx, dy):
        for i, vertex in enumerate(self.vertices):
            self.vertices[i] = [vertex[0] + dx, vertex[1] + dy,  vertex[2]]


# define your polygons here
class Triangle(Polygon):
    def __init__(self, x, y):
        super().__init__(x, y)
        self.vertices = [
            [x, y+0.1, 0],
            [x-0.1, y-0.1, 0],
            [x+0.1, y-0.1, 0]
        ]
        self.vertices = list(np.array(self.vertices))

    def draw(self):
        glBegin(GL_TRIANGLES)
        for vertex in self.vertices:
            glColor4f(55/255, 114/255, 240/255, 1)
            glVertex3f(vertex[0], vertex[1], vertex[2])
        glEnd()

    def translate(self, dx, dy):
        super().translate(dx, dy)


class Rectangle(Polygon):
    def __init__(self, x, y):
        super().__init__(x, y)
        self.vertices = [
            [x-0.1, y+0.1, 0],
            [x+0.1, y+0.1, 0],
            [x+0.1, y-0.1, 0],
            [x-0.1, y-0.1, 0],
        ]
        self.vertices = list(np.array(self.vertices))

    def draw(self):
        glBegin(GL_QUADS)
        for vertex in self.vertices:
            glColor4f(148/255, 74/255, 255/255, 1)
            glVertex3f(vertex[0], vertex[1], vertex[2])
        glEnd()
    
    def translate(self, dx, dy):
        super().translate(dx, dy)


class Ellipse(Polygon):
    def __init__(self, x, y):
        super().__init__(x, y)
        self.vertices = []
        pointNum = 20
        theta = (2 * math.pi) / pointNum
        c = math.cos(theta)
        s = math.sin(theta)
        xs, ys = 1, 0 # starting angle is 0
        for i in range(pointNum):
            pointX = xs * 0.05 + x
            pointY = ys * 0.01 + y
            self.vertices.append([pointX, pointY, 0])
            # self.vertices.extend([[pointX, pointY, 0],[-pointX, pointY, 0], [pointX, -pointY, 0], [-pointX, -pointY, 0]])
            
            t = xs
            xs = c * xs - s * ys
            ys = s * t + c * ys

        xs = ys = t = 0

    def draw(self):
        glBegin(GL_TRIANGLE_FAN)
        for vertex in self.vertices:
            glColor4f(24/255, 158/255, 135/255, 1)
            glVertex3f(vertex[0], vertex[1], vertex[2])
        glEnd()

    def translate(self, dx, dy):
        super().translate(dx, dy)


class Viewer:
    def __init__(self):
        self.mode = 0
        self.polygons = []
        self.polyNum = 0
        self.halfWidth = 400
        self.halfHeight = 400
        pass

    def display(self):
        glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
        glClearColor(0, 0, 0, 1)

        glMatrixMode(GL_MODELVIEW)

        # visualize your polygons here
        self.halfWidth = glutGet(GLUT_WINDOW_WIDTH)/2
        self.halfHeight = glutGet(GLUT_WINDOW_HEIGHT)/2

        for pol in self.polygons:
            pol.draw()

        glutSwapBuffers()

    def keyboard(self, key, x, y):
        print(f"keyboard event: key={key}, x={x}, y={y}")
        if glutGetModifiers() & GLUT_ACTIVE_SHIFT:
            print("shift pressed")
        if glutGetModifiers() & GLUT_ACTIVE_ALT:
            print("alt pressed")
        if glutGetModifiers() & GLUT_ACTIVE_CTRL:
            print("ctrl pressed")

        if key == b'1':
            self.mode = 1
            print("Triangle Draw")
        elif key == b'2':
            self.mode = 2
            print("Rectangle Draw")
        elif key == b'3':
            self.mode = 3
            print("Ellipse Draw")
        elif key == b'\x1b':
            self.mode = 0
            print("cancellation of polygon drawing mode")
    
        glutPostRedisplay()

    def special(self, key, x, y):
        print(f"special key event: key={key}, x={x}, y={y}")
        if key == 100: # left arrow
            print("Translate left")
            for pol in self.polygons:
                pol.translate(-1/self.halfWidth, 0)

        elif key == 101: # up arrow
            print("Translate up")
            for pol in self.polygons:
                pol.translate(0, 1/self.halfHeight)

        elif key == 102: # right arrow
            print("Translate right")
            for pol in self.polygons:
                pol.translate(1/self.halfWidth, 0)

        if key == 103: # down arrow
            print("Translate down")
            for pol in self.polygons:
                pol.translate(0, -1/self.halfHeight)

        glutPostRedisplay()

    def mouse(self, button, state, x, y):
        # button macros: GLUT_LEFT_BUTTON, GLUT_MIDDLE_BUTTON, GLUT_RIGHT_BUTTON
        print(f"mouse press event: button={button}, state={state}, x={x}, y={y}")

        if button == GLUT_LEFT_BUTTON and state == GLUT_DOWN:
            newX = (x-self.halfWidth)/self.halfWidth
            newY = -(y-self.halfHeight)/self.halfHeight
            self.polyNum =  self.polyNum + 1
            if self.mode == 1 :
                self.polygons.append( Triangle(newX,newY) )
                print(f"add Triangle {self.polyNum}")
            elif self.mode == 2 :
                self.polygons.append( Rectangle(newX,newY) )
                print(f"add Rectangle {self.polyNum}")
            elif self.mode == 3 :
                self.polygons.append( Ellipse(newX,newY) )
                print(f"add Ellipse {self.polyNum}")
            else :
                 self.polyNum =  self.polyNum - 1
                

        glutPostRedisplay()

    def motion(self, x, y):
        print(f"mouse move event: x={x}, y={y}")

        glutPostRedisplay()

    def run(self):
        glutInit()
        glutInitDisplayMode(GLUT_DOUBLE | GLUT_RGB | GLUT_DEPTH)
        glutInitWindowSize(800, 800)
        glutInitWindowPosition(0, 0)
        glutCreateWindow("CS471 Computer Graphics #1")

        glutDisplayFunc(self.display)
        glutKeyboardFunc(self.keyboard)
        glutSpecialFunc(self.special)
        glutMouseFunc(self.mouse)
        glutMotionFunc(self.motion)

        glutMainLoop()


if __name__ == "__main__":
    viewer = Viewer()
    viewer.run()
