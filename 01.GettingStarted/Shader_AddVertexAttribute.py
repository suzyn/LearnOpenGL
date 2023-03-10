import sys 
import numpy as np 
import math

import glfw
from OpenGL.GL import *

### SHADERS  
vertex_shader_source = """
    # version 330 core 

    layout (location = 0) in vec3 aPos;
    layout (location = 1) in vec3 aColor;
    
    out vec3 ourColor;
    
    void main()
    {
        gl_Position = vec4(aPos, 1.0);
        ourColor = aColor;   
    }
"""
fragment_shader_source = """
    # version 330 core
    
    out vec4 FragColor;
    in  vec3 ourColor;
    
    void main()
    {
        FragColor = vec4(ourColor, 1.0);
    }
"""

### FUNCTIONS 
def framebuffer_size_callback(window, width, height):
    glViewport(0, 0, width, height)    

# process all input 
def processInput(window):
    if(glfw.get_key(window, glfw.KEY_ESCAPE) == glfw.PRESS):
        glfw.set_window_should_close(window, True)

# build and compile our shader program  
def set_shader_program():
    # create vertex shader 
    vertex_shader = glCreateShader(GL_VERTEX_SHADER)
    glShaderSource(vertex_shader, vertex_shader_source)
    glCompileShader(vertex_shader)
    
    # check for shader compile error 
    success = glGetShaderiv(vertex_shader, GL_COMPILE_STATUS)
    if not success:
        info_log = glGetShaderInfoLog(vertex_shader, 512, None, info_log)
        print("ERROR::SHADER::VERTEX::COMPILATION_FAILED ", info_log)
    
    # fragment shader 
    fragment_shader = glCreateShader(GL_FRAGMENT_SHADER)
    glShaderSource(fragment_shader, fragment_shader_source)
    glCompileShader(fragment_shader)
    
    # check for shader compile errors
    success = glGetShaderiv(fragment_shader, GL_COMPILE_STATUS)
    if not success:
       info_log = glGetShaderInfoLog(fragment_shader, 512, None)
       print("ERROR::SHADER::FRAGMENT::COMPILATION_FAILED ", info_log) 

    # link shaders 
    shader_program = glCreateProgram()
    glAttachShader(shader_program, vertex_shader)
    glAttachShader(shader_program, fragment_shader)
    glLinkProgram(shader_program)
    
    # check for linking errors
    success = glGetProgramiv(shader_program, GL_LINK_STATUS)
    if not success:
        info_log = glGetProgramInfoLog(shader_program, 512, None)
        print("ERROR::SHADER::PROGRAM::LINKING_FAILED ", info_log)
    
    glDeleteShader(vertex_shader)
    glDeleteShader(fragment_shader)
    
    return shader_program

def set_triangle():
    vertices = [
                   # positions        # colors 
                   -0.5, -0.5, 0.0,   0.0, 1.0, 0.0,    # bottom left
                    0.5, -0.5, 0.0,   1.0, 0.0, 0.0,    # bottom right
                    0.0,  0.5, 0.0,   0.0, 0.0, 1.0     # top 
               ]
    vertices = np.array(vertices, dtype=np.float32)
    
    return vertices

def main(*args):
    glfw.init() 
    glfw.window_hint(glfw.CONTEXT_VERSION_MAJOR, 3) 
    glfw.window_hint(glfw.CONTEXT_VERSION_MINOR, 3)
    glfw.window_hint(glfw.OPENGL_PROFILE, glfw.OPENGL_CORE_PROFILE)
    
    window = glfw.create_window(800, 600, "Shader", None, None)
    if(window == None):
        print("Failed to create GLFW window")
        glfw.terminate()
        return -1
    
    glfw.make_context_current(window)
    glfw.set_framebuffer_size_callback(window, framebuffer_size_callback)

    is_wireframe = args[0]
    
    shader_program = set_shader_program()
    vertices = set_triangle()
        
    VAO = glGenVertexArrays(1)
    VBO = glGenBuffers(1)
    
    glBindVertexArray(VAO)
    glBindBuffer(GL_ARRAY_BUFFER, VBO)
    glBufferData(GL_ARRAY_BUFFER, vertices, GL_STATIC_DRAW)
    
    # position attribute
    glVertexAttribPointer(0, 3, GL_FLOAT, GL_FALSE, 6 * sizeof(GLfloat), ctypes.c_void_p(0))
    glEnableVertexAttribArray(0)
    
    # color attribute 
    glVertexAttribPointer(1, 3, GL_FLOAT, GL_FALSE, 6 * sizeof(GLfloat), ctypes.c_void_p(3*sizeof(GLfloat)))
    glEnableVertexAttribArray(1)
        
    if is_wireframe:
        glPolygonMode(GL_FRONT_AND_BACK, GL_LINE)
        
    # activate shader  
    glUseProgram(shader_program)
    
    # render loop 
    while(glfw.window_should_close(window)==False): 
        # input
        processInput(window)
        
        # render
        glClearColor(0.2, 0.3, 0.3, 1.0)
        glClear(GL_COLOR_BUFFER_BIT)
        
        # render the triangle 
        glBindVertexArray(VAO)
        glDrawArrays(GL_TRIANGLES, 0, 3)
        
        # check and call events and swap the buffers
        glfw.swap_buffers(window)
        glfw.poll_events()
    
    glDeleteVertexArrays(1, VAO)
    glDeleteBuffers(1, VBO)
    glDeleteProgram(shader_program)

    glfw.terminate()
    return 0
    
if __name__ == "__main__":
    main(False)