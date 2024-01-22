streams = ['kosarak','novel','retail']


for stream_name in streams:
    with open(f'{stream_name}/{stream_name}_stream.txt', 'r') as rf:
        lines = rf.readlines()
        lines = [line.rstrip() for line in lines]

    freq = {} 
    N = 0
    for item in lines: 
        N+=1
        if (item in freq): 
            freq[item] += 1
        else: 
            freq[item] = 1

    sfreq = sorted(freq.items(), key=lambda x: x[1], reverse=True)

    with open(f'{stream_name}/{stream_name}_stream_info.csv', 'w') as wf:
        wf.write("Item,Count\n")
        for e in sfreq:
            wf.write(f"{e[0]},{e[1]}\n")

    print(f"{stream_name}")
    print(f"Domain Size: {len(sfreq)}")
    print(f"Stream Length: {N}\n")  
    