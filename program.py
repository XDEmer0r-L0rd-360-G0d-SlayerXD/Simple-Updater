import sys

VERSION = 'dev_1'

for a in sys.argv[1:]:
    if a == '-v':
        print('v0.0')
        exit()
print('other stuff')