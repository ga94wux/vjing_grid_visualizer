from OpenGL.GL import *
from OpenGL.GLU import gluPerspective, gluLookAt
import glfw
import numpy as np
import time
import colorsys

class Renderer:
    def __init__(self, param):
        self.amp = 3.0
        self.freq = 1.0
        self.speed = 2.0
        self.rotation_speed = 20.0
        self.zoom = 50.0
        self.color_hue = 130.0
        self.sensitivity = 100.0
        self.auto_mode = False
        self.time_start = time.time()

        self.audio = None
        param.updated.connect(self.set_params)

    def set_audio_source(self, audio):
        self.audio = audio

    def set_params(self, amp, freq, speed, rot, zoom, color_hue, sensitivity, auto_mode):
        self.amp = amp
        self.freq = freq
        self.speed = speed
        self.rotation_speed = rot
        self.zoom = zoom
        self.color_hue = color_hue
        self.sensitivity = sensitivity
        self.auto_mode = auto_mode

    def draw_grid(self):
        grid_size = 30
        spacing = 1.0
        t = (time.time() - self.time_start) * self.speed

        # Audio-Reaktivität im Automatikmodus
        if self.auto_mode and self.audio:
            amp_total = self.audio.bass_energy * self.sensitivity / 100
            hue = (self.audio.mid_energy * self.sensitivity * 2) % 360
            self.color_hue = hue
            speed = self.audio.global_level * self.sensitivity
        else:
            amp_total = self.amp
            speed = self.speed

        t = (time.time() - self.time_start) * speed
        r, g, b = colorsys.hsv_to_rgb(self.color_hue / 360.0, 1.0, 1.0)
        glColor3f(r, g, b)

        glBegin(GL_LINES)
        for i in range(grid_size):
            for j in range(grid_size):
                x = (i - grid_size / 2) * spacing
                z = (j - grid_size / 2) * spacing
                dist = np.sqrt(x**2 + z**2)
                y = amp_total * np.sin(self.freq * dist - t)

                glVertex3f(x, y, z)
                y2 = amp_total * np.sin(self.freq * (dist + spacing) - t)
                glVertex3f(x + spacing, y2, z)

                y3 = amp_total * np.sin(self.freq * np.sqrt(x**2 + (z + spacing)**2) - t)
                glVertex3f(x, y, z)
                glVertex3f(x, y3, z + spacing)
        glEnd()

    def run(self):
        if not glfw.init():
            return
        window = glfw.create_window(900, 700, "OpenGL Grid Visualizer", None, None)
        if not window:
            glfw.terminate()
            return
        glfw.make_context_current(window)

        glEnable(GL_DEPTH_TEST)
        glClearColor(0.05, 0.05, 0.08, 1.0)

        while not glfw.window_should_close(window):
            width, height = glfw.get_framebuffer_size(window)
            glViewport(0, 0, width, height)
            glMatrixMode(GL_PROJECTION)
            glLoadIdentity()
            gluPerspective(45, width / float(height), 0.1, 1000.0)
            glMatrixMode(GL_MODELVIEW)

            glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
            glLoadIdentity()

            eye_y = 8.0
            eye_z = self.zoom
            gluLookAt(0.0, eye_y, eye_z, 0.0, 0.0, 0.0, 0.0, 1.0, 0.0)
            glRotatef((time.time() - self.time_start) * self.rotation_speed % 360, 0, 1, 0)

            self.draw_grid()

            glfw.swap_buffers(window)
            glfw.poll_events()

        glfw.terminate()
