import os
import sys
import time

import numpy
import pygame
from OpenGL.GL import *
from OpenGL.GLU import *
from PIL import Image
from PIL.ImageOps import flip
from pygame.constants import *


def normalize_v3(arr):
    # Normalize a numpy array of 3 component vectors shape=(n,3)
    lens = numpy.sqrt(arr[:, 0] ** 2 + arr[:, 1] ** 2 + arr[:, 2] ** 2)
    arr[:, 0] /= lens
    arr[:, 1] /= lens
    arr[:, 2] /= lens
    return arr


class OBJ:
    def __init__(self, filename, swapyz=True):
        # has_mtl = False
        # Loads a Wavefront OBJ file
        self.vertices = []
        self.normals = []
        self.texcoords = []
        self.faces = []

        material = None
        for line in open(filename, "r"):
            if line.startswith('#'):
                continue
            values = line.split()
            if not values:
                continue
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
            elif values[0] == 'f':
                face = []
                texcoords = []
                norms = []
                for v in values[1:]:
                    w = v.split('/')
                    face.append(int(w[0]) - 1)
                    # if len(w) >= 2 and len(w[1]) > 0:
                    #     texcoords.append(int(w[1]))
                    # else:
                    #     texcoords.append(0)
                    # if len(w) >= 3 and len(w[2]) > 0:
                    #     norms.append(int(w[2]))
                    # else:
                    #     norms.append(0)

                    self.faces.append((face, norms, texcoords, material))

        n_vertices = numpy.array(self.vertices)
        n_faces = numpy.array([row[0] for row in self.faces])

        # Create a zeroed array with the same type and shape as our vertices i.e., per vertex normal

        norm = numpy.zeros(n_vertices.shape, dtype=n_vertices.dtype)
        # Create an indexed view into the vertex array using the array of three indices for triangles
        tris = n_vertices[n_faces]
        # Calculate the normal for all the triangles, by taking the cross product of the vectors v1-v0, and v2-v0 in
        #  each triangle
        n = numpy.cross(tris[::, 1] - tris[::, 0], tris[::, 2] - tris[::, 0])
        # n is now an array of normals per triangle. The length of each normal is dependent the vertices,
        # we need to normalize these, so that our next step weights each normal equally.
        normalize_v3(n)
        # Now we have a normalized array of normals, one per triangle, i.e., per triangle normals.
        # But instead of one per triangle (i.e., flat shading), we add to each vertex in that triangle,
        # the triangles' normal. Multiple triangles would then contribute to every vertex, so we need to
        # normalize again afterwards.
        norm[n_faces[:, 0]] += n
        norm[n_faces[:, 1]] += n
        norm[n_faces[:, 2]] += n
        normalize_v3(norm)

        self.gl_list = glGenLists(1)
        glNewList(self.gl_list, GL_COMPILE)
        glFrontFace(GL_CCW)
        glBegin(GL_TRIANGLES)
        for face in n_faces:
            t_normal = norm[face]
            t_vertice = n_vertices[face]

            glNormal3fv(t_normal[0].tolist())
            glVertex3fv(t_vertice[0].tolist())
            glNormal3fv(t_normal[1].tolist())
            glVertex3fv(t_vertice[1].tolist())
            glNormal3fv(t_normal[2].tolist())
            glVertex3fv(t_vertice[2].tolist())

        glEnd()
        glDisable(GL_TEXTURE_2D)
        glEndList()

        # def calculate_normals(self,face):


def main():
    target_fps = 60
    pygame.init()
    viewport = (1600, 900)

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
    output_dir = sys.argv[2]
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
        glTranslate(0, 0, - 15)
        glRotate(-60, 1, 0, 0)
        glRotate(i, 0, 0, 1)

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
