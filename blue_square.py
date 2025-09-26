import glfw
from OpenGL.GL import *
import numpy as np

vertex_shader_source = """
#version 330
layout(location = 0) in vec3 aPos;
void main() {
    gl_Position = vec4(aPos, 1.0);
}
"""

fragment_shader_source = """
#version 330
out vec4 FragColor;
void main() {
    FragColor = vec4(0.0, 0.0, 1.0, 1.0);
}
"""

def compile_shader(source, shader_type):
    shader = glCreateShader(shader_type)
    glShaderSource(shader, source)
    glCompileShader(shader)
    if not glGetShaderiv(shader, GL_COMPILE_STATUS):
        raise RuntimeError(glGetShaderInfoLog(shader).decode())
    return shader

def main():
    if not glfw.init():
        return
    window = glfw.create_window(500, 500, "Blue Square", None, None)
    glfw.make_context_current(window)

    vertex_shader = compile_shader(vertex_shader_source, GL_VERTEX_SHADER)
    fragment_shader = compile_shader(fragment_shader_source, GL_FRAGMENT_SHADER)

    shader_program = glCreateProgram()
    glAttachShader(shader_program, vertex_shader)
    glAttachShader(shader_program, fragment_shader)
    glLinkProgram(shader_program)

    vertices = np.array([
        -0.5,  0.5, 0.0,
        -0.5, -0.5, 0.0,
         0.5, -0.5, 0.0,
        -0.5,  0.5, 0.0,
         0.5, -0.5, 0.0,
         0.5,  0.5, 0.0
    ], dtype=np.float32)

    VAO = glGenVertexArrays(1)
    VBO = glGenBuffers(1)
    glBindVertexArray(VAO)
    glBindBuffer(GL_ARRAY_BUFFER, VBO)
    glBufferData(GL_ARRAY_BUFFER, vertices.nbytes, vertices, GL_STATIC_DRAW)

    glVertexAttribPointer(0, 3, GL_FLOAT, GL_FALSE, 0, None)
    glEnableVertexAttribArray(0)

    while not glfw.window_should_close(window):
        glClear(GL_COLOR_BUFFER_BIT)
        glUseProgram(shader_program)
        glBindVertexArray(VAO)
        glDrawArrays(GL_TRIANGLES, 0, 6)
        glfw.swap_buffers(window)
        glfw.poll_events()

    glfw.terminate()

if __name__ == "__main__":
    main()
