import pygame, thread, random, time, math
import numpy.fft as fft

class Screen():
    def __init__(self, screen_w=1000, screen_h=500, bg_color=[10, 10, 10], mode=0):
        pygame.init()
        pygame.display.init()
        pygame.font.init()
        # common variables
        self.scr_w = screen_w # var for screen width
        self.scr_h = screen_h # var for screen height
        self.bg_col = bg_color # screen background color
        self.mode = 0 # screen mode (0 - static, 1 - resizable, 2 - fullscreen, any other - static)
        self.done = False # graphic loop flag
        self.display = pygame.display
        self.screen = None
        # common plot variables
        self.cell_color = [0, 64, 0]
        self.bright_border = [150, 150, 150]
        self.dark_border = [80, 80, 80]
        self.graphic_line_color = [200, 200, 0]
        self.text_color = [0, 200, 200]
        self.cell_step = 10
        self.plot_pos_x = 10 # null-point plots coordinates
        self.plot_pos_y = 10
        self.plot_end_x = self.scr_w - 2 * self.plot_pos_x
        self.channel_height = 100 # height of 1-channel plot
        self.plot_end_y = 100
        self.plot_len = self.plot_end_x - self.plot_pos_x # length of graphic plot
        self.linear_channels = 1
        self.dFreq = None
        self.Font = pygame.font.SysFont('COURIER', 20, 'bold')
        self.data = {}
        self.loaded = False
        self.painted = True
        self.k_amp = 1.0
        self.k_amp_step = 1.1

        if mode == 0:
            self.mode = 0
        if mode == 1: # if it used FULLSCREEN mode
            # before initializing read real monitor height and width
            self.scr_w = self.display.Info().current_w
            self.scr_h = self.display.Info().current_h
            self.plot_len = self.plot_end_x - self.plot_pos_x  # length of graphic plot
            self.mode = pygame.FULLSCREEN

    def main_screen(self):
        self.screen = self.display.set_mode([self.scr_w, self.scr_h], self.mode)
        self.plot_end_x = self.scr_w - self.plot_pos_x
        self.plot_len = self.plot_end_x - self.plot_pos_x # length of graphic plot
        return not self.done

    def canvas(self):
        for i in range(self.plot_pos_x, self.plot_end_x, self.cell_step): # drawing graphic cells
            if i % self.cell_step == 0:
                pygame.draw.line(self.screen, self.cell_color,
                                 [i, self.plot_pos_y],
                                 [i, self.plot_end_y], 1)  # drawing vertical lines

        for j in range(self.plot_pos_y, self.plot_end_y, self.cell_step):
            pygame.draw.line(self.screen, self.cell_color,
                             [self.plot_pos_x, j],
                             [self.plot_end_x, j], 1)  # drawing horizontal lines

        pygame.draw.line(self.screen, self.dark_border,
                         [self.plot_pos_x, self.plot_pos_y],
                         [self.plot_end_x, self.plot_pos_y], 2)

        for i in range(1, self.linear_channels):
            pygame.draw.line(self.screen, self.bright_border,
                             [self.plot_pos_x, i*self.channel_height + self.plot_pos_y],
                             [self.plot_end_x, i*self.channel_height + self.plot_pos_y], 2)  # upper border line

        pygame.draw.line(self.screen, self.dark_border,
                         [self.plot_pos_x, self.plot_pos_y],
                         [self.plot_pos_x, self.plot_end_y], 2) # left border line

        pygame.draw.line(self.screen, self.bright_border,
                         [self.plot_end_x, self.plot_pos_y],
                         [self.plot_end_x, self.plot_end_y], 2)  # right border line

        pygame.draw.line(self.screen, self.bright_border,
                         [self.plot_pos_x, self.plot_end_y],
                         [self.plot_end_x, self.plot_end_y], 2)  # lower border line

        #self.display.flip() # update screen
        return 0


    def load_data(self, data):
        while self.loaded and not self.painted:
            pass
        self.loaded = True
        self.painted = False
        self.data = data
        self.linear_channels = len(data)
        self.plot_end_y = self.channel_height * self.linear_channels + self.plot_pos_y
        return 0

    def FFT_plot(self):
        return 0

    def loop(self, *args):  # Main graphic cycle.
        while not self.done: # Check loop flag
            while not self.loaded and self.painted:
                pass
            self.loaded = False

            self.screen.fill(self.bg_col)
            self.canvas()  # draw basic canvas
            for i in range(self.linear_channels):  # writing name for every channel
                text1 = pygame.font.Font.render(self.Font, self.data.keys()[i], True, self.text_color)
                self.screen.blit(text1, [self.plot_pos_x + 2, i * self.channel_height + self.plot_pos_y + 2])

            for i in range(len(self.data.keys())):
                if len(self.data.values()[i]) != self.plot_len:
                    print 'ERROR! Length of every channel should be equal to length of plot!', \
                        len(self.data.values()[i]), self.plot_len
                    return 0
                for x in range(self.plot_len - 1):
                    pygame.draw.line(self.screen, self.graphic_line_color,
                                     [x + self.plot_pos_x, self.k_amp*self.data.values()[i][x] +
                                      i * self.channel_height + self.channel_height / 2 + self.plot_pos_y],
                                     [x + 1 + self.plot_pos_x, self.k_amp*self.data.values()[i][x + 1] +
                                      i * self.channel_height + self.channel_height / 2 + self.plot_pos_y], 1)
            '''a = [fft.fft(self.data.values()[i]) for i in range(len(self.data))]
            for i in range(len(a)):
                for j in range(len(a[i])-1):
                    pygame.draw.line(self.screen, [255, 0, 0],
                                     [j + self.plot_pos_x, -int(a[i][j]/20) + i * self.channel_height + self.channel_height / 2 + self.plot_pos_y],
                                     [j + 1 + self.plot_pos_x, -int(a[i][j+1]/20) + i * self.channel_height + self.channel_height / 2 + self.plot_pos_y], 1)'''


            self.display.flip()
            for event in pygame.event.get(): # processing of any events
                if event.type == pygame.QUIT: # processing of QUIT event
                    self.done = True
                    pygame.quit()
                    break
                if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                    self.done = True
                    pygame.quit()
                    break
                if event.type == pygame.MOUSEBUTTONUP and event.button == 4:
                    self.k_amp *= self.k_amp_step
                if event.type == pygame.MOUSEBUTTONUP and event.button == 5:
                    self.k_amp /= self.k_amp_step
            self.painted = True
        return self.done

    def run(self, done):
        self.done = not done  # set loop flag
        thread.start_new(self.loop, (None,)) # starting new thread with graphic loop
        return self.done


data = {
    'Channel 1': [],
    'Channel 2': [],
    'Channel 3': [],
    'Channel 4': []
}


s = Screen(mode=1)
s.main_screen()
s.run(True)

while 1:
    data = {
        'Channel 1': [],
        'Channel 2': [],
        'Channel 3': [],
        'Channel 4': []
    }
    for i in range(len(data)):
        for j in range(s.plot_len):
            data[data.keys()[i]].append(20*math.sin(6.283 * j * 5 / 250))
    s.load_data(data)

