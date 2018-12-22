import pygame

class Line():
    def __init__(self, master, start=[0, 0], end=[10, 10], width=1, color=[255, 255, 255]):
        self.master = master  # Parent object
        self.start = start  # start point coordinates
        self.end = end  # end point coordinates
        self.width = width
        self.color = color
        pass

    def plot(self):
        pygame.draw.line(self.master, self.color, self.start, self.end, self.width)  # drawing line
        return True


class Frame:
    def __init__(self, master, start=[0, 0], end=[10, 10], width=1, dark_color=[255, 255, 255],
                 color_bright=[0, 0, 0]):
        self.master = master
        self.start = start
        self.end = end
        self.width = width
        self.dark_color = dark_color
        self.color_bright = color_bright

    def plot(self):
        Line(self.master, self.start, [self.end[0], self.start[1]], self.width, self.color_bright).plot()
        Line(self.master, [self.end[0], self.start[1]], self.end, self.width, self.dark_color).plot()
        Line(self.master, self.end, [self.start[0], self.end[1]], self.width, self.dark_color).plot()
        Line(self.master, [self.start[0], self.end[1]], self.start, self.width, self.color_bright).plot()
        return True

class Ploter:
    def __init__(self, master, name, start=[0, 0], end=[10, 10], width=1, dark_color=[255, 255, 255],
                 color_bright=[0, 0, 0], cell_color=[0, 100, 0], graphic_line_color=[255, 255, 255],
                 cell_step=10, data = [], k=1, stretch=1):
        self.master = master
        self.start = start
        self.end = end
        self.width = width
        self.dark_color = dark_color
        self.color_bright = color_bright
        self.name = name
        self.cell_color = cell_color
        self.cell_step = cell_step
        self.text_color = [0, 200, 200]
        self.Font = pygame.font.SysFont('COURIER', 20, 'bold')
        self.data = data
        self.line_color = graphic_line_color
        self.k = k
        self.stretch = stretch
        self.cell_voltage = (1.0 / self.k) * 1000

    def plot(self):
        for i in range(self.start[0], self.end[0], self.cell_step): # drawing graphic cells
            Line(self.master, [i, self.start[1]], [i, self.end[1]],
                 1, self.cell_color).plot()
            # drawing vertical lines

        for i in range(self.start[1], self.end[1], self.cell_step):
            Line(self.master,[self.start[0], i], [self.end[0], i],
                 1, self.cell_color).plot()  # drawing horizontal lines

        data_shift = (self.end[1] - self.start[1]) / 2 + self.start[1]

        for i in range(1, len(self.data)):
            x1 = self.start[0] + (i - 1) * self.stretch
            y1 = 0 - self.k * self.data[i - 1] + data_shift
            x2 = self.start[0] + i * self.stretch
            y2 = 0 - self.k * self.data[i] + data_shift

            Line(self.master, [x1, y1], [x2, y2], 2, self.line_color).plot()


        Frame(self.master, self.start, self.end, self.width, self.dark_color, self.color_bright).plot()
        text1 = pygame.font.Font.render(self.Font, self.name, True, self.text_color)
        text2 = pygame.font.Font.render(self.Font, 'Voltage = '+str(self.cell_voltage) + 'mV/cell', True, self.text_color)
        self.master.blit(text1, [self.start[0] + 2, self.start[1] + 2])
        self.master.blit(text2, [self.start[0] + 2, self.end[1] - 20])
        return True

    def load_data(self, data):
        self.data = data[0, len(self.data)-1]
        return 0

