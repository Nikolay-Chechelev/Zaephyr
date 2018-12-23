Device = {}
Datatypes = {}
Bodies = {}
Channels = {}
Commands = {}
Answers = {}
Dataflow = {}
CommandList = {}

f = open('1.txt', 'r')
script = f.read()
script = eval(script)
if type(script) == type({}):
    print 'Describing Script is OK!'
else:
    print 'Errors exist! Check your describing script!'
    pass

if 'Device' in script.keys():
    Device = script.get('Device')

if 'Datatypes' in script.keys():
    Datatypes = script.get('Datatypes')

if 'Bodies' in script.keys():
    Bodies = script.get('Bodies')

if 'Channels' in script.keys():
    Channels = script.get('Channels')

if 'Commands' in script.keys():
    Commands = script.get('Commands')

if 'Answers' in script.keys():
    Answers = script.get('Answers')

if 'Dataflow' in script.keys():
    Dataflow = script.get('Dataflow')



for i in Commands.keys():
    Shift = Bodies.get(Commands.get(i)).get('shift')
    Signature = Datatypes.get(Bodies.get(Commands.get(i)).get('type')).get('signature')
    Body = Bodies.get(Commands.get(i)).get('command')
    if Shift >= 0:
        Body = chr(ord(Body) << abs(Shift))
    else:
        Body = chr(ord(Body) >> abs(Shift))
    End = Datatypes.get(Bodies.get(Commands.get(i)).get('type')).get('end')
    cmd = Signature + Body + End
    CommandList[i] = cmd



print CommandList