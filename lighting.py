from OpenGL.GL import *
import numpy as np

def setLightAttributes(lightingPipeline, viewPos, L, t):
    # Setting all uniform shader variables
    
        # night = (0.15, 0.15, 0.3)
        # day = (1, 1, 1)
        light_rg = (0.85/2)*np.cos(2*t*np.pi/L) + 0.85/2 + 0.15
        light_b = (0.7/2)*np.cos(2*t*np.pi/L) + 0.7/2 + 0.3

        # White light in all components: ambient, diffuse and specular.
        glUniform3f(glGetUniformLocation(lightingPipeline.shaderProgram, "La"), light_rg, light_rg, light_b)
        glUniform3f(glGetUniformLocation(lightingPipeline.shaderProgram, "Ld"), light_rg, light_rg, light_b) 
        glUniform3f(glGetUniformLocation(lightingPipeline.shaderProgram, "Ls"), light_rg, light_rg, light_b)

        # Object is barely visible at only ambient. Diffuse behavior is slightly red. Sparkles are white
        glUniform3f(glGetUniformLocation(lightingPipeline.shaderProgram, "Ka"), 0.5, 0.5, 0.5)
        glUniform3f(glGetUniformLocation(lightingPipeline.shaderProgram, "Kd"), 0.9, 0.9, 0.9)
        glUniform3f(glGetUniformLocation(lightingPipeline.shaderProgram, "Ks"), 0.4, 0.4, 0.4)

        # TO DO: Explore different parameter combinations to understand their effect!

        glUniform3f(glGetUniformLocation(lightingPipeline.shaderProgram, "lightPosition"), -7, 0, 7)
        glUniform3f(glGetUniformLocation(lightingPipeline.shaderProgram, "viewPosition"), viewPos[0], viewPos[1], viewPos[2])
        glUniform1ui(glGetUniformLocation(lightingPipeline.shaderProgram, "shininess"), 500)
        
        glUniform1f(glGetUniformLocation(lightingPipeline.shaderProgram, "constantAttenuation"), 0.0001)
        glUniform1f(glGetUniformLocation(lightingPipeline.shaderProgram, "linearAttenuation"), 0.03)
        glUniform1f(glGetUniformLocation(lightingPipeline.shaderProgram, "quadraticAttenuation"), 0.01)