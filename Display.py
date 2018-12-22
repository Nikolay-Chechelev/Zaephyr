from graphic import *
import pygame, thread

class Screen():
    def __init__(self, screen_w=1000, screen_h=800, bg_color=[30, 30, 30], mode=0):
        pygame.init()
        pygame.display.init()
        pygame.font.init()
        pygame.key.set_repeat(50, 50)
        # common variables
        self.avr_end_x = 400
        self.bg_col = bg_color # screen background color
        self.bright_border = [150, 150, 150]
        self.cell_color = [0, 64, 0]
        self.data_position = 0
        self.cell_step = 5
        self.dark_border = [80, 80, 80]
        self.display = pygame.display
        self.done = False # graphic loop flag
        self.Font = pygame.font.SysFont('COURIER', 20, 'bold')
        self.full_data = []
        self.graphic_line_color = [150, 150, 0]
        self.k_amp = 50000.0
        self.k_amp_step = 1.1
        self.loaded = False
        self.mode = 0 # screen mode (0 - static, 1 - resizable, 2 - fullscreen, any other - static)
        self.painted = True
        self.plot_end_y = 100
        self.plot_pos_x = 10 # null-point plots coordinates
        self.plot_pos_y = 10
        self.screen = None
        self.scr_h = screen_h # var for screen height
        self.scr_w = screen_w # var for screen width
        self.text_color = [0, 200, 200]
        # common plot variables
        self.plot_shift = 100
        self.averange = []
        self.texts = ['ECG Lead 1', 'ECG Lead 2', 'ECG Lead 3']
        self.plotter_shift = 10
        self.RR_dist = []

        self.avr_end_y = self.plot_end_y
        self.plot_end_x = self.scr_w - 2 * self.plot_pos_x

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
        Ploter(self.screen, 'Data', start=[10, 10], end=[500, 300], width=1, dark_color=[255, 255, 255],
                 color_bright=[0, 0, 0], cell_color=[0, 100, 0], graphic_line_color=[255, 255, 255],
                 cell_step=10, data = [], k=1, stretch=1).plot()
        return 0


    def load_data(self):
        while self.loaded and not self.painted:
            pass
        self.loaded = True
        self.painted = False
        return 0


    def loop(self, *args):  # Main graphic cycle.
        while not self.done: # Check loop flag

            while not self.loaded and self.painted:
                pass
            self.loaded = False

            self.screen.fill(self.bg_col)
            self.canvas()  # draw basic canvas
            self.display.flip()
            for event in pygame.event.get(): # processing of any events
                #print event
                if event.type == pygame.QUIT: # processing of QUIT event
                    self.done = True
                    pygame.quit()
                    break
                if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                    self.done = True
                    pygame.quit()
                    break
                if event.type == pygame.MOUSEBUTTONUP and event.button == 4:
                    if self.data_position < len(self.full_data[1]) - self.plot_shift - self.plot_len *2:
                        self.data_position += self.plot_shift
                if event.type == pygame.MOUSEBUTTONUP and event.button == 5:
                    if self.data_position > 0:
                        self.data_position -= self.plot_shift
                if event.type == pygame.KEYDOWN and event.key == 283:
                    self.k_amp *= self.k_amp_step
                if event.type == pygame.KEYDOWN and event.key == 282:
                    self.k_amp /= self.k_amp_step
            self.painted = True
        return self.done

    def run(self, done):
        self.done = not done  # set loop flag
        thread.start_new(self.loop, (None,)) # starting new thread with graphic loop
        return self.done

