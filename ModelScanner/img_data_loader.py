import pygame, sys
from PIL.ImageOps import flip
from pygame.examples.midi import input_main
from pygame.locals import *
from OpenGL.GL import *
from OpenGL.GLU import *
from pygame.constants import *
from PIL import Image
import os
import time
import math

green2 = [0.0, 0.5, 0.0, 0.0]


def cross(a, b):
    c = [a[1] * b[2] - a[2] * b[1],
         a[2] * b[0] - a[0] * b[2],
         a[0] * b[1] - a[1] * b[0]]

    return c


class OBJ:
    def __init__(self, filename, swapyz=True):
        has_mtl = False
        """Loads a Wavefront OBJ file. """
        self.vertices = []
        self.normals = []
        self.texcoords = []
        self.faces = []

        material = None
        for line in open(filename, "r"):
            if line.startswith('#'): continue
            values = line.split()
            if not values: continue
            if values[0] == 'v':
                v = list(map(float, values[1:4]))
                if swapyz:
                    v = v[0], v[2], v[1]
                self.vertices.append(v)
            elif values[0] == 'vn':
                v = list(map(float, values[1:4]))
                if swapyz:
                    v = v[0], v[2], v[1]
                self.normals.append(v)
            elif values[0] == 'vt':
                self.texcoords.append(map(float, values[1:3]))
            elif values[0] in ('usemtl', 'usemat'):
                material = values[1]

            elif values[0] == 'f':
                face = []
                texcoords = []
                norms = []
                normal_vertices = []
                for v in values[1:]:
                    w = v.split('/')
                    face.append(int(w[0]))
                    if len(w) >= 2 and len(w[1]) > 0:
                        texcoords.append(int(w[1]))
                    else:
                        texcoords.append(0)
                    if len(w) >= 3 and len(w[2]) > 0:
                        norms.append(int(w[2]))
                    else:
                        norms.append(0)
                # Per vertex
                    # Use cross-products to calculate the face normals for the triangles surrounding a given vertex,
                # add them together, and normalize.
                vertex1 = [(round(n, 4)) for n in self.vertices[face[0] - 1]]
                # print 'Vertex1 = ' + str(vertex1)
                vertex2 = [(round(n, 4)) for n in self.vertices[face[1] - 1]]
                # print 'Vertex2 = ' + str(vertex2)
                vertex3 = [(round(n, 4)) for n in self.vertices[face[2] - 1]]
                # print 'Vertex3 = ' + str(vertex3)
                vector1 = [vertex2[0] - vertex1[0], vertex2[1] - vertex1[1], vertex2[2] - vertex1[2]]

                vector2 = [vertex3[0] - vertex1[0], vertex3[1] - vertex1[1], vertex3[2] - vertex1[2]]
                vector3 = [(round(n, 4)) for n in cross(vector2, vector1)]

                # norms.append(normalize(vector3))
                print("cross product: " + str(vector3))

                # print self.vertices[10]
                # print "Vertex: " + self.vertices[face[0]]

                self.faces.append((face, norms, texcoords, material))
                # print(self.faces)
        self.gl_list = glGenLists(1)
        glNewList(self.gl_list, GL_COMPILE)
        glFrontFace(GL_CCW)
        for face in self.faces:
            vertices, normals, texture_coords, material = face

            glBegin(GL_POLYGON)
            for i in range(len(vertices)):
                if normals[i] > 0:
                    glNormal3fv(self.normals[normals[i] - 1])
                glVertex3fv(self.vertices[vertices[i] - 1])
            glEnd()
        glDisable(GL_TEXTURE_2D)
        glEndList()


def main():
    target_fps = 60
    pygame.init()
    viewport = (1600, 900)
    hx = viewport[0] / 2
    hy = viewport[1] / 2
    screen = pygame.display.set_mode(viewport, OPENGL | DOUBLEBUF | GL_DEPTH)

    glColorMaterial(GL_FRONT_AND_BACK, GL_AMBIENT_AND_DIFFUSE)
    glLightfv(GL_LIGHT0, GL_POSITION, (-40, 200, 100, 0.0))
    glLightfv(GL_LIGHT0, GL_AMBIENT, (0.2, 0.2, 0.2, 1.0))
    glLightfv(GL_LIGHT0, GL_DIFFUSE, (0.5, 0.5, 0.5, 1.0))
    glEnable(GL_LIGHT0)
    glEnable(GL_LIGHTING)
    glEnable(GL_COLOR_MATERIAL)
    glEnable(GL_DEPTH_TEST)
    glEnable(GL_NORMALIZE)
    glShadeModel(GL_SMOOTH)  # most obj files expect to be smooth-shaded

    input_dir = sys.argv[1]
    output_dir = '/home/hyzi/Documents/results/'
    filenames = os.listdir(input_dir)
    filenames.sort()

    obj = OBJ(input_dir + filenames[0], swapyz=False)

    clock = pygame.time.Clock()

    glMatrixMode(GL_PROJECTION)
    glLoadIdentity()
    width, height = viewport
    gluPerspective(90.0, width / float(height), 1, 100.0)
    glEnable(GL_DEPTH_TEST)
    glMatrixMode(GL_MODELVIEW)

    rx, ry = (0, 0)
    tx, ty = (0, 0)
    zpos = 5
    rotate = move = False
    i = 0
    iteration = 0
    index = 0
    prev_time = time.time()
    while 1:
        # No wait this is probably fastest speed
        # clock.tick(10000)
        for e in pygame.event.get():
            if e.type == QUIT:
                sys.exit()
            elif e.type == KEYDOWN and e.key == K_ESCAPE:
                sys.exit()
        # glClearColor(1, 1, 1, 1)
        glClearColor(0.0, 0.0, 0.0, 1.0)
        glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
        glLoadIdentity()

        # After 12 screenshot change object
        # RENDER OBJECT
        glMaterialfv(GL_FRONT_AND_BACK, GL_AMBIENT_AND_DIFFUSE, green2)
        glMaterialfv(GL_FRONT_AND_BACK, GL_SPECULAR, green2)
        glTranslate(0, 0, - 15)
        glRotate(-60, 1, 0, 0)
        # glRotate(30,)
        glRotate(i, 0, 0, 1)

        # glRotate(ry, 1, 0, 0)
        # glRotate(rx, 0, 1, 0)
        glScale(15.0, 15.0, 15.0)
        glCallList(obj.gl_list)
        if i % 30 == 0:
            glPixelStorei(GL_PACK_ALIGNMENT, 1)
            data = glReadPixels(0, 0, width, height, GL_RGB, GL_UNSIGNED_BYTE)
            image = Image.frombytes('RGB', (width, height), data)
            image = flip(image)
            output = output_dir + filenames[index].split('.')[0]
            if not os.path.exists(output):
                os.makedirs(output)
            image.save(output + '/out' + str(i) + '.jpeg')
            iteration = iteration + 1
            if iteration == 11:
                print("object: " + filenames[index])
                index = index + 1
                obj = OBJ(input_dir + filenames[index], swapyz=False)
                iteration = 0
                i = 0

        i = i + 1
        pygame.display.flip()
        curr_time = time.time()  # so now we have time after processing
        diff = curr_time - prev_time  # frame took this much time to process and render
        delay = max(1.0 / target_fps - diff,
                    0)  # if we finished early, wait the remaining time to desired fps, else wait 0 ms!
        time.sleep(delay)
        fps = 1.0 / (delay + diff)  # fps is based on total time ("processing" diff time + "wasted" delay time)
        prev_time = curr_time
        pygame.display.set_caption("{0}: {1:.2f}".format("Demo", fps))


main()
