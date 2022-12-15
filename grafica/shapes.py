# coding=utf-8
"""Textures and transformations in 3D"""

import glfw
from OpenGL.GL import *
import OpenGL.GL.shaders
import numpy as np
import sys
import os.path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
import grafica.transformations as tr
import grafica.basic_shapes as bs
import grafica.easy_shaders as es
import grafica.scene_graph as sg
from grafica.assets_path import getAssetPath

__author__ = "Daniel Calderon"
__license__ = "MIT"

############################################################################

def createColorPyramid(r, g ,b):

    # Defining the location and colors of each vertex  of the shape
    vertices = [
    #    positions         colors
        -0.5, 0.5,  0,  r, g, b,
         0.5, -0.5, 0,  r, g, b,
         0.5, 0.5,  0,  r, g, b,
        -0.5, -0.5, 0,  r, g, b,
         0, 0,  0.5,  r, g, b]

    # Defining connections among vertices
    # We have a triangle every 3 indices specified
    indices = [
         0, 1, 2,
         0, 1, 3,
         0, 2, 4,
         2, 4, 1,
         3, 4, 1,
         0, 4, 3]

    return bs.Shape(vertices, indices)

def create_tree(pipeline):
    # Piramide verde
    green_pyramid = createColorPyramid(0, 1, 0)
    gpuGreenPyramid = es.GPUShape().initBuffers()
    pipeline.setupVAO(gpuGreenPyramid)
    gpuGreenPyramid.fillBuffers(green_pyramid.vertices, green_pyramid.indices, GL_STATIC_DRAW)

    # Cubo cafe
    brown_quad = bs.createColorCube(139/255, 69/255, 19/255)
    gpuBrownQuad = es.GPUShape().initBuffers()
    pipeline.setupVAO(gpuBrownQuad)
    gpuBrownQuad.fillBuffers(brown_quad.vertices, brown_quad.indices, GL_STATIC_DRAW)

    # Tronco
    tronco = sg.SceneGraphNode("tronco")
    tronco.transform = tr.scale(0.05, 0.05, 0.2)
    tronco.childs += [gpuBrownQuad]

    # Hojas
    hojas = sg.SceneGraphNode("hojas")
    hojas.transform = tr.matmul([tr.translate(0, 0, 0.1), tr.uniformScale(0.25)])
    hojas.childs += [gpuGreenPyramid]

    # Arbol
    tree = sg.SceneGraphNode("arbol")
    tree.transform = tr.identity()
    tree.childs += [tronco, hojas]

    return tree


def create_house(pipeline):
    # Piramide cafe
    brown_pyramid = createColorPyramid(166/255, 112/255, 49/255)
    gpuBrownPyramid = es.GPUShape().initBuffers()
    pipeline.setupVAO(gpuBrownPyramid)
    gpuBrownPyramid.fillBuffers(brown_pyramid.vertices, brown_pyramid.indices, GL_STATIC_DRAW)

    # Cubo rojo
    red_cube = bs.createColorCube(1, 0, 0)
    gpuRedCube = es.GPUShape().initBuffers()
    pipeline.setupVAO(gpuRedCube)
    gpuRedCube.fillBuffers(red_cube.vertices, red_cube.indices, GL_STATIC_DRAW)

    # Cubo cafe
    brown_cube = bs.createColorCube(166/255, 112/255, 49/255)
    gpuBrownCube = es.GPUShape().initBuffers()
    pipeline.setupVAO(gpuBrownCube)
    gpuBrownCube.fillBuffers(brown_cube.vertices, brown_cube.indices, GL_STATIC_DRAW)

    # Techo
    techo = sg.SceneGraphNode("techo")
    techo.transform = tr.matmul([tr.translate(0, 0, 0.1), tr.scale(0.2, 0.4, 0.2)])
    techo.childs += [gpuBrownPyramid]

    # Base
    base = sg.SceneGraphNode("base")
    base.transform = tr.matmul([tr.translate(0, 0, 0), tr.scale(0.2, 0.4, 0.2)])
    base.childs += [gpuRedCube]

    # Puerta
    puerta = sg.SceneGraphNode("puerta")
    puerta.transform = tr.matmul([tr.translate(0, -0.2, 0), tr.scale(0.05, 0.001, 0.1)])
    puerta.childs += [gpuBrownCube]

    # Casa
    casa = sg.SceneGraphNode("house")
    casa.transform = tr.identity()
    casa.childs += [techo, base, puerta]

    return casa

def create_skybox():
    gpuSky = es.toGPUShape(createSkyBox("assets/skybox3.png"), GL_REPEAT, GL_LINEAR)
    
    skybox = sg.SceneGraphNode("skybox")
    skybox.transform = tr.identity()#tr.matmul([tr.translate(0, 0, 0.3), tr.uniformScale(2)])
    skybox.childs += [gpuSky]

    return skybox

def create_floor():
    gpuFloor = es.toGPUShape(bs.createTextureQuad("assets/grass.jfif", 8, 8), GL_REPEAT, GL_LINEAR)

    floor = sg.SceneGraphNode("floor")
    floor.transform = tr.matmul([tr.translate(0, 0, 0),tr.scale(2, 2, 1)])
    floor.childs += [gpuFloor]

    return floor

#funcion para crear un cubo/ skybox con texturas
# se agregaron normales
def createSkyBox(image_filename):
    dx = 1.0 / 4.0
    dy = 1.0 / 3.0
    r = 1
    vertices = []
    indices = []

    vertices += [
        -r, r, -r, 0 * dx, 2 * dy,-1,0,1,
        r, r, -r, 1 * dx, 2 * dy,-1,0,1,
        r, r, r, 1 * dx, 1 * dy,-1,0,1,
        -r, r, r, 0 * dx, 1 * dy,-1,0,1]
    indices += [0, 1, 2, 2, 3, 0]

    vertices += [
        r, r, -r, 1 * dx, 2 * dy,-1,0,1,
        r, -r, -r, 2 * dx, 2 * dy,-1,0,1,
        r, -r, r, 2 * dx, 1 * dy,-1,0,1,
        r, r, r, 1 * dx, 1 * dy,-1,0,1]
    indices += [4, 5, 6, 6, 7, 4]

    vertices += [
        r, -r, -r, 2 * dx, 2 * dy,-1,0,1,
        -r, -r, -r, 3 * dx, 2 * dy,-1,0,1,
        -r, -r, r, 3 * dx, 1 * dy,-1,0,1,
        r, -r, r, 2 * dx, 1 * dy,-1,0,1]
    indices += [8, 9, 10, 10, 11, 8]

    vertices += [
        -r, -r, -r, 3 * dx, 2 * dy,-1,0,1,
        -r, r, -r, 4 * dx, 2 * dy,-1,0,1,
        -r, r, r, 4 * dx, 1 * dy,-1,0,1,
        -r, -r, r, 3 * dx, 1 * dy,-1,0,1]
    indices += [12, 13, 14, 14, 15, 12]

    vertices += [
        -r, r, -r, 1 * dx, 3 * dy,-1,0,1,
        -r, -r, -r, 2 * dx, 3 * dy,-1,0,1,
        r, -r, -r, 2 * dx, 2 * dy,-1,0,1,
        r, r, -r, 1 * dx, 2 * dy,-1,0,1]
    indices += [16, 17, 18, 18, 19, 16]

    vertices += [
        r, r, r, 1 * dx, 1 * dy,-1,0,1,
        r, -r, r, 2 * dx, 1 * dy,-1,0,1,
        -r, -r, r, 2 * dx, 0 * dy,-1,0,1,
        -r, r, r, 1 * dx, 0 * dy,-1,0,1]
    indices += [20, 21, 22, 22, 23, 20]

    return bs.Shape(vertices, indices, image_filename)

###################################################################################################

# Función para generar la tubería (creada por mí dado que para el personaje se usó un archivo .OBJ)
def createColorPipe(N, h, R1, R2, r, g, b):
    vertices = []
    indices = []

    dtheta = 2 * np.pi / N

    for i in range(N):
        theta = i * dtheta
        
        #            posición                                                  color    normales
        vertices += [R2*np.cos(theta), R2*np.sin(theta), 0,                   r, g, b, np.cos(theta), np.sin(theta), 0]
        vertices += [R2*np.cos(theta), R2*np.sin(theta), h-0.1,               r, g, b, 0, 0, 0]
        vertices += [(2*R2-R1)*np.cos(theta), (2*R2-R1)*np.sin(theta), h-0.1, r, g, b, np.cos(theta), np.sin(theta), 0]
        vertices += [(2*R2-R1)*np.cos(theta), (2*R2-R1)*np.sin(theta), h,     r, g, b, np.cos(theta), np.sin(theta), 0]
        vertices += [R1*np.cos(theta), R1*np.sin(theta), h,                   r, g, b, -np.cos(theta), -np.sin(theta), 0]
        vertices += [R1*np.cos(theta), R1*np.sin(theta), 0,                   r, g, b, 0, 0, -1]

    for i in range(N):
        theta = i * dtheta

        #            posición                                                  color    normales
        vertices += [R2*np.cos(theta), R2*np.sin(theta), 0,                   r, g, b, 0, 0, -1]
        vertices += [R2*np.cos(theta), R2*np.sin(theta), h-0.1,               r, g, b, 0, 0, 0]
        vertices += [(2*R2-R1)*np.cos(theta), (2*R2-R1)*np.sin(theta), h-0.1, r, g, b, 0, 0, -1]
        vertices += [(2*R2-R1)*np.cos(theta), (2*R2-R1)*np.sin(theta), h,     r, g, b, 0, 0, 1]
        vertices += [R1*np.cos(theta), R1*np.sin(theta), h,                   r, g, b, 0, 0, 1]
        vertices += [R1*np.cos(theta), R1*np.sin(theta), 0,                   r, g, b, -np.cos(theta), -np.sin(theta), 0]
    
    for i in range(6*N-6):
        indices += [i+6, i, i+7]
        indices += [i+1, i, i+7]

    for i in range(6*N-6,6*N):
        m = 6*N
        indices += [(i+6)%m, i%m, (i+7)%m]
        indices += [(i+1)%m, i%m, (i+7)%m]

    return bs.Shape(vertices, indices)