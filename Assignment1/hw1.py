from telnetlib import NEW_ENVIRON
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
        glBegin(self.mode)
        glColor4f(self.color[0], self.color[1], self.color[2], self.color[3])
        for vertex in self.vertices:
            newVertex = self.mat @ vertex
            glVertex3f(newVertex[0], newVertex[1], newVertex[2])


            # for vertex in self.vertices:
            # print(f"origin {vertex} {self.mat}")
            # newVertex = np.transpose([vertex,[0,0,0,0],[0,0,0,0],[0,0,0,0]])
            # print(f"trans {newVertex}")
            # newVertex = newVertex @ self.mat
            # print(f"mat {newVertex}")
            # newVertex = np.transpose(newVertex)[0]
            # print(f"new {newVertex}")
            # glVertex3f(newVertex[0], newVertex[1], newVertex[2])
        glEnd()

    # Task 3-1
    def scale(self, sx, sy):
        dx = dy = 1
        if sx > 0 :
            dx = 1.1
        elif sx < 0:
            dx = 0.9
        
        if sy > 0 :
            dy = 1.1
        elif sy < 0:
            dy = 0.9

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
        # xm = np.array([[cos, -sin,   0,  0], 
        #                           [sin, cos,    0,  0], 
        #                           [0,   0,      1,  0], 
        #                           [0,   0,      0,  1]])
        # ym = np.array([[cos, -sin,   0,  0], 
        #                           [sin, cos,    0,  0], 
        #                           [0,   0,      1,  0], 
        #                           [0,   0,      0,  1]])
                                

        self.mat = transfromeMat @ self.mat

    # Task 3-3
    def translation(self, dx, dy):
        transfromeMat = np.array([[1,   0,  dx,  dx], 
                                  [0,   1, dy,  dy], 
                                  [0,   0,  1,  0], 
                                  [0,   0,  0,  1]])
        self.mat = transfromeMat @ self.mat
        # for i, vertex in enumerate(self.vertices):
        #     self.vertices[i] = [vertex[0] + dx, vertex[1] + dy,  vertex[2], vertex[3]]


# Task 1
# define your polygons here
class Triangle(Polygon):
    def __init__(self, x, y):
        super().__init__(x, y)
        self.mode = GL_TRIANGLES
        self.color = [55/255, 114/255, 240/255, 1]
        self.vertices = [
            [x, y+0.1, 0, 1],
            [x-0.1, y-0.1, 0, 1],
            [x+0.1, y-0.1, 0, 1],
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
        self.color = [148/255, 74/255, 255/255, 1]
        self.vertices = [
            [x-0.1, y+0.1, 0, 1],
            [x+0.1, y+0.1, 0, 1],
            [x+0.1, y-0.1, 0, 1],
            [x-0.1, y-0.1, 0, 1],
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


# TODO : 대칭 추가하기, 크기 바꾸고, 변수 이름 변경 
class Ellipse(Polygon):
    def __init__(self, x, y):
        super().__init__(x, y)
        self.mode = GL_TRIANGLE_FAN
        self.color = [24/255, 158/255, 135/255, 1]
        self.vertices = []
        pointNum = 20
        theta = (2 * math.pi) / pointNum
        c = math.cos(theta)
        s = math.sin(theta)
        xs, ys = 1, 0 # starting angle is 0
        for i in range(pointNum):
            pointX = xs * 0.05 + x
            pointY = ys * 0.01 + y
            self.vertices.append([pointX, pointY, 0, 1])
            # self.vertices.extend([[pointX, pointY, 0],[-pointX, pointY, 0], [pointX, -pointY, 0], [-pointX, -pointY, 0]])
            
            t = xs
            xs = c * xs - s * ys
            ys = s * t + c * ys

        xs = ys = t = 0

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
        self.polygons = []
        self.polyNum = 0
        self.halfWidth = 400
        self.halfHeight = 400
        self.click = False
        self.isScaleMode = False
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
        
        if key == b's':
            self.isScaleMode = not self.isScaleMode
            print(f"now scale mode is {self.isScaleMode}")
    
        glutPostRedisplay()

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

        if state == GLUT_DOWN:
            self.click = True
            self.xStart = x
            self.yStart = y
        elif state == GLUT_UP:
            self.click = False
        
        if button == GLUT_LEFT_BUTTON and self.click:
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

        dx = (self.xStart - x)
        dy = (self.yStart - y)

        if self.isScaleMode :
            if abs(dx) > 2 or abs(dy) > 2:
                for pol in self.polygons:
                    pol.scale(dx, dy)
        else :
            if abs(dx) > 2 or abs(dy) > 2:
                degree = math.pi/1800
                if abs(dx) > abs(dy):
                    degree = degree*dx
                else :
                    degree = -degree*dy
                for pol in self.polygons:
                    pol.rotation(degree)

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
