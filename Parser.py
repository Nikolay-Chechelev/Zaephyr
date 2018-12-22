'''
keywords = ['Device', 'Channels']

class Parser():
    def __init__(self, file):
        self.file = file # path to initial file
        self.device_description = {}
        self.channel_description = {}
        self.parameters = [] # will be list of dictionaries with all params

    def load_config(self):
        f = open(self.file, 'r')
        a = f.read()  # read in string
        a = ''.join(a.split('Device{\n\t'))  # cut all Device
        a = a.split('Channels{\n\t')  # cut all Channels
        Device = a[0]  # cut Device area
        del a[0]
        a = ''.join(a)  # and make string with channels and other data
        Device = ''.join(Device.split('}\n\n'))  # cut all new lines
        Device = Device.split('\n\t')  # cut all TABs
        for i in range(len(Device)):
            self.device_description[Device[i].split('=')[0]] = Device[i].split('=')[1]
        self.parameters.append(self.device_description)
        ##################################################### Here we should cut smth next after Cannels area
        a = ''.join(a.split('}}\n\n\n'))  # cut all Device
        for i in range(int(self.device_description['channels'])):
            a = ''.join(a.split('name' + str(i + 1) + '='))
            a = a.split('name' + str(i + 2) + '=')
            c = a[0]
            del a[0]
            a = ''.join(a)
            c = c.split('{\n\t\t')
            d = c[0]
            del c[0]
            self.channel_description[d] = {}
            c = ''.join(c)
            c = ''.join(c.split('}\n\t'))
            c = c.split('\n\t\t')
            for j in range(len(c)):
                self.channel_description[d][c[j].split('=')[0]] = c[j].split('=')[1]
        self.parameters.append(self.channel_description)
        return self.parameters

    def save_config(self):
        return 0

p = Parser('test.ini')
print p.load_config()'''

f = open('1.txt', 'r')
c = f.read()
try:
    print 'Yes'
    c = eval(c)
except:
    pass
print c, type(c)