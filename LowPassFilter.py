input_file = '1.ZHR'
output_file = '3.ibi'

time = 0

from matplotlib import pyplot as plt
data = [[] for i in range(3)]
f = open(input_file, 'rb')
#o = open(output_file, 'w')
a = f.read()
for i in range(0x00, len(a) - 32, 32):
    for j in range(0, len(data) * 2, 2):
        d = ord(a[i+j+1]) * 2**8 + ord(a[i+j+2])
        if d > 2**15:
            d = d - 2**16
        data[j / 2].append(d)

    '''o.write(str(time / 500.0))
    o.write(',')
    for j in range(len(data)):
        o.write(str(data[j][len(data[j]) - 1]))
        o.write(',')
    o.write(chr(13))

    time += 1'''


print len(data[0])
plt.plot(data[0])
plt.show()
