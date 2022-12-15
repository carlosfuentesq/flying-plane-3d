import glfw
import sys
import grafica.shapes as shapes
from OpenGL.GL import *
from modelos import *
from lighting import *
from controlador import *

if __name__ == "__main__":

    # Initialize glfw
    if not glfw.init():
        sys.exit()

    width = 1280
    height = 720

    window = glfw.create_window(width, height, "Flying Plane 3D", None, None)

    if not window:
        glfw.terminate()
        sys.exit()

    glfw.make_context_current(window)

    # We will use the global controller as communication with the callback function
    controller = Controller()

    # Connecting the callback function 'on_key' to handle keyboard events
    glfw.set_key_callback(window, controller.on_key)

    # Para chequear posición del mouse
    glfw.set_cursor_pos_callback(window, controller.cursor_pos_callback)

    # Se usará el método de Phong para la iluminación
    lightingTexturePipeline = ls.SimpleTexturePhongShaderProgram()
    lightingPipeline = ls.SimplePhongShaderProgram()

    # This shader program does not consider lighting
    mvpPipeline = es.SimpleModelViewProjectionShaderProgram()

    # Shader program para el texto
    textPipeline = tx.TextureTextRendererShaderProgram()

    # Setting up the clear screen color
    glClearColor(0.85, 0.85, 0.85, 1.0)

    # As we work in 3D, we need to check which part is in front,
    # and which one is at the back
    glEnable(GL_DEPTH_TEST)
    
    # Enabling transparencies
    glEnable(GL_BLEND)
    glBlendFunc(GL_SRC_ALPHA, GL_ONE_MINUS_SRC_ALPHA)

    # Creating shapes on GPU memory
    gpuAxis = es.toGPUShape(bs.createAxis(4))

    # Modelos del juego
    skybox = shapes.create_skybox()
    floor = shapes.create_floor()
    pipe_creator = pipeCreator()
    plane = Plane(textPipeline)
    counter = Counter(textPipeline)
    controller.set_obstacle(pipe_creator)
    controller.set_model(plane)

    # Condiciones iniciales
    t0 = glfw.get_time()
    last_pipe = glfw.get_time()
    k = 0
    mouse_pos = (
            2 * (controller.mousePos[0] - width / 2) / width,
            2 * (height / 2 - controller.mousePos[1]) / height
        )
    mouse_moving = False

    while not glfw.window_should_close(window):

        # Using GLFW to check for input events
        glfw.poll_events()

        # Getting the time difference from the previous iteration
        t1 = glfw.get_time()
        t_light = glfw.get_time()
        dt = t1 - t0
        plane_dt = t1 - t0
        t0 = t1

        if plane.win:
            plane_dt = 0.0
        if not plane.alive:
            dt = 0.0
            plane_dt *= 0.25
            if plane.zpos <= 0.01:
                plane_dt = 0.0

        # Getting the mouse location in opengl coordinates
        controller.GLMousePos = (
            2 * (controller.mousePos[0] - width / 2) / width,
            2 * (height / 2 - controller.mousePos[1]) / height
        )

        if controller.GLMousePos != mouse_pos:
            mouse_moving = True

        # Se selecciona la cámara
        if controller.camera == CAMERA_TP:
            controller.eye = np.array([-0.7, 0, plane.zpos+0.1])
            if plane.moving and mouse_moving:
                controller.at = np.array([0, -2*controller.GLMousePos[0], 2*controller.GLMousePos[1]])
            else:
                controller.at = np.array([0, 0, 0.5])

        elif controller.camera == CAMERA_SIDE:
            controller.eye = np.array([0, 0.99, 0.75])
            controller.at = np.array([0, 0, 0.7])

        elif controller.camera == CAMERA_FP:
            controller.eye = np.array([-0.3, 0, plane.zpos])
            if plane.moving:
                controller.at = np.array([0, 0, plane.velocity*0.1+plane.zpos])
                # Obs: reemplazar controller.at por np.array([0, -2*controller.GLMousePos[0], 2*controller.GLMousePos[1]])
                # para mover la camara con el mouse en primera persona, tal como se mueve en tercera persona
            else:
                controller.at = np.array([0, 0, 0.5])

        else:
            raise Exception()

        # Pausa
        if controller.pause_mode:
            dt = 0.0
            plane_dt = 0.0
            pipe_creator.creating = False
            t_light = 0.0

        # Actualizamos los modelos
        if len(pipe_creator.pipes) == int(sys.argv[1]) or plane.win:
            pipe_creator.creating = False
        if t1 - last_pipe > 2.5 and dt != 0.0:
            pipe_creator.createPipe()
            last_pipe = t1
        pipe_creator.update(dt)
        plane.update(plane_dt)

        # Se reconoce la lógica del juego
        if pipe_creator.pipes != []:
            pipe_creator.pipes[k].collide(plane)
            if pipe_creator.pipes[k].xpos < -0.71 and not plane.win:
                counter.update()
                if k+1 == int(sys.argv[1]):
                    plane.win = True
                elif k < int(sys.argv[1]):
                    k+=1

        # Filling or not the shapes depending on the controller state
        if (controller.fillPolygon):
            glPolygonMode(GL_FRONT_AND_BACK, GL_FILL)
        else:
            glPolygonMode(GL_FRONT_AND_BACK, GL_LINE)

        # Clearing the screen in both, color and depth
        glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
       
        # Proyección y matriz de vista
        projection = tr.ortho(-1, 1, -1, 1, 0.1, 100)
        projection = tr.perspective(70, float(width)/float(height), 0.1, 100)

        view = tr.lookAt(
            controller.eye,    # eye
            controller.at,     # at
            np.array([0,0,1])  # up
        )

        axis = np.array([1,-1,1])
        axis = axis / np.linalg.norm(axis)

        # The axis is drawn without lighting effects
        if controller.showAxis:
            glUseProgram(mvpPipeline.shaderProgram)
            glUniformMatrix4fv(glGetUniformLocation(mvpPipeline.shaderProgram, "projection"), 1, GL_TRUE, projection)
            glUniformMatrix4fv(glGetUniformLocation(mvpPipeline.shaderProgram, "view"), 1, GL_TRUE, view)
            glUniformMatrix4fv(glGetUniformLocation(mvpPipeline.shaderProgram, "model"), 1, GL_TRUE, tr.identity())
            mvpPipeline.drawShape(gpuAxis, GL_LINES)
        
        # Dibujamos los modelos
        glUseProgram(lightingPipeline.shaderProgram)
        setLightAttributes(lightingPipeline, controller.eye, int(sys.argv[2]), t_light)

        glUniformMatrix4fv(glGetUniformLocation(lightingPipeline.shaderProgram, "projection"), 1, GL_TRUE, projection)
        glUniformMatrix4fv(glGetUniformLocation(lightingPipeline.shaderProgram, "view"), 1, GL_TRUE, view)
        
        # Se dibujan las tuberías y el avión
        pipe_creator.draw(lightingPipeline)
        plane.draw(lightingPipeline)

        glUseProgram(lightingTexturePipeline.shaderProgram)
        setLightAttributes(lightingTexturePipeline, controller.eye, int(sys.argv[2]), t_light)
        
        glUniformMatrix4fv(glGetUniformLocation(lightingTexturePipeline.shaderProgram, "projection"), 1, GL_TRUE, projection)
        glUniformMatrix4fv(glGetUniformLocation(lightingTexturePipeline.shaderProgram, "view"), 1, GL_TRUE, view)

        # Se dibuja la skybox y el piso
        sg.drawSceneGraphNode(skybox, lightingTexturePipeline, "model")
        sg.drawSceneGraphNode(floor, lightingTexturePipeline, "model")

        # Se usa el shader program correspondiente al texto
        glUseProgram(textPipeline.shaderProgram)

        # Se dibuja el texto
        counter.draw(textPipeline)

        if not plane.alive:
            plane.wasted(textPipeline)
        if plane.win:
            plane.mission_passed(textPipeline)

        # Once the drawing is rendered, buffers are swap so an uncomplete drawing is never seen.
        glfw.swap_buffers(window)

    glfw.terminate()