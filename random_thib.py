import pygame
import numpy as np
import math
from OpenGL.GL import *
from OpenGL.GL.shaders import compileProgram, compileShader

VERTEX_SHADER = """
#version 330 core
layout(location = 0) in vec2 vPosition;
layout(location = 1) in vec3 vColor;
out vec3 fragColor;
void main() {
    gl_Position = vec4(vPosition, 0.0, 1.0);
    fragColor = vColor;
}
"""

FRAGMENT_SHADER = """
#version 330 core
in vec3 fragColor;
out vec4 outColor;
void main() {
    outColor = vec4(fragColor, 1.0);
}
"""

def create_circle(center_x, center_y, radius, color):
    vertices, colors = [], []
    vertices.extend([center_x, center_y])
    colors.extend(color)
    segments = 40
    for i in range(segments + 1):
        angle = 2 * math.pi * i / segments
        x = center_x + math.cos(angle) * radius
        y = center_y + math.sin(angle) * radius
        vertices.extend([x, y])
        colors.extend(color)
    return np.array(vertices, dtype=np.float32), np.array(colors, dtype=np.float32), GL_TRIANGLE_FAN, segments + 2

def create_square(center_x, center_y, size, color):
    half = size / 2
    coords = [
        [center_x - half, center_y + half],
        [center_x - half, center_y - half],
        [center_x + half, center_y - half],
        [center_x - half, center_y + half],
        [center_x + half, center_y - half],
        [center_x + half, center_y + half]
    ]
    vertices, colors = [], []
    for x, y in coords:
        vertices.extend([x, y])
        colors.extend(color)
    return np.array(vertices, dtype=np.float32), np.array(colors, dtype=np.float32), GL_TRIANGLES, 6

def create_triangle(center_x, center_y, size, color):
    height = size * math.sqrt(3) / 2
    coords = [
        [center_x, center_y + height / 2],
        [center_x - size / 2, center_y - height / 2],
        [center_x + size / 2, center_y - height / 2]
    ]
    vertices, colors = [], []
    for x, y in coords:
        vertices.extend([x, y])
        colors.extend(color)
    return np.array(vertices, dtype=np.float32), np.array(colors, dtype=np.float32), GL_TRIANGLES, 3

def setup_vao(vertices, colors):
    vao = glGenVertexArrays(1)
    vbo = glGenBuffers(1)
    interleaved = np.empty(len(vertices)//2 * 5, dtype=np.float32)
    for i in range(len(vertices)//2):
        interleaved[i*5:i*5+5] = [vertices[i*2], vertices[i*2+1], colors[i*3], colors[i*3+1], colors[i*3+2]]
    glBindVertexArray(vao)
    glBindBuffer(GL_ARRAY_BUFFER, vbo)
    glBufferData(GL_ARRAY_BUFFER, interleaved.nbytes, interleaved, GL_STATIC_DRAW)
    glVertexAttribPointer(0, 2, GL_FLOAT, GL_FALSE, 5*4, ctypes.c_void_p(0))
    glEnableVertexAttribArray(0)
    glVertexAttribPointer(1, 3, GL_FLOAT, GL_FALSE, 5*4, ctypes.c_void_p(8))
    glEnableVertexAttribArray(1)
    return vao, vbo, len(vertices)//2

def main():
    pygame.init()
    pygame.display.set_mode((500, 500), pygame.OPENGL | pygame.DOUBLEBUF)
    pygame.display.set_caption("Three Shapes on One Line")

    shader = compileProgram(
        compileShader(VERTEX_SHADER, GL_VERTEX_SHADER),
        compileShader(FRAGMENT_SHADER, GL_FRAGMENT_SHADER)
    )
    glUseProgram(shader)

    circle = create_circle(-0.6, 0.0, 0.2, [1.0, 0.0, 0.0])       # красный
    square = create_square(0.0, 0.0, 0.4, [0.0, 1.0, 0.0])        # зелёный
    triangle = create_triangle(0.6, 0.0, 0.4, [0.0, 0.0, 1.0])    # синий

    shapes = [circle, square, triangle]
    vao_list = []
    for shape in shapes:
        vertices, colors, mode, count = shape
        vao, vbo, _ = setup_vao(vertices, colors)
        vao_list.append((vao, mode, count))

    glClearColor(0.0, 0.0, 0.0, 1.0)

    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
        glClear(GL_COLOR_BUFFER_BIT)
        for vao, mode, count in vao_list:
            glBindVertexArray(vao)
            glDrawArrays(mode, 0, count)
        pygame.display.flip()
        pygame.time.wait(16)
    pygame.quit()

if __name__ == "__main__":
    main()
