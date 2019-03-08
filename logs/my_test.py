import sys
inFile = open(sys.argv[1], 'r')
outFile = open(sys.argv[2], 'w')    
read = True
for i in inFile.read():
        if i == '<':
            read = not read
        if read:
            outFile.write(i)
        if i == '>':
            read = not read
