with open('ejemplo.txt') as f:
    for line in f:
        line = line.strip()
        if line.startswith('The'):
            print (line)