import sys, os, random
sys.path.extend([f'./{name}' for name in os.listdir(".") if os.path.isdir(name)])

from ck import CK


structs = ["ck"] # ,"cms","hk"]
streams = ["kosarak","retail","novel"]
params = [["1024x4"]] #, ["512x4"], ["256x4","341x3","512x2"]]

for i,struct in enumerate(structs):
        for stream in streams:
            for p in params[i]:
                os.mkdir(f"./data/{struct}_{p}_{stream}")


streams = {"retail" : [], "kosarak" : [], "novel" : []}

with open('./streams/retail_stream.txt','r') as f:
        retail_elements = [line.rstrip() for line in f]
streams["retail"] = retail_elements

with open('./streams/kosarak_stream.txt','r') as f:
        kosarak_elements = [line.rstrip() for line in f]
streams["kosarak"] = kosarak_elements

with open('./streams/novel_stream.txt','r') as f:
        novel_elements = [line.rstrip() for line in f]
streams["novel"] = novel_elements

for stream, elements in streams.items():
    for trial in range(100):


        print(f"Stream {stream}, Trial {trial}")

        cfe_ck = CK(1024,4,0.0012)
        
        random.shuffle(elements)

        #insert stream
        freq = {}
        for e in elements: 
            if (e in freq): 
                freq[e] += 1
            else: 
                freq[e] = 1
            cfe_ck.up(e)


        sfreq = sorted(freq.items(), key=lambda x: x[1], reverse=True)
        
        # log_data
        ck_of = open(f"./data/ck_1024x4_{stream}/{trial}.csv","w")
        ck_of.write("Item,TrueFreq,EstFrq,AbsErr,PctErr,Flag\n")

        for e in sfreq:
            item = e[0]
            tfrq = e[1]

            ck_efrq,flag = cfe_ck.qry(item)
            ck_ae = abs(tfrq-ck_efrq)
            ck_pe = (ck_ae / tfrq) * 100
            ck_of.write(f"{item},{tfrq},{ck_efrq},{ck_ae},{ck_pe},{flag}\n")

        ck_of.close()
        

