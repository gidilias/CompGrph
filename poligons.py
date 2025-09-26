import pygame
import math
import numpy as np
from OpenGL.GL import *
from OpenGL.GL.shaders import compileProgram, compileShader

WINDOW_WIDTH = 500
WINDOW_HEIGHT = 500

VERTEX_SHADER_SOURCE = """
#version 330 core
layout (location = 0) in vec2 vPosition;
layout (location = 1) in vec3 vColor;
out vec3 fragColor;
void main() {
    gl_Position = vec4(vPosition, 0.0, 1.0);
    fragColor = vColor;
}
"""

FRAGMENT_SHADER_SOURCE = """
#version 330 core
in vec3 fragColor;
out vec4 outColor;
void main() {
    outColor = vec4(fragColor, 1.0);
}
"""

def compile_shaders():
    vertex_shader = compileShader(VERTEX_SHADER_SOURCE, GL_VERTEX_SHADER)
    fragment_shader = compileShader(FRAGMENT_SHADER_SOURCE, GL_FRAGMENT_SHADER)
    return compileProgram(vertex_shader, fragment_shader)

def create_ellipse():
    vertices = []
    colors = []
    vertices.extend([-0.6, 0.5])
    colors.extend([1.0, 0.0, 0.0])
    segments = 50
    radius_x = 0.2
    radius_y = 0.15
    for i in range(segments + 1):
        angle = 2.0 * math.pi * i / segments
        x = -0.6 + math.cos(angle) * radius_x
        y = 0.5 + math.sin(angle) * radius_y * 0.6
        vertices.extend([x, y])
        colors.extend([1.0, 0.0, 0.0])
    return np.array(vertices, dtype=np.float32), np.array(colors, dtype=np.float32)

def create_triangle():
    vertices = []
    colors = []
    size = 0.3
    height = size * math.sqrt(3) / 2
    vertices.extend([0.0, 0.5 + height/2])
    colors.extend([1.0, 0.0, 0.0])
    vertices.extend([-size/2, 0.5 - height/2])
    colors.extend([0.0, 1.0, 0.0])
    vertices.extend([size/2, 0.5 - height/2])
    colors.extend([0.0, 0.0, 1.0])
    return np.array(vertices, dtype=np.float32), np.array(colors, dtype=np.float32)

def create_circle():
    vertices = []
    colors = []
    vertices.extend([0.6, 0.5])
    colors.extend([1.0, 0.0, 0.0])
    segments = 50
    radius = 0.18
    for i in range(segments + 1):
        angle = 2.0 * math.pi * i / segments
        x = 0.6 + math.cos(angle) * radius
        y = 0.5 + math.sin(angle) * radius
        vertices.extend([x, y])
        if angle >= math.pi and angle <= 3*math.pi/2:
            colors.extend([0.0, 0.0, 0.0])
        else:
            angle_normalized = angle / (2 * math.pi)
            if angle_normalized > 0.75 or angle_normalized < 0.25:
                gradient = 0.3
            else:
                gradient = 0.7
            colors.extend([gradient, 0.0, 0.0])
    return np.array(vertices, dtype=np.float32), np.array(colors, dtype=np.float32)

def create_nested_squares():
    vertices = []
    colors = []
    sizes = [0.6, 0.5, 0.4, 0.3, 0.2, 0.1]
    center_x, center_y = 0.0, -0.3
    for i, size in enumerate(sizes):
        half_size = size / 2
        square_vertices = []
        for j in range(4):
            angle = math.pi/4 + j * math.pi/2
            x = center_x + math.cos(angle) * half_size
            y = center_y + math.sin(angle) * half_size
            square_vertices.extend([x, y])
        strip_order = [0, 1, 3, 2]
        for idx in strip_order:
            vertices.extend([square_vertices[idx*2], square_vertices[idx*2+1]])
        if i % 2 == 0:
            for _ in range(4):
                colors.extend([1.0, 1.0, 1.0])
        else:
            for _ in range(4):
                colors.extend([0.0, 0.0, 0.0])
    return np.array(vertices, dtype=np.float32), np.array(colors, dtype=np.float32)

def setup_vao(vertices, colors):
    vao = glGenVertexArrays(1)
    vbo = glGenBuffers(1)
    glBindVertexArray(vao)
    interleaved_data = np.empty(len(vertices) // 2 * 5, dtype=np.float32)
    for i in range(len(vertices) // 2):
        interleaved_data[i*5] = vertices[i*2]
        interleaved_data[i*5+1] = vertices[i*2+1]
        interleaved_data[i*5+2] = colors[i*3]
        interleaved_data[i*5+3] = colors[i*3+1]
        interleaved_data[i*5+4] = colors[i*3+2]
    glBindBuffer(GL_ARRAY_BUFFER, vbo)
    glBufferData(GL_ARRAY_BUFFER, interleaved_data.nbytes, interleaved_data, GL_STATIC_DRAW)
    glVertexAttribPointer(0, 2, GL_FLOAT, GL_FALSE, 5 * 4, ctypes.c_void_p(0))
    glEnableVertexAttribArray(0)
    glVertexAttribPointer(1, 3, GL_FLOAT, GL_FALSE, 5 * 4, ctypes.c_void_p(2 * 4))
    glEnableVertexAttribArray(1)
    return vao, vbo, len(vertices) // 2

def main():
    pygame.init()
    pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT), pygame.DOUBLEBUF | pygame.OPENGL)
    pygame.display.set_caption("Task 2 Part 2 - 4 Objects Scene")
    shader_program = compile_shaders()
    glUseProgram(shader_program)
    ellipse_vao, ellipse_vbo, ellipse_vertex_count = setup_vao(*create_ellipse())
    triangle_vao, triangle_vbo, triangle_vertex_count = setup_vao(*create_triangle())
    circle_vao, circle_vbo, circle_vertex_count = setup_vao(*create_circle())
    squares_vao, squares_vbo, squares_vertex_count = setup_vao(*create_nested_squares())
    glClearColor(0.0, 0.0, 0.0, 1.0)
    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
        glClear(GL_COLOR_BUFFER_BIT)
        glBindVertexArray(ellipse_vao)
        glDrawArrays(GL_TRIANGLE_FAN, 0, ellipse_vertex_count)
        glBindVertexArray(triangle_vao)
        glDrawArrays(GL_TRIANGLES, 0, triangle_vertex_count)
        glBindVertexArray(circle_vao)
        glDrawArrays(GL_TRIANGLE_FAN, 0, circle_vertex_count)
        glBindVertexArray(squares_vao)
        for i in range(6):
            glDrawArrays(GL_TRIANGLE_STRIP, i*4, 4)
        pygame.display.flip()
        pygame.time.wait(16)
    glDeleteVertexArrays(4, [ellipse_vao, triangle_vao, circle_vao, squares_vao])
    glDeleteBuffers(4, [ellipse_vbo, triangle_vbo, circle_vbo, squares_vbo])
    glDeleteProgram(shader_program)
    pygame.quit()

if __name__ == "__main__":
    main()
