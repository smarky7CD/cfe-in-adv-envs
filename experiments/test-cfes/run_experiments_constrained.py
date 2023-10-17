import sys, os, random
sys.path.extend([f'./{name}' for name in os.listdir(".") if os.path.isdir(name)])

from ck import CK
from cms import CMS 
from hk import HK

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
    for trial in range(1000):


        print(f"Stream {stream}, Trial {trial}")

        cfe_ck = CK(341,2)
        cfe_cms = CMS(512,4)
        cfe_hk = HK(246,4)
        
        random.shuffle(elements)

        #insert stream
        freq = {}
        for e in elements: 
            if (e in freq): 
                freq[e] += 1
            else: 
                freq[e] = 1
            cfe_ck.up(e)
            cfe_cms.up(e)
            cfe_hk.up(e)

        sfreq = sorted(freq.items(), key=lambda x: x[1], reverse=True)
        
        # log_data
        ck_of = open(f"./data/ck_341x2_{stream}/{trial}.csv","w")
        cms_of = open(f"./data/cms_512x4_{stream}/{trial}.csv","w")
        hk_of = open(f"./data/hk_246x4_{stream}/{trial}.csv","w")
    
    
        ck_of.write("Item,TrueFreq,EstFrq,AbsErr,PctErr,EstimatorUsed\n")
        cms_of.write("Item,TrueFreq,EstFrq,AbsErr,PctErr\n") 
        hk_of.write("Item,TrueFreq,EstFrq,AbsErr,PctErr\n")
        

        for e in sfreq:
            item = e[0]
            tfrq = e[1]

            ck_efrq,ck_estimator = cfe_ck.qry(item)
            ck_ae = abs(tfrq-ck_efrq)
            ck_pe = (ck_ae / tfrq) * 100
            ck_of.write(f"{item},{tfrq},{ck_efrq},{ck_ae},{ck_pe},{ck_estimator}\n")
            
            cms_efrq = cfe_cms.qry(item)
            cms_ae = abs(tfrq - cms_efrq)
            cms_pe = (cms_ae / tfrq) * 100
            cms_of.write(f"{item},{tfrq},{cms_efrq},{cms_ae},{cms_pe}\n")

            hk_efrq = cfe_hk.qry(item)
            hk_ae = abs(tfrq - hk_efrq)
            hk_pe = (hk_ae / tfrq) * 100
            hk_of.write(f"{item},{tfrq},{hk_efrq},{hk_ae},{hk_pe}\n")

        ck_of.close()
        cms_of.close() 
        hk_of.close()
        

