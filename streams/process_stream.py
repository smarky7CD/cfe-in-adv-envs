import random

streams = ['kosarak','retail']

for stream_name in streams:
    
    elements = []
    
    with open(f'{stream_name}/{stream_name}_unprocessed.txt', 'r') as rf:
        for line in rf:
            line = line.rstrip()
            items = line.split(" ")
            for item in items:
                elements.append(item)

    random.shuffle(elements)

    with open(f'{stream_name}/test_{stream_name}_stream.txt','w') as of:
        for element in elements:
            of.write(f"{element}\n")