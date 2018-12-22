import serial, math, serial.tools.list_ports, time, thread
import pygame

class eeOnDo():
    def __init__(self):
        self.port_list = list(serial.tools.list_ports.comports()) # list of available ports
        self.com = ''
        self.eeOnDo = None
        self.connected = False
        self.run = False
        self.output_data = [[] for i in range(8)]

    def connect(self):
        print 'Number of COM-ports ' + str(len(self.port_list))
        i = 1
        while i < len(self.port_list): # counting all ports trying to connect them
            self.com = self.port_list[len(self.port_list) - i][0]
            print 'Checking port ' + self.port_list[i][0]
            self.eeOnDo = serial.Serial(self.com, '115200')
            try: # if it was successfully opened
                self.eeOnDo.write('|')
                time.sleep(0.1)
                self.eeOnDo.write('?')
                time.sleep(0.1)
            except:
                print 'The port ' + self.port_list[i][0] + ' may by busy with another process.'

            if self.eeOnDo.inWaiting():
                s = self.eeOnDo.read(self.eeOnDo.inWaiting())
                if 'eOnDo' in s:
                    print 'eeOnDo was successfully recognized and connected!' + self.com
                    break
            self.eeOnDo.close()
            i += 1

        if self.eeOnDo.isOpen():
            self.connected = True
            self.run = True
            return (True, self.com)
        else:
            self.com = ''
            return (False, self.com)

    def read(self, *argw):
        while self.run:
            while self.eeOnDo.inWaiting() >= 29:
                s = self.eeOnDo.read(29)
                if (ord(s[0]) == 255) and (ord(s[3]) == 221):
                    for i in range(8):
                        ch_data = ord(s[3*i + 5]) * 2**16 + ord(s[3*i + 6]) * 2**8 + ord(s[3*i + 7])
                        if ch_data > (2**23)-1:
                            ch_data = ch_data - 2**24
                        self.output_data[i].append(ch_data)

    def start_Flow(self):
        if self.connected:
            self.eeOnDo.write('|')
            time.sleep(0.1)
            self.eeOnDo.write('~')
            thread.start_new(self.read, (None,))
            return True
        return False

    def get_data(self):
        data = self.output_data
        self.output_data = [[] for i in range(8)]
        return data

    def stop_Flow(self):
        self.eeOnDo.write('|')
        time.sleep(0.1)
        self.eeOnDo.write('|')
        self.output_data = [[] for i in range(8)]
        self.run = False
        return True

class ee_Plot():
    def __init__(self, win_w=1000, win_h=540, bg_color=[0, 0, 0], cell_color=[0, 64, 0], plot_color=[128, 255, 0]
                 , cell_step=10):
        self.win_w = win_w
        self.win_h = win_h
        self.bg_color = bg_color
        self.cell_color = cell_color
        self.plot_color = plot_color
        self.cell_step = cell_step
        self.display = pygame.display
        self.screen = self.display.set_mode([self.win_w, self.win_h])
        self.done = False
        self.array = [[0 for j in range(self.win_w - 1)] for i in range(8)]


    def draw(self, cell_step, bitrate=24, amp=1000):
        while not self.done:
            self.screen.fill(self.bg_color)
            for i in range(0, self.win_w, self.cell_step):
                if i % self.cell_step == 0:
                    pygame.draw.line(self.screen, self.cell_color, [i, 0], [i, self.win_h], 1)
            for j in range(0, self.win_h, self.cell_step):
                    pygame.draw.line(self.screen, self.cell_color, [0, j], [self.win_w, j], 1)

            k = amp / 2.0 ** bitrate
            for i in range(len(self.array)):
                for j in range(1, len(self.array[i])):
                    pygame.draw.line(self.screen, self.plot_color,
                                     [j - 1, k * self.array[i][j - 1] + (i + 1) * self.win_h / (len(self.array)+1)],
                                     [j, k * self.array[i][j] + (i + 1) * self.win_h / (len(self.array)+1)], 1)

            self.display.flip()
            for event in pygame.event.get():  # if it was an event...
                if event.type == pygame.QUIT:  # if it was quit event, then quit app
                    self.done = True

                if event.type == pygame.MOUSEBUTTONDOWN and event.button == 4:
                    if self.cell_step > 2:
                        self.cell_step += 2
                if event.type == pygame.MOUSEBUTTONDOWN and event.button == 5:
                    if self.cell_step > 4:
                        self.cell_step -= 2

    def load_array(self, array):
        if len(array[0]) > 0:
            for i in range(len(array)):
                del self.array[i][0:len(array[i]) - 1]
                self.array[i] += array[i]


e = eeOnDo()
print e.connect()
print e.start_Flow()
p = ee_Plot()
thread.start_new(p.draw, (20,))
while 1:
    data = e.get_data()
    p.load_array(data)
    time.sleep(0.01)







