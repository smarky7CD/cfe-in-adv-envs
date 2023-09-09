import os

structs = ["ck"] # ,"cms","hk"]
streams = ["kosarak","retail","novel"]
params = [["1024x4"]] #, ["512x4"], ["256x4","341x3","512x2"]]

for i,struct in enumerate(structs):
        for stream in streams:
            for p in params[i]:
                os.mkdir(f"{struct}_{p}_{stream}")
