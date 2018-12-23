DeviceName = ''

f = open('1.txt', 'r')
script = eval(f.read())
if type(script) == type({}):
    print 'Describing Script is OK!'
else:
    print 'Errors exist! Check your describing script!'
    pass

