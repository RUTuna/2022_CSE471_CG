from telnetlib import NEW_ENVIRON
from OpenGL.GL import *
from OpenGL.GLUT import *
import numpy as np
import math 

class Polygon:
    def __init__(self, x, y):
        self.mat = np.eye(4)
        self.origin = [x, y, 1, 1]
        self.newOrigin = [x, y, 1, 1]
        self.vertices = []

    # Task 1, Task 4
    def draw(self):
        # draw polygon
        glPushMatrix()
        glLoadIdentity()
        glMultMatrixf(self.mat)
        glBegin(self.mode)
        glColor4f(self.color[0], self.color[1], self.color[2], self.color[3])
        for vertex in self.vertices:

            # newVertex = self.mat @ vertex # apply transform matrix
            # glVertex3f(newVertex[0], newVertex[1], newVertex[2])
            glVertex3f(vertex[0], vertex[1], vertex[2])
        glEnd()
        glPopMatrix()

        # draw origin point
        glPointSize(2.0)
        glBegin(GL_POINTS)
        glColor4f(1,1,1,1)
        glVertex3f(self.newOrigin[0], self.newOrigin[1], self.newOrigin[2])
        glEnd()

    # Task 3-1
    def scale(self, sx, sy):
        dx = dy = 1
        if sx > 0:
            dx = 0.99
        elif sx < 0:
            dx = 1.01
        
        if sy > 0:
            dy = 1.01
        elif sy < 0:
            dy = 0.99

        transfromeMat = np.array([[dx,  0,  0,  0], 
                                  [0,   dy, 0,  0], 
                                  [0,   0,  1,  0], 
                                  [0,   0,  0,  1]])

        self.mat = transfromeMat @ self.mat
    
    # Task 3-2
    def rotation(self, degree):
        cos = math.cos(degree)
        sin = math.sin(degree)
        transfromeMat = np.array([[cos, -sin,   0,  0], 
                                  [sin, cos,    0,  0], 
                                  [0,   0,      1,  0], 
                                  [0,   0,      0,  1]])

        self.mat = transfromeMat @ self.mat

    # Task 3-3
    def translation(self, dx, dy):
        transfromeMat = np.array([[1,   0,  0,  0], 
                                  [0,   1,  0,  0], 
                                  [0,   0,  1,   0], 
                                  [dx,   dy,  0,   1]])
        self.mat = transfromeMat @ self.mat

    # Task 3-3
    def translationori(self, dx, dy):
        transfromeMat = np.array([[1,   0,  0,  dx], 
                                  [0,   1,  0,  dy], 
                                  [0,   0,  1,   0], 
                                  [0,   0,  0,   1]])
        self.mat = transfromeMat @ self.mat


# Task 1
# define your polygons here
class Triangle(Polygon):
    def __init__(self, x, y):
        super().__init__(x, y)
        self.mode = GL_TRIANGLES
        self.color = [186/255, 231/255, 175/255, 1]
        self.vertices = [
            [x, y+0.1, 1, 1],
            [x-0.1, y-0.1, 1, 1],
            [x+0.1, y-0.1, 1, 1],
        ]
        self.vertices = list(np.array(self.vertices))

    def draw(self):
        super().draw()
        
    def translation(self, dx, dy):
        super().translation(dx, dy)
    
    def scale(self, sx, sy):
        super().scale(sx, sy)

    def rotation(self, degree):
        super().rotation(degree)


class Rectangle(Polygon):
    def __init__(self, x, y):
        super().__init__(x, y)
        self.mode = GL_QUADS
        self.color = [175/255, 196/255, 231/255, 1]
        self.vertices = [
            [x-0.1, y+0.1, 1, 1],
            [x+0.1, y+0.1, 1, 1],
            [x+0.1, y-0.1, 1, 1],
            [x-0.1, y-0.1, 1, 1],
        ]
        self.vertices = list(np.array(self.vertices))

    def draw(self):
        super().draw()
    
    def translation(self, dx, dy):
        super().translation(dx, dy)

    def scale(self, sx, sy):
        super().scale(sx, sy)

    def rotation(self, degree):
        super().rotation(degree)


class Ellipse(Polygon):
    def __init__(self, x, y):
        super().__init__(x, y)
        self.mode = GL_TRIANGLE_FAN
        self.color = [238/255, 175/255, 175/255, 1]
        self.vertices = []

        pointNum = 40
        radiusX = 0.1
        radiusY = 0.05
        theta = math.pi / pointNum
        for i in range(pointNum):
            pointX = radiusX * math.cos(theta * i)
            pointY = radiusY * math.sin(theta * i) 
            self.vertices.extend([[x + pointX, y + pointY, 1, 1], [x - pointX, y + pointY, 1, 1], [x -pointX, y - pointY, 1, 1], [x + pointX, y - pointY, 1, 1]])

    def draw(self):
        super().draw()

    def translation(self, dx, dy):
        super().translation(dx, dy)

    def scale(self, sx, sy):
        super().scale(sx, sy)

    def rotation(self, degree):
        super().rotation(degree)


class Viewer:
    def __init__(self):
        self.mode = 0
        self.polygons = [] # array to save added polygon
        self.polyNum = 0 # number of polygons

        # half of window width, height 
        self.halfWidth = 400 
        self.halfHeight = 400

        # init is rotate, global mode
        self.click = False # mouse click
        self.isScaleMode = False # True : scale, Flase : rotate
        self.isGlobalMode = True # True : global transform, Flase : local transform

    def display(self):
        glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
        glClearColor(0, 0, 0, 1)

        glMatrixMode(GL_MODELVIEW)

        # visualize your polygons here
        self.halfWidth = glutGet(GLUT_WINDOW_WIDTH)/2
        self.halfHeight = glutGet(GLUT_WINDOW_HEIGHT)/2

        # Task 5
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

        # Task 2
        # change draw mode
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
        

        # change scale/rotate global/local mode
        if key == b's':
            self.isScaleMode = not self.isScaleMode
            print(f"now scale mode is {self.isScaleMode}")

        if key == b'g':
            self.isGlobalMode = not self.isGlobalMode
            print(f"now global mode is {self.isGlobalMode}")
    
        glutPostRedisplay()

    # Task 3-3, Task 4
    def special(self, key, x, y):
        print(f"special key event: key={key}, x={x}, y={y}")
        if key == 100: # left arrow
            print("Translate left")
            for pol in self.polygons:
                pol.translation(-1/self.halfWidth, 0)

        elif key == 101: # up arrow
            print("Translate up")
            for pol in self.polygons:
                pol.translation(0, 1/self.halfHeight)

        elif key == 102: # right arrow
            print("Translate right")
            for pol in self.polygons:
                pol.translation(1/self.halfWidth, 0)

        if key == 103: # down arrow
            print("Translate down")
            for pol in self.polygons:
                pol.translation(0, -1/self.halfHeight)

        glutPostRedisplay()

    def mouse(self, button, state, x, y):
        # button macros: GLUT_LEFT_BUTTON, GLUT_MIDDLE_BUTTON, GLUT_RIGHT_BUTTON
        print(f"mouse press event: button={button}, state={state}, x={x}, y={y}")

        # set start coordinates to measure drag distance
        if state == GLUT_DOWN:
            self.click = True
            self.xStart = x
            self.yStart = y
        elif state == GLUT_UP:
            self.click = False
        
        # Task 2
        if button == GLUT_LEFT_BUTTON and self.click:
            # conversion between window coordinates and world coordinates
            newX = (x-self.halfWidth)/self.halfWidth
            newY = -(y-self.halfHeight)/self.halfHeight

            if self.mode == 1:
                self.polyNum =  self.polyNum + 1
                self.polygons.append( Triangle(newX,newY) )
                print(f"add Triangle, # polygon is {self.polyNum}")
            elif self.mode == 2:
                self.polyNum =  self.polyNum + 1
                self.polygons.append( Rectangle(newX,newY) )
                print(f"add Rectangle, # polygon is {self.polyNum}")
            elif self.mode == 3:
                self.polyNum =  self.polyNum + 1
                self.polygons.append( Ellipse(newX,newY) )
                print(f"add Ellipse, # polygon is {self.polyNum}")
                
        glutPostRedisplay()

    def motion(self, x, y):
        print(f"mouse move event: x={x}, y={y}")

        # drag distance
        dx = (self.xStart - x)
        dy = (self.yStart - y)

        # Task 3-1, Task 3-2, Task 4
        if abs(dx) > 2 or abs(dy) > 2:
            for pol in self.polygons:
                # if not self.isGlobalMode:
                #     pol.translation(-pol.newOrigin[0], -pol.newOrigin[1])

                if self.isScaleMode:
                    pol.scale(dx, dy)

                else:
                    degree = math.pi/1800
                    if abs(dx) > abs(dy):
                        degree = degree*dx
                    else:
                        degree = -degree*dy
                    pol.rotation(degree)

                # if not self.isGlobalMode:
                #     pol.translation(pol.newOrigin[0], pol.newOrigin[1])

                # if global mode, transform origin
                if self.isGlobalMode:
                    pol.newOrigin = pol.mat.transpose() @ pol.origin 

        glutPostRedisplay()

    def run(self):
        glutInit()
        glutInitDisplayMode(GLUT_DOUBLE | GLUT_RGB | GLUT_DEPTH)
        glutInitWindowSize(800, 800)
        glutInitWindowPosition(0, 0)
        glutCreateWindow(b"CS471 Computer Graphics #1")

        glutDisplayFunc(self.display)
        glutKeyboardFunc(self.keyboard)
        glutSpecialFunc(self.special)
        glutMouseFunc(self.mouse)
        glutMotionFunc(self.motion)

        glutMainLoop()


if __name__ == "__main__":
    viewer = Viewer()
    viewer.run()
