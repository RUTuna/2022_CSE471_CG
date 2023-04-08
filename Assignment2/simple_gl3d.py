from cmath import sqrt
from OpenGL.GL import *
from OpenGL.GLU import *
from OpenGL.GLUT import *
import numpy as np
import math 

class Viewer:
    def __init__(self):
        # transform matrix
        self.perp = np.eye(4)
        self.model = np.eye(4)
        self.rotateMatrix = np.eye(4)

        # camera view parameter
        self.translate = [0,0]
        self.scale = 1

        # projectioin parameter
        # Task 5
        self.cop = np.array([0,0,1])
        self.at = np.array([0,0,0])
        self.up = np.array([0,1,0])
        self.fov = 0

        # window width, height 
        self.width = 800 
        self.height = 800

        self.click = False


    # Because of numpy cross, according to https://github.com/microsoft/pylance-release/issues/3277 
    def cross(self, a:np.ndarray,b:np.ndarray)->np.ndarray:
        return np.cross(a,b)

    # Task 1 - camera view function
    def world2camera(self, cop, at, up):
        z = cop - at
        z = z / np.linalg.norm(z)
        x = self.cross(up, z)
        x = x / np.linalg.norm(x)
        y = self.cross(z, x)

        rc = [-np.dot(cop, x), -np.dot(cop, y), -np.dot(cop, z), 1]
        x = np.append(x,0)
        y = np.append(y,0)
        z = np.append(z,0)

        return np.array([x,y,z,rc])

    # set near (actually z-coordinamtion of COP)
    def near(self, fov):
        near = 0.5/math.tan(math.radians(fov/2))
        self.cop = np.array([self.cop[0], self.cop[1], near*2])

    # camera translate (actually model translate)
    def translation(self, dx, dy):
        transfromeMat = np.array([[1,   0,  0,  0], 
                                  [0,   1,  0,  0], 
                                  [0,   0,  1,   0], 
                                  [dx,  dy,  0,   1]])
        self.model =  self.model @ transfromeMat 

    # transform 2D plane to 3D trackball
    def transPos(self, x, y):
        print(f"x is {x} y is {y}")
        radius = min([self.width, self.height])/2
        z = 0
        d = pow(radius,2) - pow(x,2) - pow(y, 2)
        if d > 0:
            z = sqrt(d).real

        return z

    # Task 2 - virtual trackball
    def trackball(self, str, dst):
        # transfrom coordinate(2D plane to 3D trackball), center is (0,0) and y-axis is filp
        str = np.array([str[0] - (self.width/2), (self.height/2) - str[1], 0])
        dst = np.array([dst[0] - (self.width/2), (self.height/2) - dst[1], 0])

        str[2] = self.transPos(str[0], str[1])
        dst[2] = self.transPos(dst[0], dst[1])

        # calculate rotation angle and axis
        axis = self.cross(str, dst)
        axisNorm = np.linalg.norm(axis)
        if axisNorm == 0 :
            angle = 0
        else :
            axis = axis / axisNorm
            angle = - axisNorm / (np.linalg.norm(str) + np.linalg.norm(dst))

        xAngle = math.radians(angle * axis[0])
        yAngle = math.radians(angle * axis[1]) 
        zAngle = math.radians(angle * axis[2]) 

        cosx = math.cos(xAngle)
        sinx = math.sin(xAngle)

        cosy = math.cos(yAngle)
        siny = math.sin(yAngle)

        cosz = math.cos(zAngle)
        sinz = math.sin(zAngle)

        matrixX = np.array([[cosz,  -sinz,  0,  0], 
                            [sinz,  cosz,   0,  0], 
                            [0,     0,      1,  0], 
                            [0,     0,      0,  1]])

        matriY = np.array([[cosy,   0,  siny,   0], 
                            [0,     1,  0,      0], 
                            [-siny, 0,  cosy,   0], 
                            [0,     0,  0,      1]])

        matriZ = np.array([[1,  0,      0,      0], 
                            [0, cosx,   -sinx,  0], 
                            [0, sinx,   cosx,   0], 
                            [0, 0,      0,      1]])

        self.rotateMatrix =  self.rotateMatrix @ matrixX @ matriY @ matriZ 

        # rotate model
        self.model =  self.model @ matrixX @ matriY @ matriZ 

        # rotate camera (rotate COP)
        # test = matrixX @ matriY @ matriZ
        # test = np.delete(test, 3 , axis = 0)
        # test = np.delete(test, 3 , axis = 1)
        # self.cop = test @ self.cop
                                    
        
    def light(self):
        glEnable(GL_COLOR_MATERIAL)
        glEnable(GL_LIGHTING)
        glEnable(GL_DEPTH_TEST)

        # feel free to adjust light colors
        lightAmbient = [0.5, 0.5, 0.5, 1.0]
        lightDiffuse = [0.5, 0.5, 0.5, 1.0]
        lightSpecular = [0.5, 0.5, 0.5, 1.0]
        lightPosition = [1, 1, -1, 0]    # vector: point at infinity
        glLightfv(GL_LIGHT0, GL_AMBIENT, lightAmbient)
        glLightfv(GL_LIGHT0, GL_DIFFUSE, lightDiffuse)
        glLightfv(GL_LIGHT0, GL_SPECULAR, lightSpecular)
        glLightfv(GL_LIGHT0, GL_POSITION, lightPosition)
        glEnable(GL_LIGHT0)

    def display(self):
        glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
        glClearColor(0, 0, 0, 1)
        glColor4f(1,1,1,1)

        glMatrixMode(GL_PROJECTION)
        glLoadIdentity()
        # projection matrix
        # use glOrtho and glFrustum (or gluPerspective) here
        if self.fov < 5 : # orhogonal
            top = self.height/800
            right = self.width/800
            factor = 1/min(right, top)
            right = right * factor
            top = top * factor
            glOrtho(-right, right, -top, top, 0.1, 50)
        else:
            top = 0.1 * math.tan(math.radians(self.fov/2));  
            top = top * max(800/self.width, 800/self.height)
            right = (self.width/self.height) * top
            glFrustum(-right, right, -top, top, 0.1, 50)
            # gluPerspective(self.fov, self.width/self.height, 0.1, 50)
        
        glMultMatrixf(self.world2camera(self.cop, self.at, self.up))

        glMatrixMode(GL_MODELVIEW)    
        glLoadIdentity()
        # do some transformations using camera view
        glMultMatrixf(self.model)
        glScalef(self.scale, self.scale, self.scale)
        glutSolidTeapot(0.5)


        # to axis operates independently of both GL_PROJECTION and GL_MODELVIEW
        glMatrixMode(GL_PROJECTION)
        glLoadIdentity()
        glMatrixMode(GL_MODELVIEW)    
        glLoadIdentity()

        glPushMatrix()
        glTranslatef(-0.9, -0.9, 0)
        glMultMatrixf(self.rotateMatrix) # only rotate

        glLineWidth(3)
        glBegin(GL_LINES)
        glColor4f(0,0,1,1)
        glVertex3f(0,0,0.1)
        glVertex3f(0,0,0)

        glColor4f(0,1,0,1)
        glVertex3f(0,0.1,0)
        glVertex3f(0,0,0)

        glColor4f(1,0,0,1)
        glVertex3f(0.1,0,0)
        glVertex3f(0,0,0)
        glEnd()
        
        glPopMatrix()

        glutSwapBuffers()

    def keyboard(self, key, x, y):
        print(f"keyboard event: key={key}, x={x}, y={y}")
        if glutGetModifiers() & GLUT_ACTIVE_SHIFT:
            print("shift pressed")
        if glutGetModifiers() & GLUT_ACTIVE_ALT:
            print("alt pressed")
        if glutGetModifiers() & GLUT_ACTIVE_CTRL:
            print("ctrl pressed")

        # Task 4 - user interface for translation
        if key == b'w':
            self.translation(0, 10/self.height)
            # self.translate[1] += self.height/100
        elif key == b'a':
            self.translation(-10/self.width, 0)
            # self.translate[0] -= self.width/100
        elif key == b's':
            self.translation(0, -10/self.height)
            # self.translate[1] -= self.height/100
        elif key == b'd':
            self.translation(10/self.width, 0)
            # self.translate[0] += self.width/100

        # Task 4 - user interface for scaling
        if key == b'+':
            if self.scale < 1.0:
                self.scale += 0.1
            elif self.scale < 10.0:
                self.scale += 1.0
            print(f"Scale is {round(self.scale, 1)}")
        elif key == b'-':
            if self.scale > 1.0 :
                self.scale -= 1.0
            elif self.scale >= 0.2:
                self.scale -= 0.1
            print(f"Scale is {round(self.scale, 1)}")

        # Task 4 - user interface for reset camera and projection
        if key == b'q':
            self.scale = 1
            self.model = np.eye(4)
            self.rotateMatrix = np.eye(4)
        elif key == b'e':
            self.fov = 0

        # Task 4 - user interface for exit. But only for Window OS
        # if key == b'\x1b':
        #     print("exit")
        #     glutLeaveMainLoop()

        glutPostRedisplay()

    def special(self, key, x, y):
        print(f"special key event: key={key}, x={x}, y={y}")
        # Task 4 - user interface for FoV
        if key == 101 and self.fov < 90: # up arrow
            self.fov += 5.0

            print(f"FoV is {self.fov}")
        elif key == 103 and self.fov > 0: # down arrow
            self.fov -= 5.0
            print(f"FoV is {self.fov}")

        if self.fov > 0:
            self.near(self.fov)
        glutPostRedisplay()

    def mouse(self, button, state, x, y):
        # button macros: GLUT_LEFT_BUTTON, GLUT_MIDDLE_BUTTON, GLUT_RIGHT_BUTTON
        print(f"mouse press event: button={button}, state={state}, x={x}, y={y}")

        # Task 4 - user interface for rotation
        if state == GLUT_DOWN:
            self.click = True
            self.xStart = x
            self.yStart = y
        elif state == GLUT_UP:
            self.click = False
            
        glutPostRedisplay()

    def motion(self, x, y):
        print(f"mouse move event: x={x}, y={y}")

        # Task 4 - user interface for rotation
        print(f"start position {self.xStart} {self.yStart}")
        self.trackball([self.xStart, self.yStart], [x,y])
        self.xStart = x
        self.yStart = y

        glutPostRedisplay()

    def reshape(self, w, h):
        # implement here
        print(f"window size: {w} x {h}")
        # Task 4 - user interface for resize window
        glViewport(0,0,w,h)
        self.width = w 
        self.height = h

        glutPostRedisplay()

    def run(self):
        glutInit()

        glutInitDisplayMode(GLUT_DOUBLE | GLUT_RGB | GLUT_DEPTH)
        glutInitWindowSize(800, 800)
        glutInitWindowPosition(0, 0)
        glutCreateWindow(b"CS471 Computer Graphics #2")

        glutDisplayFunc(self.display)
        glutKeyboardFunc(self.keyboard)
        glutSpecialFunc(self.special)
        glutMouseFunc(self.mouse)
        glutMotionFunc(self.motion)
        glutReshapeFunc(self.reshape)

        self.light()

        # Task 4 - user interface for exit. But only for Window OS
        # glutSetOption(GLUT_ACTION_ON_WINDOW_CLOSE, GLUT_ACTION_GLUTMAINLOOP_RETURNS)
        glutMainLoop()


if __name__ == "__main__":
    viewer = Viewer()
    viewer.run()
