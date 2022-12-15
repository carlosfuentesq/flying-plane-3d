from modelos import Plane, pipeCreator
from typing import Union
import numpy as np
import glfw
import sys

CAMERA_TP   = 1
CAMERA_SIDE = 2
CAMERA_FP   = 3

# A class to store the application control
class Controller:
    model: Union['Plane', None]
    obstacle: Union['pipeCreator', None]

    def __init__(self):
        self.background = None
        self.model = None
        self.obstacle = None
        self.fillPolygon = True
        self.showAxis = False
        self.camera = CAMERA_TP
        self.mousePos = (0.0, 0.0)
        self.GLMousePos = (0.0, 0.0)  # 2 * (controller.mousePos[0] - width / 2) / width
        self.eye = np.array([-0.99, 0, 0.9])
        self.at = np.array([-0.5, -self.GLMousePos[0], self.GLMousePos[1]])
        self.pause_mode = False

    def set_obstacle(self, o):
        self.obstacle = o

    def set_model(self, m):
        self.model = m

    def on_key(self, window, key, scancode, action, mods):

        if action != glfw.PRESS:
            return

        if key == glfw.KEY_P:
            self.pause_mode = not self.pause_mode

        elif key == glfw.KEY_W and action == glfw.PRESS:
            self.model.start()
            self.obstacle.start()
            self.model.jump()

        elif key == glfw.KEY_SPACE:
            self.fillPolygon = not self.fillPolygon

        elif key == glfw.KEY_LEFT_CONTROL:
            self.showAxis = not self.showAxis

        elif key == glfw.KEY_1:
            self.camera = CAMERA_TP

        elif key == glfw.KEY_2:
            self.camera = CAMERA_SIDE

        elif key == glfw.KEY_3:
            self.camera = CAMERA_FP

        elif key == glfw.KEY_ESCAPE:
            sys.exit()

    # Para chequear la posición del mouse
    def cursor_pos_callback(self, window, x, y):
        self.mousePos = (x, y)
