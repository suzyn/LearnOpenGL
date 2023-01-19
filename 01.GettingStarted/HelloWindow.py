import glfw
from OpenGL.GL import *


def framebuffer_size_callback(window, width, height):
    glViewport(0, 0, width, height)    
    
def processInput(window):
    if(glfw.get_key(window, glfw.KEY_ESCAPE) == glfw.PRESS):
        glfw.set_window_should_close(window, True)

def main():
    glfw.init() 
    glfw.window_hint(glfw.CONTEXT_VERSION_MAJOR, 3) 
    glfw.window_hint(glfw.CONTEXT_VERSION_MINOR, 3)
    glfw.window_hint(glfw.OPENGL_PROFILE, glfw.OPENGL_CORE_PROFILE)
    
    window = glfw.create_window(800, 600, "Hello Window", None, None)
    if(window == None):
        print("Failed to create GLFW window")
        glfw.terminate()
        return -1
    
    glfw.make_context_current(window)
    glfw.set_framebuffer_size_callback(window, framebuffer_size_callback)
    
    while(glfw.window_should_close(window)==False): # window closed when glfw.window_should_close() is True
        # input
        processInput(window)
        
        # render
        glClearColor(0.2, 0.3, 0.3, 1.0)
        glClear(GL_COLOR_BUFFER_BIT)
        
        # check and call events and swap the buffers
        glfw.swap_buffers(window)
        glfw.poll_events()

    glfw.terminate()
    return 0
    
if __name__ == "__main__":
    main()