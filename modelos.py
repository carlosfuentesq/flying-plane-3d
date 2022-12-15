from OpenGL.GL import *
from typing import List
from random import uniform
from grafica.shapes import *
from grafica.off_obj_reader import readOBJ
import grafica.easy_shaders as es
import grafica.lighting_shaders as ls
import grafica.basic_shapes as bs
import grafica.scene_graph as sg
import grafica.transformations as tr
import grafica.text_renderer as tx
import grafica.gpu_shape as gs
import numpy as np

class Plane:

    def __init__(self, textPipeline):
        gpuPlane = es.toGPUShape(readOBJ('assets/plane2.obj', (0.95,0.95,0.95)), GL_REPEAT, GL_NEAREST)

        self.model = sg.SceneGraphNode("plane")
        self.model.transform = tr.identity()
        self.model.childs += [gpuPlane]
    
        # Creating texture with all characters
        textBitsTexture = tx.generateTextBitsTexture()

        # Moving texture to GPU memory
        gpuText3DTexture = tx.toOpenGLTexture(textBitsTexture)
        self.gpuMissionPassed = gs.GPUShape().initBuffers()
        self.gpuWasted = gs.GPUShape().initBuffers()
        textPipeline.setupVAO(self.gpuMissionPassed)
        textPipeline.setupVAO(self.gpuWasted)
        self.gpuMissionPassed.texture = gpuText3DTexture
        self.gpuWasted.texture = gpuText3DTexture

        self.alive = True
        self.moving = False
        self.zpos = 0.5
        self.velocity = 0
        self.win = False

    def draw(self, pipeline):
        self.model.transform = tr.matmul([tr.translate(-0.5, 0, self.zpos), tr.uniformScale(0.015), 
                                          tr.rotationX(np.pi/2), tr.rotationY(np.pi/2), tr.rotationX(-self.velocity*0.3)])
        sg.drawSceneGraphNode(self.model, pipeline, "model")
    
    def update(self, dt):
        if self.moving:
            self.velocity += -3*dt
            self.zpos += self.velocity*dt

        elif not self.moving:
            self.zpos = self.zpos
    
    def mission_passed(self, textPipeline):
        missionPassedShape = tx.textToShape('YOU WIN!', 0.05, 0.1)

        self.gpuMissionPassed.fillBuffers(missionPassedShape.vertices, missionPassedShape.indices, GL_STATIC_DRAW)

        glUniform4f(glGetUniformLocation(textPipeline.shaderProgram, "fontColor"), 0, 1, 0, 1)
        glUniform4f(glGetUniformLocation(textPipeline.shaderProgram, "backColor"), 0, 0, 0, 0)
        glUniformMatrix4fv(glGetUniformLocation(textPipeline.shaderProgram, "transform"), 1, GL_TRUE,
                           np.matmul(tr.translate(-0.44,0,0), tr.uniformScale(2)))
        textPipeline.drawCall(self.gpuMissionPassed)

    def wasted(self, textPipeline):
        wastedShape = tx.textToShape('GAME OVER', 0.05, 0.1)

        self.gpuWasted.fillBuffers(wastedShape.vertices, wastedShape.indices, GL_STATIC_DRAW)

        glUniform4f(glGetUniformLocation(textPipeline.shaderProgram, "fontColor"), 1, 0, 0, 1)
        glUniform4f(glGetUniformLocation(textPipeline.shaderProgram, "backColor"), 0, 0, 0, 0)
        glUniformMatrix4fv(glGetUniformLocation(textPipeline.shaderProgram, "transform"), 1, GL_TRUE,
                           np.matmul(tr.translate(-0.44,0,0), tr.uniformScale(2)))
        textPipeline.drawCall(self.gpuWasted)

    def jump(self):
        if not self.alive:
            return
        self.velocity = 0.8

    def start(self):
        self.moving = True

class Pipe:
    
    def __init__(self):
        
        gpuPipe = es.toGPUShape(createColorPipe(100, 1, 0.075, 0.1, 0, 0.75, 0), GL_REPEAT, GL_NEAREST)

        pipe = sg.SceneGraphNode('pipe')
        pipe.transform = tr.identity()
        pipe.childs += [gpuPipe]

        btm_pipe = sg.SceneGraphNode('btmPipe')
        btm_pipe.transform = tr.translate(0,0,-0.6)
        btm_pipe.childs += [pipe]

        top_pipe = sg.SceneGraphNode('topPipe')
        top_pipe.transform = tr.matmul([tr.translate(0,0,1.7), tr.rotationZ(np.pi), tr.scale(1, 1, -1)])
        top_pipe.childs += [pipe]

        pipes = sg.SceneGraphNode('bothPipes')
        rnd = uniform(-0.3,0.2)
        pipes.transform = tr.translate(1.5, 0, rnd)
        pipes.childs += [btm_pipe, top_pipe]

        transform_pipes = sg.SceneGraphNode('trPipes')
        transform_pipes.childs += [pipes]

        self.model = transform_pipes
        self.xpos = 1.5
        self.btm_pipe_height = rnd + 0.4
        self.top_pipe_height = rnd + 0.65

    def draw(self, pipeline):
        self.model.transform = tr.translate(self.xpos-1.5, 0, 0)
        sg.drawSceneGraphNode(self.model, pipeline, "model")

    def update(self, dt):
        self.xpos -= 0.4*dt
        
    def collide(self, plane: 'Plane'):
        # Colisiones simplificadas
        if (-0.7 <= self.xpos <= -0.3 and (plane.zpos < self.btm_pipe_height \
            or plane.zpos > self.top_pipe_height)) or plane.zpos <= 0.01 or plane.zpos >= 0.99:
                plane.alive = False

class pipeCreator:
    pipes: List['Pipe']

    def __init__(self):
        self.pipes = []
        self.creating = False

    def createPipe(self):
        if self.creating:
            self.pipes.append(Pipe())

    def draw(self, pipeline):
        for p in self.pipes:
            p.draw(pipeline)
            
    def start(self):
        self.creating = True

    def update(self, dt):
        for p in self.pipes:
            p.update(dt)

class Counter(object):
    def __init__(self, textPipeline):
        self.score = 0

        # Creating texture with all characters
        textBitsTexture = tx.generateTextBitsTexture()

        # Moving texture to GPU memory
        gpuText3DTexture = tx.toOpenGLTexture(textBitsTexture)
        self.gpuScoreText = gs.GPUShape().initBuffers()
        self.gpuScore = gs.GPUShape().initBuffers()
        textPipeline.setupVAO(self.gpuScoreText)
        textPipeline.setupVAO(self.gpuScore)
        self.gpuScoreText.texture = gpuText3DTexture
        self.gpuScore.texture = gpuText3DTexture
    
    def draw(self, textPipeline):
        
        scoreTextShape = tx.textToShape('SCORE', 0.05, 0.1)
        scoreShape = tx.textToShape(str(self.score), 0.05, 0.1)

        self.gpuScoreText.fillBuffers(scoreTextShape.vertices, scoreTextShape.indices, GL_STATIC_DRAW)
        self.gpuScore.fillBuffers(scoreShape.vertices, scoreShape.indices, GL_STREAM_DRAW)

        glUniform4f(glGetUniformLocation(textPipeline.shaderProgram, "fontColor"), 1, 1, 1, 1)
        glUniform4f(glGetUniformLocation(textPipeline.shaderProgram, "backColor"), 0, 0, 0, 0)
        glUniformMatrix4fv(glGetUniformLocation(textPipeline.shaderProgram, "transform"), 1, GL_TRUE,
                           tr.translate(0.715, 0.825, 0))
        textPipeline.drawCall(self.gpuScoreText)

        glUniform4f(glGetUniformLocation(textPipeline.shaderProgram, "fontColor"), 1, 1, 1, 1)
        glUniform4f(glGetUniformLocation(textPipeline.shaderProgram, "backColor"), 0, 0, 0, 0)
        glUniformMatrix4fv(glGetUniformLocation(textPipeline.shaderProgram, "transform"), 1, GL_TRUE,
                           tr.translate(0.917, 0.69, 0))
        textPipeline.drawCall(self.gpuScore)
    
    def update(self):
        self.score += 1